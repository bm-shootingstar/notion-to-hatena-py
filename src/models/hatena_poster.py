import base64
import hashlib
import logging
import os
from datetime import datetime, timezone
from xml.etree import ElementTree

import requests

from src.utils.env_loader import load_env

load_env()

logger = logging.getLogger(__name__)


def _generate_wsse_header(hatena_user_id, hatena_api_key):
    """Generates WSSE authentication header for Hatena API."""
    created = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    b_nonce = hashlib.sha1(os.urandom(16)).digest()
    b_digest = hashlib.sha1(b_nonce + created.encode("ascii") + hatena_api_key.encode("ascii")).digest()
    nonce = base64.b64encode(b_nonce).decode("ascii")
    digest = base64.b64encode(b_digest).decode("ascii")
    return f'UsernameToken Username="{hatena_user_id}", PasswordDigest="{digest}", Nonce="{nonce}", Created="{created}"'


def upload_image_to_hatena_photolife(image_url: str) -> str | None:
    """
    Uploads an image to Hatena Photolife and returns the permanent URL.

    Args:
        image_url: The temporary URL of the image from Notion.

    Returns:
        The permanent URL of the uploaded image on Hatena Photolife, or None on failure.
    """
    hatena_user_id = os.environ["HATENA_USER_ID"]
    hatena_api_key = os.environ["HATENA_API_KEY"]

    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        image_data = response.content
        content_type = response.headers.get("Content-Type", "image/jpeg")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to download image from {image_url}. {e}")
        return None

    url = "https://f.hatena.ne.jp/atom/post"
    title = "image"  # Title in Hatena Photolife (can be customized)
    xml_data = f"""<entry xmlns="http://purl.org/atom/ns#">
<title>{title}</title>
<content mode="base64" type="{content_type}">{base64.b64encode(image_data).decode()}</content>
</entry>"""

    headers = {"X-WSSE": _generate_wsse_header(hatena_user_id, hatena_api_key)}

    try:
        post_response = requests.post(url, headers=headers, data=xml_data.encode("utf-8"))
        post_response.raise_for_status()

        # Register the Hatena namespace to find hatena:syntax
        namespaces = {
            "hatena": "http://www.hatena.ne.jp/info/xmlns#",
            "atom": "http://www.w3.org/2005/Atom",
        }
        root = ElementTree.fromstring(post_response.content)

        syntax_tag = root.find("hatena:syntax", namespaces)
        if syntax_tag is not None:
            # Return the Hatena syntax which is like [f:id:user:yyyymmddhhmmss:plain]
            return syntax_tag.text
        else:
            # Fallback to find the alternate link if syntax is not available
            alt_link = root.find('atom:link[@rel="alternate"]', namespaces)
            if alt_link is not None:
                return alt_link.get("href")
            else:
                logger.error("Could not find image URL in Hatena Photolife response.")
                logger.error(f"Response: {post_response.text}")
                return None

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to upload image to Hatena Photolife. {e}")
        if "post_response" in locals():
            logger.error(f"Response: {post_response.text}")
        return None
    except ElementTree.ParseError as e:
        logger.error(f"Failed to parse Hatena Photolife XML response. {e}")
        return None


def post_to_hatena(title: str, content: str, draft: bool = True):
    """
    Posts an article to Hatena Blog.

    Args:
        title: The title of the article.
        content: The content of the article in Markdown format.
        draft: If True, post as a draft. Defaults to True.
    """
    hatena_user_id = os.environ["HATENA_USER_ID"]
    hatena_blog_id = os.environ["HATENA_BLOG_ID"]
    hatena_api_key = os.environ["HATENA_API_KEY"]

    url = f"https://blog.hatena.ne.jp/{hatena_user_id}/{hatena_blog_id}/atom/entry"

    headers = {"Content-Type": "application/xml"}

    draft_tag = ""
    if draft:
        draft_tag = "<app:control><app:draft>yes</app:draft></app:control>"

    data = f"""<?xml version="1.0" encoding="utf-8"?>
<entry xmlns="http://www.w3.org/2005/Atom"
       xmlns:app="http://www.w3.org/2007/app">
  <title>{title}</title>
  <author><name>{hatena_user_id}</name></author>
  <content type="text/markdown"><![CDATA[{content}]]></content>
  {draft_tag}
</entry>"""

    response = requests.post(url, auth=(hatena_user_id, hatena_api_key), headers=headers, data=data.encode("utf-8"))

    if response.status_code == 201:
        status = "draft" if draft else "published"
        logger.info(f"Successfully posted to Hatena Blog as a {status}.")
    else:
        logger.error(f"Failed to post to Hatena Blog. Status code: {response.status_code}")
        logger.error(response.text)


if __name__ == "__main__":
    # Test post
    logging.basicConfig(level=logging.INFO)
    post_to_hatena("Test Title", "# Hello Hatena\n\nThis is a test post.")
