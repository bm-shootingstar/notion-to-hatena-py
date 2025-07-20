# Notion to Hatena Blog

Notion のドキュメントをはてなブログに投稿するための python ツールです。

## 概要

このツールは、指定された Notion のページを取得し、Markdown 形式に変換した後、はてなブログに新しい記事として投稿します。

## 特徴

- Notion API を利用してページコンテンツを取得
- 基本的な Notion ブロック（見出し、段落、リスト、コードなど）を Markdown に変換
- はてなブログの AtomPub API を利用して記事を投稿
- API キーなどの機密情報を `.env` ファイルで安全に管理
- Notion のコールアウトをはてなブログ上で再現（要 CSS 設定）

## 必要なもの

- Python 3.8 以上
- [uv](https://github.com/astral-sh/uv) (Python パッケージインストーラー)

## セットアップ

1.  **リポジトリをクローンします**

    ```bash
    git clone https://github.com/bm-shootingstar/notion-to-hatena-py.git
    cd notion_to_hatena
    ```

2.  **Python 仮想環境を作成し、依存ライブラリをインストールします**

    ```bash
    # 仮想環境の作成
    uv venv

    # 依存ライブラリの同期
    uv sync

    ```

3.  **`.env` ファイルを設定します**

    `.env.example` ファイルをコピーして `.env` ファイルを作成します。

    ```bash
    cp .env.example .env
    ```

    次に、`.env` ファイルを編集し、あなたの Notion と、はてなブログの情報を設定します。

    ```
    NOTION_API_KEY='YOUR_NOTION_API_KEY'
    HATENA_API_KEY='YOUR_HATENA_API_KEY'
    HATENA_USER_ID='YOUR_HATENA_USER_ID'
    HATENA_BLOG_ID='YOUR_HATENA_BLOG_ID'
    ```

    - `NOTION_API_KEY`: [Notion インテグレーション](https://www.notion.so/my-integrations)から取得した API キー。

      <details>
      <summary>Notionインテグレーションのトークン取得方法</summary>

      1. [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations) にアクセスします。
      2. 「新しいインテグレーション」を作成します。
      3. 「基本情報」でインテグレーションに名前を付けます。
      4. 「機能」で「コンテンツ機能」の「読み取り機能」を有効にします。
      5. 「保存」をクリックすると、インテグレーションのシークレット（API キー）が生成されます。
      6. 共有したい Notion のページ右上のメニューから「コネクトの追加」を選択し、作成したインテグレーションを連携させます。

      </details>

    - `HATENA_API_KEY`: はてなブログの「設定」→「詳細設定」→「API キー」で確認できます。
    - `HATENA_USER_ID`: あなたのはてな ID。
    - `HATENA_BLOG_ID`: あなたのはてなブログのドメイン名 (例: `example.hatenablog.com`)。

4.  **（任意）コールアウト機能のための CSS を設定します**

    Notion のコールアウト機能を使用する場合、はてなブログのデザイン CSS にスタイルを追加する必要があります。

    `documents/hatena_design_css.css` の内容を、はてなブログの **「デザイン」>「カスタマイズ」（レンチのアイコン）>「デザイン CSS」** に貼り付けてください。

    現在、以下の絵文字に対応した色分けが設定されています。

    - 💡, ℹ️ : 情報（青色）
    - ⚠️ : 警告（黄色）
    - 🔥 : 危険（赤色）
    - ✅ : 成功（緑色）
    - 上記以外の絵文字 : デフォルト（灰色）

## 使い方

以下のコマンドを実行して、Notion ページをはてなブログに投稿します。デフォルトでは下書きとして投稿されます。

```bash
python main.py <NOTION_PAGE_ID_OR_URL>
```

- `<NOTION_PAGE_ID_OR_URL>`: 投稿したい Notion ページの ID または URL に置き換えてください。

公開状態で投稿するには、`--publish` フラグを追加します。

```bash
python main.py <NOTION_PAGE_ID_OR_URL> --publish
```

### 例

```bash
# ページIDで指定（下書き）
python main.py a1b2c3d4-e5f6-7890-1234-567890abcdef

# URLで指定（公開）
python main.py https://www.notion.so/your-workspace/My-Awesome-Post-a1b2c3d4e5f678901234567890abcdef --publish
```

投稿が成功すると、コンソールに成功メッセージが表示されます。

## ライセンス

このプロジェクトは MIT ライセンスのもとで公開されています。詳細は `LICENSE` ファイルを参照してください。

## 今後の予定

- GUI 機能の追加
- スタンドアローンアプリとしてリリース
