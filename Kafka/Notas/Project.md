`kafka-topics --list --zookeeper localhost:2181`


`kafka-avro-console-consumer --topic turnstile --from-beginning --bootstrap-server localhost:9092 --max-messages 10`



Tip: If you want to learn more about the python kafka client, please check out [this tutorial](https://www.confluent.io/blog/introduction-to-apache-kafka-for-python-programmers/?utm_medium=sem&utm_source=google&utm_campaign=ch.sem_br.nonbrand_tp.prs_tgt.kafka_mt.mbm_rgn.apac_lng.eng_dv.all&utm_term=%2Bkafka%20%2Bpython&creative=&device=c&placement=&gclid=Cj0KCQjwhIP6BRCMARIsALu9Lfnf2sDVe8Fn3QlqM4qNnzSfjvElioX3NQ6rDQP1gz7j_Iu14MpcJPsaAuzJEALw_wcB). I would suggest that you could read [this article](https://databricks.com/blog/2017/05/18/taking-apache-sparks-structured-structured-streaming-to-production.html) about how to do Kafka Structured Streaming production monitoring.


## Reviews ##

### Kafka Producer ###

`kafka-topics --list --zookeeper localhost:2181`
`kafka-avro-console-consumer --topic turnstile --from-beginning --bootstrap-server localhost:9092 --max-messages 10`

### Kafka Consumer ###

### Kafka REST Proxy ###
1. `kafka-avro-console-consumer --topic from_weather_topic --from-beginning --bootstrap-server localhost:9092 --max-messages 10`

2. Kafka Schema Registry REST API, a schema is defined for the weather topic. 

### Kafka Connect ###

1. All stations exist in the topic "psql-connector-stations": `kafka-console-consumer --topic psql-connector-stations --from-beginning --bootstrap-server localhost:9092 --max-messages 10`
2.  Using the Kafka Connect REST API, the Kafka Connect configuration is configured to use JSON for both key and values.

Using the Schema Registry REST API, the schemas for stations key and value are visible.

### Faust Streams ###

1. A consumer group for Faust is created: `python consumers/faust_stream.py tables`
2. `python consumers/faust_stream.py --json worker`
3. A topic is present in Kafka with the output topic name the student supplied. `kafka-console-consumer --topic org.chicago.cta.stations.table.v1 --from-beginning --bootstrap-server localhost:9092 --max-messages 10`

### KSQL ###
1. `ksql> select * from turnstile;`
2. `ksql> select * from turnstile_summary;`

