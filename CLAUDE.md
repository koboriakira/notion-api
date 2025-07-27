# CLAUDE.md

このファイルは、このリポジトリでコードを扱う際のClaude Code (claude.ai/code) へのガイダンスを提供します。

## 開発コマンド

### ローカル開発
- `make dev` - Docker Composeで開発環境を起動し、http://localhost:10119/docs でAPIドキュメントを開く
- `pipenv run uvicorn main:app --reload --port=8080 --host=0.0.0.0` - ホットリロード付きでAPIサーバーを直接実行

### テスト
- `make test` - slow、learning、genuine APIテストを除いたpytestを実行
- `make test-current` - "current"タグが付いたテストを実行
- `make gauge` - e2eディレクトリからすべてのGauge E2Eテストを実行
- `make gauge-current` - "current"タグが付いたGauge E2Eテストを実行
- `make cdk-test` - CDKテストを実行

### コード品質
- Python 3.12、行長120、Googleスタイルのdocstring規約でRuffを使用
- 依存関係管理にpipenvを使用（Python 3.12）

## アーキテクチャ概要

これは、タスクとコンテンツ管理を自動化するために様々な外部サービスと連携するFastAPIベースのNotion APIサービスです。

### コア要素

**メインアプリケーション構成:**
- `notion_api/main.py` - AWS Lambda用のMangumハンドラーを持つFastAPIアプリケーションのエントリーポイント
- `notion_api/router/` - 機能別に整理されたAPIエンドポイント（tasks、projects、booksなど）
- `notion_api/injector/injector.py` - 静的ファクトリーメソッドを使用した依存性注入コンテナ

**ドメインアーキテクチャ:**
- **Use Cases** (`usecase/`) - タスク管理、プロジェクト作成などの具体的なユースケースを持つビジネスロジック層
- **Domain Models** (`notion_databases/`, `task/`, `project/`) - コアビジネスエンティティとドメインロジック
- **Infrastructure** (`infrastructure/`) - 外部サービス連携（Slack、Google Calendar、Books APIs）
- **Repositories** - タスク、プロジェクト、デイリーログの実装を持つデータアクセス層

**主要な外部連携:**
- **Notion API** - `lotion`ライブラリラッパーを使用したプライマリデータストア
- **Slack** - 通知とコンテキスト管理のためのBot連携
- **OpenAI** - テキスト解析、要約、タグ生成
- **Google Calendar** - 外部カレンダー同期
- **AWS Services** - EventBridgeスケジューリングによるLambdaデプロイ

### 重要なパターン

**依存性注入:**
- 中央の`Injector`クラスが設定済みインスタンスを提供
- サービスは通常、logger、clients、repositoriesが注入される

**タスク管理システム:**
- 設定可能なスケジュールでのルーチンタスク作成
- タスクライフサイクル管理（開始、完了、中止）
- 外部カレンダー同期
- 完了タスクのバックアップシステム

**コンテンツ作成パイプライン:**
- 自動タグ解析と分類によるページ作成
- AI駆動処理によるレシピ、書籍、動画コンテンツクリエーター
- コンテンツ抽出と要約によるWebクリップ処理

**テスト戦略:**
- pytestによるユニットテスト、テストカテゴリのマーカー（slow、learning、use_genuine_api）
- TypeScriptでのGaugeフレームワークを使用したE2Eテスト
- 異なる統合レベルのための分離されたテスト環境

### デプロイ
- CDKを使用したAWS Lambdaデプロイ
- 自動デプロイのためのGitHub Actionsワークフロー
- Dockerベースのローカル開発環境