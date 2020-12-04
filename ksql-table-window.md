### Hopping and Tumbling Windows
In this demonstration we'll see how to create Tables with windowing enabled.

#### 01. Tumbling Windows
Let's create a tumbling clickevents table, where the window size is 30 seconds.


```sql
CREATE STREAM clickevents_tumbling AS
  SELECT * FROM clickevents
  WINDOW TUMBLING (SIZE 30 SECONDS);
```

#### 02. Hopping Windows
Now we can create a Table with a hopping window of 30 seconds with 5 second increments.

```sql
CREATE TABLE clickevents_hopping AS
  SELECT uri FROM clickevents
  WINDOW HOPPING (SIZE 30 SECONDS, ADVANCE BY 5 SECONDS)
  WHERE uri LIKE 'http://www.b%'
  GROUP BY uri;
```

The above window is 30 seconds long and advances by 5 second. If you query the table you will see the associated window times!

#### 03. Session Windows
Finally, lets see how session windows work. We're going to define the session as 5 minutes in order to group many events to the same window


```sql
CREATE TABLE clickevents_session AS
  SELECT uri FROM clickevents
  WINDOW SESSION (5 MINUTES)
  WHERE uri LIKE 'http://www.b%'
  GROUP BY uri;
```