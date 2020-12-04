### Creating a Table
Creating a table is very similar to creating a Stream. In this demo, you'll learn the syntax and see the handful of small differences between creating Tables and Streams.

#### Managing Offsets
Like all Kafka Consumers, KSQL by default begins consumption at the latest offset. This can be a problem for some scenarios. In the following example we're going to create a pages table -- but -- we want all the data available to us in this table. In other words, we want KSQL to ***start from the earliest offset***. To do this, we will use the SET command to set the configuration variabl auto.offset.reset for our session -- and before we run any commands.

SET `'auto.offset.reset' = 'earliest';`

Also note that this can be set at the KSQL server level, if you'd like.

Once you're done querying or creating tables or streams with this value, you can set it back to its original setting by simply running:

UNSET 'auto.offset.reset';

#### 01. Creating a Table
To create a table, as with a stream, specify a name, the fields, and the source topic

```sql
CREATE TABLE pages
  (uri VARCHAR,
   description VARCHAR,
   created VARCHAR)
  WITH (KAFKA_TOPIC='com.udacity.streams.pages',
        VALUE_FORMAT='JSON',
        KEY='uri');
```
The only new field we have provided here is ***KEY***, which is the string key that ***uniquely identifies our records***. Remember with KSQL TABLEs we will keep track of the latest value for a given key, not all values we have ever seen for a key.

#### 02. Creating a Table from a Query
Tables, like Streams, may also be derived from queries. Lets create a Table of all pages whose url starts with the letter a.


```sql
CREATE TABLE a_pages AS
  SELECT * FROM pages 
  WHERE uri LIKE 'http://www.a%';
```
#### 03. Describing Tables and Streams
KSQL can provide a lot of valuable information to us with the DESCRIBE command:


ksql> DESCRIBE pages;

Name                 : PAGES
 Field       | Type
-----------------------------------------
 ROWTIME     | BIGINT           (system)
 ROWKEY      | VARCHAR(STRING)  (system)
 URI         | VARCHAR(STRING)
 DESCRIPTION | VARCHAR(STRING)
 CREATED     | VARCHAR(STRING)
-----------------------------------------
For runtime statistics and query details run: DESCRIBE EXTENDED <Stream,Table>;
This command is useful for understanding what columns and column types are defined on your tables.

Deleting a Table
As with Streams, we must first find the running underlying query, and then drop the table.

First, find your query:


ksql> SHOW QUERIES;

 Query ID                | Kafka Topic      | Query String
----------------------------------------------------------------------------------------------
  CTAS_A_PAGES_1      | A_PAGES      | CREATE TABLE a_pages AS
    SELECT * FROM pages WHERE uri LIKE 'http://www.a%';
----------------------------------------------------------------------------------------------
For detailed information on a Query run: EXPLAIN <Query ID>;
Find your query, which in this case is CTAS_A_PAGES_1

#### 04. TERMINATE the query and DROP the table
and then, finally, TERMINATE the query and DROP the table:

```
TERMINATE QUERY CTAS_A_PAGES_1;
DROP TABLE A_PAGES;
```