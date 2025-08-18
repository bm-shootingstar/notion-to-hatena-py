from src.hatena_poster import upload_image_to_hatena_photolife


def convert_to_markdown(blocks: list) -> str:
    """
    Converts a list of Notion blocks to a Markdown string.

    Args:
        blocks: A list of Notion block objects.

    Returns:
        A string in Markdown format.
    """
    markdown_lines = []
    for block in blocks:
        block_type = block.get("type")

        if block_type == "heading_1":
            text = block["heading_1"]["rich_text"][0]["plain_text"]
            markdown_lines.append(f"# {text}")
        elif block_type == "heading_2":
            text = block["heading_2"]["rich_text"][0]["plain_text"]
            markdown_lines.append(f"## {text}")
        elif block_type == "heading_3":
            text = block["heading_3"]["rich_text"][0]["plain_text"]
            markdown_lines.append(f"### {text}")
        elif block_type == "paragraph":
            line_parts = []
            for rich_text in block["paragraph"]["rich_text"]:
                text_content = rich_text["plain_text"]
                link_info = rich_text.get("href")

                if link_info:
                    if text_content == link_info:
                        line_parts.append(link_info)
                    else:
                        line_parts.append(f"[{link_info}:title={text_content}]")
                else:
                    line_parts.append(text_content)

            full_line = "".join(line_parts)

            # Handle multi-line paragraphs by adding markdown line breaks
            processed_line = "  \n".join(full_line.split("\n"))
            markdown_lines.append(processed_line)

        elif block_type == "bulleted_list_item":
            text = block["bulleted_list_item"]["rich_text"][0]["plain_text"]
            markdown_lines.append(f"- {text}")
        elif block_type == "numbered_list_item":
            text = block["numbered_list_item"]["rich_text"][0]["plain_text"]
            markdown_lines.append(f"1. {text}")
        elif block_type == "code":
            text = block["code"]["rich_text"][0]["plain_text"]
            language = block["code"]["language"]
            markdown_lines.append(f'```"{language}"\n{text}\n```')
        elif block_type == "quote":
            text = block["quote"]["rich_text"][0]["plain_text"]
            markdown_lines.append(f"> {text}")
        elif block_type == "image":
            notion_image_url = block["image"]["file"]["url"]
            hatena_image_url = upload_image_to_hatena_photolife(notion_image_url)
            if hatena_image_url:
                markdown_lines.append(hatena_image_url)
            else:
                # Fallback to original URL if upload fails
                markdown_lines.append(f"![image]({notion_image_url})")
        elif block_type in ["bookmark", "link_preview", "embed"]:
            url = block.get(block_type, {}).get("url")
            if url:
                markdown_lines.append(f"[{url}:embed]")
        elif block_type == "callout":
            icon_emoji = block.get("callout", {}).get("icon", {}).get("emoji", "📣")
            text = "".join([t["plain_text"] for t in block["callout"]["rich_text"]])

            emoji_to_class = {
                "💡": "callout-info",
                "ℹ️": "callout-info",
                "⚠️": "callout-warning",
                "🔥": "callout-danger",
                "✅": "callout-success",
            }
            callout_class = emoji_to_class.get(icon_emoji, "callout-default")

            html = f"""<div class="callout {callout_class}">
<div class="callout-icon">{icon_emoji}</div>
<div class="callout-content"><p>{text}</p></div>
</div>"""
            markdown_lines.append(html)
        elif block_type == "table":
            table_rows = block.get("children", [])
            if not table_rows:
                continue

            has_header = block.get("table", {}).get("has_column_header", False)
            html_table = "<table>"

            if has_header:
                header_row = table_rows[0]
                html_table += "<thead><tr>"
                for cell in header_row.get("table_row", {}).get("cells", []):
                    cell_text = "".join([t.get("plain_text", "") for t in cell])
                    html_table += f"<th>{cell_text}</th>"
                html_table += "</tr></thead>"
                table_rows = table_rows[1:]  # Remove header row

            html_table += "<tbody>"
            for row in table_rows:
                html_table += "<tr>"
                for cell in row.get("table_row", {}).get("cells", []):
                    cell_text = "".join([t.get("plain_text", "") for t in cell])
                    html_table += f"<td>{cell_text}</td>"
                html_table += "</tr>"
            html_table += "</tbody></table>"
            markdown_lines.append(html_table)

    return "\n\n".join(markdown_lines)
