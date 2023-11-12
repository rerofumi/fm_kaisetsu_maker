# 解説動画メーカー

このプロジェクトは、OpenAI の API を使って解説動画風のムービーファイルを作成する原理試作品です。以下の手順に従って環境をセットアップし、プロジェクトを開始してください。

## 環境のセットアップ

### 仮想環境の作成

このプロジェクトは Python の仮想環境上で実行することをお勧めします。次のコマンドを使って仮想環境を作成してください。

```bash
python3 -m venv venv
```

作成した仮想環境をアクティブにします。

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### 必要なモジュールのインストール

moviepy からで動画作成するには ffmpeg が別途インストールされている必要があります。予め環境に応じた ffmpeg のインストールをしておいてください。

仮想環境がアクティブになったら、必要なモジュールをインストールします。

```bash
pip install -r requirements.txt
```

`requirements.txt` ファイルには、プロジェクトに必要なモジュールがリストされています。

## 環境変数の設定

OPENAI_API_KEY 環境変数を設定して、OpenAI の API にアクセスできるようにします。

#### Windows

```bash
set OPENAI_API_KEY=your_api_key_here
```

#### macOS/Linux

```bash
export OPENAI_API_KEY=your_api_key_here
```

## 実行方法

以下のコマンドを使用して `kaisetsu_maker.py` を実行します。

```bash
python kaisetsu_maker.py "解説して欲しい事柄について"
```

解説して欲しい事柄については以下の様な文章になります

- "プログラミング言語の Python について解説してください"
- "ゲームエンジンの GODOT について、概要とメリットについて説明してください"

## 動画のカスタマイズ

resource ディレクトリ内にある txt ファイルが生成プロンプトになります、書き換えることで異なったテイストになります。

## 同梱フォントについて

このプロジェクトには、Google の Noto Sans JP Medium フォント (`NotoSansJP-Medium.ttf`) が含まれています。これは、日本語のテキスト表示を美しく、一貫性をもって行うために使用されます。Noto フォントプロジェクトは、Google によって開始され、世界中のすべての言語で美しいレンダリングを目指しています。このフォントは [SIL Open Font License, Version 1.1](http://scripts.sil.org/OFL) の下でライセンスされています。

フォントファイルの取り扱いは上記ライセンスに従ってください。

## ライセンスについて

このリポジトリ内のソースコードは、同梱されている Noto Sans JP フォントを除き、MIT ライセンスのもとで公開されています。このライセンスにより、商用利用、修正、配布、プライベート利用が許可されていますが、著作権表示とライセンス表示をソフトウェアのすべての複製または重要な部分に含める必要があります。

詳細については、プロジェクトルートにある `LICENSE` ファイルを参照してください。

Noto Sans JP フォントは別途 [SIL Open Font License, Version 1.1](http://scripts.sil.org/OFL) の下でライセンスされています。

