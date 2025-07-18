# Databricks notebook source
# MAGIC %sql
# MAGIC USE CATALOG workspace;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC CREATE TABLE IF NOT EXISTS default.department
# MAGIC (
# MAGIC    deptcode   INT,
# MAGIC    deptname  STRING,
# MAGIC    location  STRING
# MAGIC );

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO default.department VALUES
# MAGIC    (10, 'FINANCE', 'EDINBURGH'),
# MAGIC    (20, 'SOFTWARE', 'PADDINGTON');
