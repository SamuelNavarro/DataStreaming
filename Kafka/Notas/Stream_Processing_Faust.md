# Stream Processing with Faust #

Glossary of Key Terms You Will Learn in this Lesson

- DSL - Domain Specific Language. A metaprogramming language for specific tasks, such as building database queries or stream processing applications.
- Dataclass (Python) - A special type of Class in which instances are meant to represent data, but not contain mutating functions
- Changelog - An append-only log of changes made to a particular component. In the case of Faust and other stream processors, this tracks all changes to a given processor.
- Processor (Faust) - Functions that take a value and return a value. Can be added in a pre-defined list of callbacks to stream declarations.
- Operations (Faust) - Actions that can be applied to an incoming stream to create an intermediate stream containing some modification, such as a group-by or filter



Faust’s API implements the storage, windowing, aggregation, and other concepts discussed in Lesson 5
Faust is a native Python API, not a Domain Specific Language (DSL) for metaprogramming
Requires no external dependency other than Kafka. Does not require a resource manager like Yarn or Mesos.
Faust does not natively support Avro or Schema Registry



[Every Faust application has an App which instantiates the top-level Faust application](https://faust.readthedocs.io/en/latest/userguide/application.html#what-is-an-application)
The application must be assigned a [topic to subscribe to](https://faust.readthedocs.io/en/latest/userguide/application.html#app-topic-create-a-topic-description)
An output Table or stream receives the output of the processing
An asynchronous function is decorated with an agent which register the function as a callback for the application when data is received

```python
# Please complete the TODO items in this code

import faust

#
# TODO: Create the faust app with a name and broker
#       See: https://faust.readthedocs.io/en/latest/userguide/application.html#application-parameters
#
app = faust.App("first_fast", broker="localhost:9092")

#
# TODO: Connect Faust to com.udacity.streams.clickevents
#       See: https://faust.readthedocs.io/en/latest/userguide/application.html#app-topic-create-a-topic-description
#
topic = app.topic("com.udacity.streams.clickevents")

#
# TODO: Provide an app agent to execute this function on topic event retrieval
#       See: https://faust.readthedocs.io/en/latest/userguide/application.html#app-agent-define-a-new-stream-processor
#
@app.agent(topic)
async def clickevent(clickevents):
    # TODO: Define the async for loop that iterates over clickevents
    #       See: https://faust.readthedocs.io/en/latest/userguide/agents.html#the-stream
    async for event in clickevents:
        print(event)
    # TODO: Print each event inside the for loop


if __name__ == "__main__":
    app.main()
```


### Deserialization in Faust ###


Faust Deserialization - Key Points

- All data model classes must inherit from the faust.Record class if you wish to use them with a Faust topic.
- It is a good idea to specify the serializer type on your so that Faust will deserialize data in this format by default.
- It is a good practice to set validation=True on your data models. When set to true, Faust will enforce that the data being deserialized from Kafka matches the expected type.
  - E.g., if we expect a str for a field, but receive an int, Faust will raise an error.
- Use Faust codecs to build custom serialization and deserialization


### Serialization in Faust ###


Faust Serialization - Key Points

- Serialization in Faust leverages the same faust.Record that we saw in the deserialization section. Faust runs the serializer in reverse to serialize the data for the output stream.
- Multiple serialization codecs may be specified for a given model
  - e.g., serialization=”binary|json”. This means, when serializing, encode to json, then base64 encode the data.




```python
from dataclasses import asdict, dataclass
import json

import faust


@dataclass
class ClickEvent(faust.Record):
    email: str
    timestamp: str
    uri: str
    number: int


@dataclass
class ClickEventSanitized(faust.Record):
    timestamp: str
    uri: str
    number: int


app = faust.App("exercise3", broker="kafka://localhost:9092")
clickevents_topic = app.topic("com.udacity.streams.clickevents", value_type=ClickEvent)

#
# TODO: Define an output topic for sanitized click events, without the user email
#
sanitized_topic = app.topic(
    "com.udacity.streams.clickevents.sanitized",
    key_type=str,
    value_type=ClickEventSanitized,
)

@app.agent(clickevents_topic)
async def clickevent(clickevents):
    async for clickevent in clickevents:
        #
        # TODO: Modify the incoming click event to remove the user email.
        #
        sanitized = ClickEventSanitized(
            timestamp=clickevent.timestamp,
            uri=clickevent.uri,
            number=clickevent.number
        )
        #
        # TODO: Send the data to the topic you created above
        #
        await sanitized_topic.send(key=sanitized.uri, value=sanitized)

if __name__ == "__main__":
    app.main()
```

## Storage in Faust ##

Why is in-memory storage inappropiate for Production?
- Does not surveve restart of the application
- May not be able to fit state in memory.
- May take a long time to restart when loading data from Kafka Changelog topic.

How is Kafka used by Faust?
- To store change events for stateful applications.

Why is RocksDB useful?
- Persists data between applications restarts.
- Allows applications to work with large datasets that don't fit in memory. 
  Allows applications to boot quickly between restarts.
  
  
  
## Stream Basics in Faust ##



- Faust streams are simply infinite asynchronous iterables which perform some processing on incoming messages: https://faust.readthedocs.io/en/latest/userguide/streams.html#id1
- Faust handles consumption, consumer groups, and offsets for you, in addition to managing message acknowledgements : https://faust.readthedocs.io/en/latest/userguide/streams.html#id3
- Faust applications may choose to forward processed messages on to another stream by using the topic.send(<data>) function at the end of the processing loop.

### Streams Processors and Operations ###



- Processors are functions that take a value and return a value and can be added in a pre-defined list of callbacks to your stream declarations: https://faust.readthedocs.io/en/latest/userguide/streams.html#id2
- Processors promote reusability and clarity in your code
- Processors may execute synchronously or asynchronously within the context of your code
    All defined processors will run, in the order they were defined, before the final value is generated.


- Faust Operations are actions that can be applied to an incoming stream to create an intermediate stream containing some modification, such as a group by or filter
- The group_by operation ingests every incoming event from a source topic, and emits it to an intermediate topic with the newly specified key
- The filter operation uses a boolean function to determine whether or not a particular record should be kept or discarded. Any records that are kept are written to a new intermediate stream.
  - The take operation bundles groups of events before invoking another iteration of the stream. Be careful to specify the within datetime.timedelta argument to this function, otherwise your program may hang.
- Faust provides a number of other operations that you may use when working with your streams. Have a look at the documentation for further information.


### Practice: Processors and Operations ###


```python
from dataclasses import asdict, dataclass
import json
import random

import faust


@dataclass
class ClickEvent(faust.Record):
    email: str
    timestamp: str
    uri: str
    number: int
    score: int = 0


#
# TODO: Define a scoring function for incoming ClickEvents.
#       It doens't matter _how_ you score the incoming records, just perform
#       some modification of the `ClickEvent.score` field and return the value
#
def add_score(clickevent):
    clickevent.score = random.random()
    return clickevent
    

app = faust.App("exercise5", broker="kafka://localhost:9092")
clickevents_topic = app.topic("com.udacity.streams.clickevents", value_type=ClickEvent)
scored_topic = app.topic(
    "com.udacity.streams.clickevents.scored",
    key_type=str,
    value_type=ClickEvent,
)

@app.agent(clickevents_topic)
async def clickevent(clickevents):
    #
    # TODO: Add the `add_score` processor to the incoming clickevents
    #       See: https://faust.readthedocs.io/en/latest/reference/faust.streams.html?highlight=add_processor#faust.streams.Stream.add_processor
    #
    clickevents.add_processor(add_score)
    async for ce in clickevents:
        await scored_topic.send(key=ce.uri, value=ce)

if __name__ == "__main__":
    app.main()

```



# Tables in Faust #



Faust Tables

- [Faust tables are defined with app.Table and take a table name and default type argument.](https://faust.readthedocs.io/en/latest/userguide/tables.html#basics)
Tables must be [co-partitioned with the streams they are aggregating.](https://faust.readthedocs.io/en/latest/userguide/tables.html#id3) Use the group_by operation to ensure co-partitioning.
Tables which are not co-partitioned may lead to inaccurate results.

Example

```python
from dataclasses import asdict, dataclass
import json
import random

import faust


@dataclass
class ClickEvent(faust.Record):
    email: str
    timestamp: str
    uri: str
    number: int


app = faust.App("exercise6", broker="kafka://localhost:9092")
clickevents_topic = app.topic("com.udacity.streams.clickevents", value_type=ClickEvent)

#
# TODO: Define a uri summary table
#
uri_summary_table = app.Table("uri_summary", default=int)


@app.agent(clickevents_topic)
async def clickevent(clickevents):
    #
    # TODO: Group By URI
    #
    async for ce in clickevents.group_by(ClickEvent.uri):
        #
        # TODO: Use the URI as key, and add the number for each click event
        #
        uri_summary_table[ce.uri] += ce.number
        print(f"{ce.uri}: uri_summary_table[ce.uri]")


if __name__ == "__main__":
    app.main()
```


### Windows ###


```python
tumbling_table = table.Tumbling(size=timedelta(minutes=5))

hopping_table = table.Hopping(
  size=timedelta(minutes=5),
  step=timedelta(minutes=1),
  expires=timedelta(minutes=60),
)
```

The `expires` key states for how long should we keep the data.  


In the example, we see the nubmers going up until the time expires. In this case, the counters reset and then starts to go up. 


```python
from dataclasses import asdict, dataclass
from datetime import timedelta
import json
import random

import faust


@dataclass
class ClickEvent(faust.Record):
    email: str
    timestamp: str
    uri: str
    number: int


app = faust.App("exercise7", broker="kafka://localhost:9092")
clickevents_topic = app.topic("com.udacity.streams.clickevents", value_type=ClickEvent)

#
# TODO: Define a tumbling window of 10 seconds
#       See: https://faust.readthedocs.io/en/latest/userguide/tables.html#how-to
#
uri_summary_table = app.Table("uri_summary", default=int).tumbling(
    timedelta(seconds=30)
)


@app.agent(clickevents_topic)
async def clickevent(clickevents):
    async for ce in clickevents.group_by(ClickEvent.uri):
        uri_summary_table[ce.uri] += ce.number
        #
        # TODO: Play with printing value by: now(), current(), value()
        #       See: https://faust.readthedocs.io/en/latest/userguide/tables.html#how-to
        #
        print(f"{ce.uri}: {uri_summary_table[ce.uri].current()}")


if __name__ == "__main__":
    app.main()

```


In the case of **Hopping windows** we could do:

```python
uri_summary_table = app.Table("uri_summary", default=int).hopping(
    size=timedelta(seconds=30),
    step=timedelta(seconds=5),
    expires=timedelta(minutes=10),
)
```

