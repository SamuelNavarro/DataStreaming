from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, to_json, col, unbase64, base64, split, expr
from pyspark.sql.types import StructField, StructType, StringType, BooleanType, ArrayType, DateType

# TO-DO: create a kafka message schema StructType including the following JSON elements:
# {"truckNumber":"5169","destination":"Florida","milesFromShop":505,"odomoterReading":50513}
KafkaMessageSchema = StructType (
    [
        StructField("truckNumber", StringType()),
        StructField("destination", StringType()),
        StructField("milesFromShop", StringType()),
        StructField("odometerReading", StringType()),
    ]
)

# TO-DO: create a spark session, with an appropriately named application name
spark = SparkSession.builder.appName("vehicle-status").getOrCreate()

#TO-DO: set the log level to WARN
spark.sparkContext.setLogLevel('WARN')

#TO-DO: read the vehicle-status kafka topic as a source into a streaming dataframe with the bootstrap server localhost:9092, configuring the stream to read the earliest messages possible                                    
vehiclestatusRawStreamingDF = spark                     \
        .readStream                                     \
        .format('kafka')                                \
        .option('kafka.bootstrap.servers', 'kafka:19092')\
        .option('subscribe', 'vehicle-status')          \
        .option('startingOffsets', 'earliest')          \
        .load()

#TO-DO: using a select expression on the streaming dataframe, cast the key and the value columns from kafka as strings, and then select them
vehicleStatusStreamingDF = vehiclestatusRawStreamingDF.selectExpr("cast(key as string)", "cast(value as string)")

# The value.* grabs all the fields. But why?
#TO-DO: using the kafka message StructType, deserialize the JSON from the streaming dataframe 
vehicleStatusStreamingDF.withColumn("value", from_json("value", KafkaMessageSchema))\
        .select(col('value.*'))                                                     \
        .createOrReplaceTempView("VehicleStatus")

# TO-DO: create a temporary streaming view called "VehicleStatus" 
# it can later be queried with spark.sql

#TO-DO: using spark.sql, select * from VehicleStatus
vehicleStatusSelectStarDF = spark.sql("select * from VehicleStatus")

# TO-DO: write the stream to the console, and configure it to run indefinitely, the console output will look something like this:
# +-----------+------------+-------------+---------------+
# |truckNumber| destination|milesFromShop|odometerReading|
# +-----------+------------+-------------+---------------+
# |       9974|   Tennessee|          221|         335048|
# |       3575|      Canada|          354|          74000|
# |       1444|      Nevada|          257|         395616|
# |       5540|South Dakota|          856|         176293|
# +-----------+------------+-------------+---------------+


vehicleStatusSelectStarDF                   \
        .writeStream                        \
        .outputMode("append")               \
        .format("console")                  \
        .start()                            \
        .awaitTermination()
