# CLAUDE.md

このファイルは、Claude Code（claude.ai/code）がこのリポジトリ内のコードを扱う際のガイダンスを提供します。

## 概要

このプロジェクトは、Databricksのサンプルプロジェクトであり、データ処理、可視化、パイプライン開発のための様々なノートブックやPythonスクリプトを含みます。データの取り込み、変換、テーブル作成など、Databricksの典型的なワークフローを実演しています。

## プロジェクト構成

- `sandbox/` - データ処理パターンを示すDatabricksノートブックとPythonスクリプトを格納
  - `01_quick-start.py` - サンプルのNYCタクシーデータをクエリする基本ノートブック
  - `02_import-visualize-data.py` - ボリュームを使ったデータインポート、外部CSVデータのダウンロード、管理テーブルの作成
  - `03_create-table.py` - テーブル作成とデータ挿入の例
  - `data-pipeline-get-started/transformations/my_transformation.py` - DLT（Delta Live Tables）パイプラインによるストリーミングデータの取り込みと変換

## 主なアーキテクチャパターン

### データパイプラインアーキテクチャ
DatabricksのUnity Catalog三層ネームスペース（`catalog.schema.table`）に従います。
- デフォルトカタログ: `workspace`
- デフォルトスキーマ: `databricks_sandbox`
- 外部データ保存には管理ボリュームを使用: `/Volumes/workspace/databricks_sandbox/health_data`

### DLTパイプラインパターン
`my_transformation.py`は完全なDLTパイプラインを示します。
1. **生データ取り込み**: Auto Loader（`cloudFiles`形式）によるストリーミングテーブル
2. **データ検証**: `@dlt.expect`を使ったデータ品質期待値付きのマテリアライズドビュー
3. **集計処理**: フィルタ・グループ化された最終マテリアライズドビュー

### データ処理ワークフロー
1. 外部データ保存用の管理ボリューム作成
2. `dbutils.fs.cp()`でデータダウンロード
3. Sparkでデータ読み込み（`spark.read.csv()`）
4. データ変換（カラム名変更、スキーマ推論）
5. `saveAsTable()`で管理テーブルへ書き込み

## よくある開発作業

### ノートブックの実行
これらはDatabricks環境で実行するノートブックです。ローカルのPythonスクリプトとして単独で実行することはできません。

### データソース
- NYCタクシーデータ: `samples.nyctaxi.trips`（Databricks組み込みサンプル）
- 外部CSV: NY.gov APIのヘルスデータ
- Million Song Dataset: `/databricks-datasets/songs/data-001/`

### DLTパイプライン開発
このプロジェクトはDelta Live Tablesによるデータパイプラインのオーケストレーションを行います。
- `StructType`と`StructField`でスキーマを明示的に定義
- テーブル定義に`@dlt.table`デコレーターを使用
- `@dlt.expect`でデータ品質ルールを適用
- テーブル依存関係による変換の連鎖

## 技術詳細

### データスキーマ
- NYCタクシーデータには乗降時刻、距離、運賃、ZIPコードなどが含まれます
- NYヘルスデータのベビーネームデータセットには年、名前、件数情報
- ソングデータセットにはアーティストメタデータ、音響特徴量、時系列情報

### PySparkパターン
- カラム名変更: `withColumnRenamed()`
- スキーマ推論: CSVリーダーで`inferSchema=True`
- ストリーミングデータ: Auto Loaderを使った`readStream`
- データ検証: DLT期待値によるNullチェックや値制約