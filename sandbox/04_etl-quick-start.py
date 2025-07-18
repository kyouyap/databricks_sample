# Databricks notebook source
# MAGIC %sql
# MAGIC CREATE VOLUME IF NOT EXISTS workspace.default.demo_checkpoint;
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import col, current_timestamp

file_path = "/databricks-datasets/structured-streaming/events"
username = spark.sql("SELECT regexp_replace(current_user(), '[^a-zA-Z0-9]', '_')").first()[0]
table_name = f"{username}_etl_quickstart"

volume_base      = "/Volumes/workspace/default/demo_checkpoint"
schema_location  = f"{volume_base}/schema"
checkpoint_path  = f"{volume_base}/checkpoints/{username}/etl_quickstart"

spark.sql(f"DROP TABLE IF EXISTS workspace.default.{table_name}")

(spark.readStream
      .format("cloudFiles")
      .option("cloudFiles.format", "json")
      .option("cloudFiles.schemaLocation", schema_location)
      .load(file_path)
      .select("*",
              col("_metadata.file_path").alias("source_file"),
              current_timestamp().alias("processing_time"))
      .writeStream
      .option("checkpointLocation", checkpoint_path)
      .trigger(availableNow=True)
      .toTable(f"workspace.default.{table_name}"))


# COMMAND ----------

df = spark.read.table(table_name)

# COMMAND ----------

display(df)
