# My Notion API

## Usage

ヘッダに`access-token`を指定して（NotionAPIのシークレット）、下記URLを呼び出す

https://6yhkmd3lcl.execute-api.ap-northeast-1.amazonaws.com/v1/projects

## Deploy

GitHub Actionsのdeployワークフローを利用。

## Development

```shell
make run
```

### Test

```shell
# インストール
npm install -g stepci

# 実行
stepci run ./stepci_workflow.yml --secret NOTION_SECRET={type a secret}
```
