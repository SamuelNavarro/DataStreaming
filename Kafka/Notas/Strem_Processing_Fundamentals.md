# Stream Processing Fundamentals #


- Join (Streams) - The process of combining one or more streams into an output stream, typically on some related key attribute.
    Filtering (Streams) - The process of removing certain events in a data stream based on a condition
- Aggregating (Streams) - The process of summing, reducing, or otherwise grouping data based on a key attribute
- Remapping (Streams) - The process of modifying the input stream data structure into a different output structure. This may include the addition or removal of fields on a given event.
- Windowing (Streams) - Defining a period of time from which data is analyzed. Once data falls outside of that period of time, it is no longer valid for streaming analysis.
- Tumbling Window (Streams) - The tumbling window defines a block of time which rolls over once the duration has elapsed. A tumbling window of one hour, started now, would collect all data for the next 60 minutes. Then, at the 60 minute mark, it would reset all of the data in the topic, and begin collecting a fresh set of data for the next 60 minutes.
- Hopping Window (Streams) - Hopping windows advance in defined increments of time. A hopping window consists of a window length, e.g. 30 minutes, and an increment time, e.g. 5 minutes. Every time the increment time expires, the window is advanced forward by the increment.
- Sliding Window (Streams) - Sliding Windows work identically to Hopping Windows, except the increment period is much smaller -- typically measured in seconds. Sliding windows are constantly updated and always represent the most up-to-date state of a given stream aggregation.
- Stream - Streams contain all events in a topic, immutable, and in order. As new events occur, they are simply appended to the end of the stream.
- Table - Tables are the result of aggregation operations in stream processing applications. They are a roll-up, point-in-time view of data.
- Stateful - Stateful operations must store the intermediate results of combining multiple events to represent the latest point-in-time value for a given key

## Combining Streams ##


- Combining, or joining, streams is the action of taking one or more streams and creating a single new output stream.
- Joined streams always share some common attribute across the data in all of the streams. For example, we might use a user_id to merge user streams.
- State must be kept as events flow through the join calculation, until all of the related data has arrived. Once this happens, the new event can be emitted, and the state can be flushed
  - If the related data never fully arrives, at some point the data in memory should be cleared
  - This process is typically accomplished through windowing, which is covered in a later section of this lesson.






Reason why you want to combine streams:
To group realated date streams into a single unified stream.
To group related data streams into one place, so taht you can analyze that dta and emit new data based on the contents.

It often increases the space and its usually not a good practice to have more than one event type in a single stream.

Some of the reaons you may want to filter streams:
- To create a tailored dataset for a particular audience.
- To remove unneced or unreleated data
- To improve performance and scalability f a processing application. 
  


## Remapping Streams
Is the process of tranforming an input event and outputting it in a different form to a new stream. 

It is also used to remove specific or necessary fields. We are not removing the entire event, we are simply removing 1 or more fields from the event. 




- Remapping streams is the process of transforming an input event and outputting it in a different form to a new stream
- Remapping may be done in conjunction with other processing steps, such as filters or joins
- Remapping is commonly used for data health, application compatibility, and security reasons
- Example Scenario 1: Transforming one data serialization format to another. E.g., Avro -> JSON, or JSON-> Avro
- Example Scenario 2: Removing sensitive or unnecessary fields from an input payload
- Example Scenario 3: Transforming an input event into a format suitable for downstream use by moving data fields or renaming them



One of the common use cases for data remapping, is filtering out personal identifiably information.




Reasons you might want to remap streams:
- Transforming data for applications which expect a different data structure.
- Changing dta serialization format, e.g. JSON to Avro, or vice versa
- Removing sensitive fields from input data. 
  
  
### Agregation

Max, Min, Sums, Histograms, Sets and Lists.

An aggregation involves taking two or more events and create one or more event based on a calculation of some kind. 


Aggregates in streaming applications almost always involve a timeframe, unless the source topic is compacted
    

It's important to understand what kind of topic you are working with, if your are working nwith a compacted topic, you can run aggregate functions across all the data available for all time for a given topic but most kafka topics for stream procesisng applications will be expired and not compacted. 



### Tumbling Window

Represent a fixed period of timei that rolls over after that period of time has elapsed.
- Tumbling windows do not overlap.
- Tumbling windows do not have gaps between windowed periods. 


### Hopping Window

- Hopping windows have both a duration and an increment by which they are advanced
  - ex.- A window of 45 minutes with an increment of 5 minutes would advance every 5 minutes. The oldest 5 minutes of the previous window would be dropped, and the newest 5 minutes of data would be added.
- Hopping windows can overlap with previous windows
- Hopping windows can have gaps if the increment time is larger than the duration period
- Possibly gaps between windows.

Examples:

- A team wants to measure the last 10 minutes of errors on a 1-minute rolling basis.
- The manufacturing team would like agregate production numbers from each of their production lines for the last 24 hours, on a 1-hour rolling basis.



### Sliding windows

Most updated representation of the defined time period posible. 


- Similar to Hopping Window, except the increment is not directly configurable and updates in real-time
  - A sliding window of the last 12 hours always includes all of the last 12 hours of data. Data is expired as soon as it reaches the 12-hour threshold, and new data is added as soon as it is received.
- Sliding Windows have no gaps between windows
- Sliding Windows do overlap

Examples:
- A critical alerting system that analyzes the most recent 5 minutes of data for outages.
- A marketing tool that requires the most recent 15 minutes of cart abandonmnet data to send follow-up emails. 

### Streams and Tables

The difference between stream processing *streams* and stream processing *tables* 
A **Table** implies state and an agreggation of some kind whereas a stream is a never ending immutable series of ordered events.

Of Streams and Tables in Kafka and Stream Processing, Part 1 : https://www.michael-noll.com/blog/2018/04/05/of-stream-and-tables-in-kafka-and-stream-processing-part1/

Data enrichment is an example of an scenario where you may take advantage of a stream. 


When we aggregate data in our streaming applications, we are creating a point-time view of the data. This point time analysis represents snapchat in time. Unlike streams that are ordered, unmmutable and unbounded, tables are the not neccesarly orderd, are mutable and are bounded. 



Streams output and unbounded sequence of events, Tabls output a point-in-time aggregate view. 

Examples of streams:
- Remapping a field on all incoming events in a stream and re-emitting the event.
- Reading n all events in a stream and filtering some, while re-emitting the rest.


Examples of tables:
- A histogram of response times for a page for the past 3 hours. 
- A list of unique currencies processed in the last hour. 

Because tables are stateful, they can be stored. 

## Data Storage ##


ksql, faust, kafka sql or flink, all use kafka topics to store the internal state of a stream processing application that are running, this may be referred as **changelog**. 

Kafka changelog topic tracks all changes in stream. So the state easily be created as needed. 

- Changelog topics are log compacted. So the size of the topics is small which can aid in startup time. 

When we have this changelog, we have the ability to recover quickly. 

Most streams framewokrs will use in-memory storage to restore state. While this is fast ant he usage of the compacted kafka topics provide fault tolerance, is not suitable for production so there should be better strategies that help boot times on our nodes than using in-memory storage. 


**RocksDB** is for this. RocksDB is used to reduce quickstart times in reboot *on the same node*. Ksql, Faust, Kafka streams, Flink, all use RocksDB as an option. 


If you use something in production, use RocksDB.



The Kafka role as a data store is:
- Track all state changes in a stream processing application.
- Aid in fault tolerance and recovery if a node reboots. 

The local state storage for stream processing nodes is provided by RocksDB and the in-memory storage for stream processing nodes is provided by the stream processing application itself.


The role of RocksDB as a data store is:
- Provide quick boot times between restarts on a given node.
- Hold the current state of the stream processing application on a given node. 
  
Kafka is used for fault tolerance between node failures. RocksDB is specific to a given node.  and RocksDB does not replicate data between nodes.  
  

