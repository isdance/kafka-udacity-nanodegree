
### Creating a Stream
In this demonstration you'll learn a few ways to create a KSQL Stream. Once you've created your stream, you'll also see how to delete them.

Throughout this lesson we will refer to two topics:

com.udacity.streams.clickevents
com.udacity.streams.pages
com.udacity.streams.pages has the following data shape:

Key: <uri: string> Value: ``` { "uri": , "description": , "created": , }


`com.udacity.streams.clickevents` has the following data shape:

**Key**: `<uri: string>`
**Value**: ```
{
  "email": <string>,
  "timestamp": <string>,
  "uri": <string>,
  "number": <int>
}

#### 01. Showing Topics
The first step is to open the KSQL CLI.


root@c9827c86286f:/home/workspace# ksql

                  ===========================================
                  =        _  __ _____  ____  _             =
                  =       | |/ // ____|/ __ \| |            =
                  =       | ' /| (___ | |  | | |            =
                  =       |  <  \___ \| |  | | |            =
                  =       | . \ ____) | |__| | |____        =
                  =       |_|\_\_____/ \___\_\______|       =
                  =                                         =
                  =  Streaming SQL Engine for Apache Kafka® =
                  ===========================================

Copyright 2017-2018 Confluent Inc.

CLI v5.1.3, Server v5.1.3 located at http://localhost:8088

Having trouble? Type 'help' (case-insensitive) for a rundown of how things work!

ksql>
With the CLI Open, lets now see what Kafka Topics we have available to us:


ksql> SHOW TOPICS;

 Kafka Topic                     | Registered | Partitions | Partition Replicas | Consumers | ConsumerGroups
-------------------------------------------------------------------------------------------------------------
 _confluent-metrics              | false      | 12         | 1                  | 0         | 0
 _schemas                        | false      | 1          | 1                  | 0         | 0
 com.udacity.streams.clickevents | false      | 1          | 1                  | 0         | 0
 com.udacity.streams.pages       | false      | 1          | 1                  | 0         | 0
 connect-configs                 | false      | 1          | 1                  | 0         | 0
 connect-offsets                 | false      | 25         | 1                  | 0         | 0
 connect-status                  | false      | 5          | 1                  | 0         | 0
-------------------------------------------------------------------------------------------------------------
you can see the two topics we're interested in -- com.udacity.streams.clickevents and com.udacity.streams.pages.

####  02. Creating Streams
Next, we're going to create a stream for ClickEvents.

```sql
CREATE STREAM clickevents
  (email VARCHAR,
   timestamp VARCHAR,
   uri VARCHAR,
   number INTEGER)
  WITH (KAFKA_TOPIC='com.udacity.streams.clickevents',
        VALUE_FORMAT='JSON');
```
Viewing available streams
We can see all available streams by running the SHOW STREAMS command


ksql> SHOW STREAMS;

 Stream Name | Kafka Topic                     | Format
-------------------------------------------------------
 CLICKEVENTS | com.udacity.streams.CLICKEVENTS | JSON
-------------------------------------------------------

### 03. Create a Stream with a Query
KSQL Also allows for the creation of Streams derived from queries.

```sql
CREATE STREAM popular_uris AS
  SELECT * FROM clickevents
  WHERE number >= 100;
```
This would create a stream with clickevents with more than or equal to 100 interactions

#### 04. Deleting a Stream
Finally, lets see how we can delete a stream.


DROP STREAM popular_uris;
You will immediately receive an error like the following:


ksql> DROP STREAM popular_uris;
Cannot drop POPULAR_URIS.

The following queries read from this source: [].
The following queries write into this source: [CSAS_POPULAR_URIS_0].

You need to terminate them before dropping POPULAR_URIS.
Under the covers KSQL is running a query to populate this stream. We first need to terminate that query before we can terminate the stream.


TERMINATE QUERY CSAS_POPULAR_URIS_0;
DROP STREAM popular_uris;
Now we have successfully terminated the underlying query and terminated the stream!

Topic Management
In this demonstration, we created two streams -- popular_uris and clickevents.

If we SHOW TOPICS; we'll notice a few interesting things:


ksql> SHOW TOPICS;

 Kafka Topic                     | Registered | Partitions | Partition Replicas | Consumers | ConsumerGroups
-------------------------------------------------------------------------------------------------------------
 _confluent-metrics              | false      | 12         | 1                  | 0         | 0
 _schemas                        | false      | 1          | 1                  | 0         | 0
 com.udacity.streams.clickevents | true       | 10         | 1                  | 0         | 0
 com.udacity.streams.pages       | false      | 10         | 1                  | 0         | 0
 connect-configs                 | false      | 1          | 1                  | 0         | 0
 connect-offsets                 | false      | 25         | 1                  | 0         | 0
 connect-status                  | false      | 5          | 1                  | 0         | 0
 POPULAR_URIS                    | false      | 4          | 1                  | 0         | 0
-------------------------------------------------------------------------------------------------------------
First, POPULAR_URIS topic has been created and is still present. By default, this is how KSQL behaves. If you'd like to clean up the topic you need to do it manually. Second, why was a POPULAR_URIS topic created, but not one for the stream CLICKEVENTS? POPULAR_URIS actually required modification to the data, so, an intermediate topic was created. CLICKEVENTS, however, required no modification, so the underlying topic is used as-is.