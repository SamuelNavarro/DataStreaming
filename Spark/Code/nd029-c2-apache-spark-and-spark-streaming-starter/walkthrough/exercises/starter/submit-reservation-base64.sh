#!/bin/bash
docker exec -it nd029-c2-apache-spark-and-spark-streaming-starter_spark_1 /opt/bitnami/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.1 /home/workspace/walkthrough/exercises/starter/reservation-base64.py | tee ../../../spark/logs/reservation-base64-walkthrough.log
