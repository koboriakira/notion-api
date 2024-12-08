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

### Test (Gauge)

```shell
cd e2e 
npm install
```

`make gauge`または`make gauge-current`を実行
