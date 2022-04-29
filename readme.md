# Mahjong Management Slack bot with Azure App Service & Azure SQL Database

麻雀の進行状況を管理してくれるslack botです。

## 大雑把な使い方(後できちんと書く)
- アプリをローカルで動かす場合
    - 適当なAzure SQL DBのインスタンスを作成して接続
        - DBも含めてローカルで動かせるかも? [この辺](https://www.sqlshack.com/how-to-set-up-and-run-sql-server-docker-image/)を参考にすればできる気はする(そのうち試す)
    - 上で作成したDBインスタンスに接続するために.envに必要な環境変数を書く(.env.exampleを参考に)
    - [ここ](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver15)を参考にODBCドライバをインストール
    - migrate.sqlを実行
        - vscodeの[拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-mssql.mssql)を使ってもできるし、SSMS使ってもできる
    - `ngrok http 8089`でローカルホストを公開
    - 別窓で`gunicorn --bind 127.0.0.1:8089 app:flask_app --reload`を実行
    - 適当な名前のslack appを作成
    - slackのScopesを適切に持たせてやる(とりあえず下の権限をBot Token Scopesに持たせているが、多分不要なやつが多いので取捨選択)
        - channels:history
        - channels:join
        - channels:read
        - chat:write
        - groups:history
        - im:history
        - incoming-webhook
        - mpim:history
        - reactions:read
        - reactions:write
        - users:read
    - .envに作成したappのトークンなどを入れる
    - InteractivityとEvent SubscriptionsをOnにして"(ngrokによって公開されてるURL)/slack/events"をURLのところに入れる
    - botをグループに招待
    - "ゲームスタート"でゲームの開始
- アプリをAzureで動かす場合
    - Todo

## 構成
詳しくはdocの中

