### Querying in KSQL
Ad-hoc querying in KSQL is one of the tools greatest strengths. Lets have a look at some sample queries.

#### 01. Basic filtering
We've already seen how to filter data in the table creation process, but lets revisit it one more time


```sql
SELECT uri, number
  FROM clickevents
  WHERE number > 100
    AND uri LIKE 'http://www.k%';
```

#### 02. Scalar Functions
KSQL Provides a number of Scalar functions for us to make use of.

Lets write a function that takes advantage of some of these features:


```sql
SELECT UCASE(SUBSTRING(uri, 12))
  FROM clickevents
  WHERE number > 100
    AND uri LIKE 'http://www.k%';
```

This query will strip the http://www. from the start of the URI and capitalize it.

The SUBSTRING function takes a string and which character to start at (and optionally end at) The UCASE function takes a string and capitalizes it.

#### 03. Terminating Queries
SELECT queries are not persistent!

Notice that as soon as you hit CTRL+C your query ends. When you run the query again, KSQL has to recreate the query. This means that if you want the results of this query to be persistent, you need to create a Table or a Stream to persist your queries for long-term usage.