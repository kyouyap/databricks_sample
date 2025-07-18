# Databricks notebook source
# MAGIC %sql
# MAGIC SELECT * FROM samples.nyctaxi.trips

# COMMAND ----------

# tpep_pickup_datetime: タクシーの乗車日時（timestamp）
# tpep_dropoff_datetime: タクシーの降車日時（timestamp）
# trip_distance: 旅行距離（double）
# fare_amount: 運賃（double）
# pickup_zip: 乗車地点の郵便番号（int）
# dropoff_zip: 降車地点の郵便番号（int）

display(spark.read.table("samples.nyctaxi.trips"))


# COMMAND ----------

