# My Notion API


## Deploy

[Deploy](https://github.com/koboriakira/notion-api/actions/workflows/deploy.yml)を実行。  
Pull Requestからマージしたときは自動で実行される。

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
