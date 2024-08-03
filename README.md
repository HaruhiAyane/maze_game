make_maze.py を用いて、迷路を作成することができます（必ずしもそうする必要はありません）
各png(character：動かすキャラクター, goal：ゴール, goaled_character：ゴール後演出、回しています)
にいい感じの画像を用意して、hand.py を動かすと、迷路が自動生成され、WASDで動かすことができます。

test.py は、hand.py を作る前に練習として作成したものです（とりあえず残します）

API_KEY は、機密情報なので git にはあげていません
.env_sample を参考に、
API_KEY = YOUR_AOU_KEY
CHANNEL_ID = YOUR_CHANNEL_ID
この YOUR_API_KEY のところにあなたの API を貼り付けるなどとしてください（引用符で囲む必要は無いっぽい？）
CHANNEL_ID は、@XYZ の XYZ ではなく URL の channel/ の後ろのところを入力する？ことに注意してください。

main.py は、YouTueAPI と連携するためのものです