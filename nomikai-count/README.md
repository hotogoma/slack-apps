# 飲み会をカウントする
`/hoto-nomikai <yyyy/mm/dd>` で飲み会の日付をDBに登録するスラッシュコマンド
返り値は 初期設定で定義したmax値からDBに登録されたレコード数を引いた数を返す

## 初期設定
- DynamoDBを用意してテーブルを用意する
	- プライマリーキーを `id` という名前で作る
- Slack に Slash Commands を追加する
  - `/hoto-nomikai` が使えるように設定する
  - 作成する API に `GET` リクエストが飛ぶように設定する
- API Gateway で API を作成する
  - `GET` でリクエストを受け付けるリソースを作成する
  - Lambda Proxy integration でイベントをそのまま Lambda Function に流すように設定する
- Lambda Function を作成する
  - ハンドラを `index.handler` に設定する
  - 環境変数を設定する
  	- `TABLE_NAME` : テーブルの名前
	- `MAX_COUNT_NUM` : 飲み会の回数の最大値