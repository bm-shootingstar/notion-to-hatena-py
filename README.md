# Notion to Hatena Blog

Notion のドキュメントを取得し、はてなブログの形式に変換して投稿するためのツールです。
GUI と CLI の両方に対応しており、Windows 用の実行ファイル（exe）としても利用可能です。

## 概要

このツールは、指定された Notion のページを取得し、Markdown 形式に変換した後、はてなブログに新しい記事として投稿します。

## 特徴

- **マルチインターフェース**: 直感的な GUI モードと、自動化に便利な CLI モードを提供。
- **Notion 変換**: 基本的なブロック（見出し、段落、リスト、コード、テーブル等）に加え、画像、ブックマーク、コールアウトにも対応。
- **自動画像アップロード**: Notion 内の画像を自動的にはてなフォトライフへアップロードし、永続的なリンクに変換。
- **機密管理**: API キーなどは `.env` ファイルで安全に管理。
- **Windows 実行ファイル対応**: Python 環境がなくても exe ファイル単体で動作可能。

## 使い方

### Windows 実行ファイル (exe) の場合

1.  `dist/notion-to-hatena.exe` を任意のフォルダに配置します（リポジトリ内では既に `dist` フォルダに同梱されています）。
2.  同じフォルダに `.env` ファイルを作成し、後述の「セットアップ」を参考に API キーを設定します。
3.  `notion-to-hatena.exe` をダブルクリックして起動すると、GUI モードが立ち上がります。
4.  Notion のページ URL または ID を入力し、「Execute」をクリックすると投稿が開始されます。
    - **CLI利用**: コマンドプロンプトから `notion-to-hatena.exe <URL/ID> [--publish]` と入力して実行することも可能です。


### Python スクリプトとして実行する場合

#### セットアップ

1.  **リポジトリをクローンし、依存ライブラリをインストールします**
    ```bash
    git clone https://github.com/bm-shootingstar/notion-to-hatena-py.git
    cd notion-to-hatena-py
    uv sync
    ```

2.  **`.env` ファイルを設定します**
    `.env.example` をコピーして `.env` を作成し、各項目を設定してください。
    ```
    NOTION_API_KEY='YOUR_NOTION_API_KEY'
    HATENA_API_KEY='YOUR_HATENA_API_KEY'
    HATENA_USER_ID='YOUR_HATENA_USER_ID'
    HATENA_BLOG_ID='YOUR_HATENA_BLOG_ID'
    ```
    - 詳細な取得方法は後述の「APIキーの取得方法」を参照してください。

3.  **（任意）コールアウト用の CSS 設定**
    `documents/hatena_design_css.css` の内容を、はてなブログの「デザイン」>「カスタマイズ」>「デザイン CSS」に追加してください。

#### 実行

- **GUI モード**: 引数なしで実行します。
  ```bash
  python main.py
  ```
- **CLI モード**: Notion の URL または ID を引数に渡します。
  ```bash
  # 下書きとして投稿
  python main.py <NOTION_PAGE_ID_OR_URL>
  # 公開状態で投稿
  python main.py <NOTION_PAGE_ID_OR_URL> --publish
  ```

## APIキーの取得方法

<details>
<summary>Notion API キー (インテグレーション・トークン)</summary>

1. [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations) にアクセスします。
2. 「新しいインテグレーション」を作成し、名前を付けます。
3. 「機能」で「読み取り機能」が有効であることを確認し、シークレットを取得します。
4. 投稿したい Notion ページ右上の「...」メニューから「コネクトの追加」を選択し、作成したインテグレーションを連携させます。
</details>

<details>
<summary>はてなブログ API キー</summary>

1. はてなブログの管理画面から「設定」>「詳細設定」を開きます。
2. 下部にある「AtomPub」セクションの「APIキー」を確認してください。
</details>

## エラーハンドリング

- **NOTION_API_KEY が未設定の場合**: GUI モードでは実行時に詳細なエラーダイアログが表示されます。
- **Notion ID が不正な場合**: 入力された URL または ID が解析できない場合、エラーダイアログで通知されます。

## ライセンス

このプロジェクトは MIT ライセンスのもとで公開されています。詳細は `LICENSE` ファイルを参照してください。