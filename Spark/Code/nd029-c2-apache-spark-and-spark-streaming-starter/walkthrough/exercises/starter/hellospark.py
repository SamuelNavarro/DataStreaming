from pyspark.sql import SparkSession

# TO-DO: create a variable with the absolute path to the text file
logfile = "/home/workspace/walkthrough/exercises/starter/Test.txt"

# TO-DO: create a Spark session
spark = SparkSession.builder.appName("HelloSpark").getOrCreate()

# TO-DO: set the log level to WARN
spark.sparkContext.setLogLevel('WARN')

# TO-DO: using the Spark session variable, call the appropriate
# function referencing the text file path to read the text file 
logData = spark.read.text(logfile).cache()

# TO-DO: call the appropriate function to filter the data containing
# the letter 'a', and then count the rows that were found
numas = logData.filter(logData.value.contains('a')).count()
numbs = logData.filter(logData.value.contains('b')).count()

# TO-DO: call the appropriate function to filter the data containing
# the letter 'b', and then count the rows that were found
print(f"Lines with a: {numas}, with b: {numbs}")

# TO-DO: print the count for letter 'd' and letter 's'

# TO-DO: stop the spark application
spark.stop()
