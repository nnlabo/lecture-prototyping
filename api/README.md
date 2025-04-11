
# OpenWeather API
https://openweathermap.org/current
- 無料登録が必要かつ、無料ユーザーはCurrent weather dataのみ呼び出し可能。
- ユーザー登録後、APIを呼び出せるようになるまでに数時間待つ必要がある
- [緯度経度を調べられる便利サイトはこちら](https://fukuno.jig.jp/app/map/latlng/)


API呼び出しサンプル（名古屋）

緯度、経度、APIキーをパラメータに設定することで呼び出せる
```
https://api.openweathermap.org/data/2.5/weather?lat=35.175&lon=136.906&appid={API key}
```

# ハンズオン

### 1.PokeAPIをブラウザから使ってみる
- 仕様：https://pokeapi.co/
  - APIドキュメントメニューのPokemon → Pokemonを見てみましょう
- サンプル：https://pokeapi.co/api/v2/pokemon/25

### 2.サンプルプログラムを動かしてみる
先程ダウンロードしたディレクトリ→`api`→`pokeapi_sample.html`をchromeで開く

#### オプション課題： 他の属性を指定して違う画像を表示してみる

##### 概要：
Web APIでは多くの場合、JSONというデータ形式で情報を取得できる。PokeAPIもJSONで情報を取得している。参照するJSONの属性を変更することで、より自分が欲しいデータを取得する練習を行う。

#### 演習内容
pokeapi_sample.htmlファイルをテキストエディタで開いてみると、Option①というコメントがある。javascriptでjsonデータの任意の属性にアクセスする方法や、PokeAPIのドキュメントから他にどんな画像が含まれているのかを確認し、違う画像を表示するように変更してみてください。

``` javascript
getBtn.addEventListener("click", () => {
    let pokemonNumber = document.getElementsByTagName("input")[0].value;
    fetch(url + pokemonNumber)
        .then((res) => res.json())
        .then((jsonData) => {
        nameLabel.innerText = jsonData.name;
        // Option①: 他の属性を指定して違う画像を表示してみる
        img.src = jsonData.sprites.front_default;
    });
});
```


### 3.PokeAPIを呼び出して画像を表示するプログラムをchatGPTに作ってもらい、実行してみる
chat-gptに投げかけ、PokeAPIを呼び出してレスポンスに含まれる画像を表示するプログラムを作ってもらえるか試してみましょう。

### 4.chatGPT APIを呼び出せるプログラムをchatGPTに作ってもらう(実際に動かすにはAPIキーが必要)
chat-gptに投げかけ、openainのAPIを呼び出せるプログラムを作ってもらえるか試してみましょう。可能であればアクセスキーを取得して実際に呼び出してみると良いでしょう。※料金がかかる場合があるので注意


#### オプション課題： pokeapi_sample.htmlを改良し、ポケモンの説明をchat-gptに作成してもらう

##### 概要：
実際に生成AIのAPIを呼び出すことで、自身のアプリで利用する方法を実践してみる。

#### 演習内容
pokeapi_sample.htmlファイルをテキストエディタで開いてみると、Option②というコメントがある。chat-gptのAPIを呼び出して説明文を生成してもらう。生成してもらった説明文をtextareaに表示するように編集してください。

``` javascript
// 生成ボタンをクリックしたときの処理
const textArea = document.getElementsByTagName("textarea")[0];
const generateBtn = document.getElementById("generatebutton");
generateBtn.addEventListener("click", () => {
    // Option②: AIにポケモンの説明を生成してもらい、textareaに表示してみる
    textArea.innerText = "ポケモン。それは不思議な生き物。ポケットモンスター。縮めて、ポケモン"
});
```