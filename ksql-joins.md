### KSQL JOINs
KSQL also supports JOIN operations. In this demonstration you will see how to join the clickevents stream to the pages table.

Before we move on, its worth remember that we cannot JOIN a Table to a Stream, me way only join a Stream to a Table (stream: left, table: right), and Stream to a Table joins always produce new Streams, not Tables.

#### 01. LEFT OUTER JOIN
In KSQL, as with most SQL derivatives, the default JOIN is the LEFT OUTER JOIN.

Let's perform a LEFT OUTER JOIN, or simply, JOIN on clickevents to pages.


```sql
CREATE STREAM clickevent_pages AS
  SELECT ce.uri, ce.email, ce.timestamp, ce.number, p.description, p.created
  FROM clickevents ce
  JOIN pages p on ce.uri = p.uri;
```

#### 02. INNER JOIN
KSQL also supports INNER JOIN between Streams and Tables


```sql
CREATE STREAM clickevent_pages_inner AS
  SELECT ce.uri, ce.email, ce.timestamp, ce.number, p.description, p.created
  FROM clickevents ce
  INNER JOIN pages p on ce.uri = p.uri;
```

#### 03. FULL OUTER JOIN
Alright, lets wrap up by trying KSQLs final supported JOIN operation, the FULL OUTER JOIN


```sql
CREATE STREAM clickevent_pages_outer AS
  SELECT ce.uri, ce.email, ce.timestamp, ce.number, p.description, p.created
  FROM clickevents ce
  FULL OUTER JOIN pages p on ce.uri = p.uri;
```

The query will fail to run:

> Full outer joins between streams and tables (stream: left, table: right) are not supported.

KSQL only supports FULL OUTER JOIN when joining a Table to a Table or a _Stream to a Stream.