# 暦
Slack に二十四節気を投稿する Lambda Function

## 初期設定
- Python ランタイムの Lambda Function を作成する
  - ハンドラを `main.handler` に設定する
  - 環境変数を設定する
  - デプロイする
- 毎日朝に実行されるように EventBridge トリガーを設定する

## デプロイ
``` console
$ make publish [AWS_PROFILE=...]
```

## 環境変数
| Key | Value |
|---|---|
| `SLACK_INCOMING_WEBHOOK_URL` | `https://hooks.slack.com/services/XXXXXXXXX/XXXXXXXXX/xxxxxxxxxxxxxxxxxxxxxxxx` |