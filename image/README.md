# 画像検索
`/image <キーワード>` で画像を表示するスラッシュコマンド

## 初期設定
- Slack に Slash Commands を追加する
  - `/image` が使えるように設定する
  - 作成する API にリクエストが飛ぶように設定する
- API Gateway で API を作成する
  - Lambda Proxy integration でイベントをそのまま Lambda Function に流すように設定する
- Lambda Function を作成する
  - ハンドラを `main.handler` に設定する
  - 環境変数を設定する
  - デプロイする

## デプロイ
``` console
$ make publish [AWS_PROFILE=...]
```

## 環境変数
| Key | Value |
|---|---|
| `SLACK_SLASH_COMMAND_TOKEN` | Slash Commands で設定されているトークン |
| `GOOGLE_CSE_KEY` | Google の API Key |
| `GOOGLE_CSE_ID` | 作成した Custom Search Engine の ID |
