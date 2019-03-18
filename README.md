# Project: Logs Analysis

This program is a reporting tool that analyzes data from an articles database. It will attempt to answer the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## Design
For each of the above questions above there is a corresponding function that queries the `news` database, the results of which are printed out to the console. See **output.txt** for an example of the output.

These functions make use of custom views that were created to facilitate the querying of data. The two views created were `article_logs` and `daily_error_count`. These need to be created on your database instance before running the program.

## Setup
Create the following views on your instance of the `news` database before executing the program.
### article_logs
```
create view article_logs as
select title, slug, author, log.time, status
  from articles join log on articles.slug = split_part(log.path, '/', 3);
```

### daily_error_count
```
create view daily_error_count as
select time::date, count(*) as log_count, max(log_error_counts.log_error_count) as error_count
  from log join (select time::date as log_date, count(*) as log_error_count from log where status != '200 OK' group by time::date) as log_error_counts
  on log.time::date = log_error_counts.log_date
  group by time::date;
```

## Executing

Python Version:
> python2.7

Command Line:
```
$ python logs_analysis.py
```

Output:
```
most popular three articles of all time
"Candidate is jerk, alleges rival" - 338647 views
"Bears love berries, alleges bear" - 253801 views
"Bad things gone, say good people" - 170098 views


most popular authors of all time
Ursula La Multa - 507594 views
Rudolf von Treppenwitz - 423457 views
Anonymous Contributor - 170098 views
Markoff Chaney - 84557 views


days with more than 1% request errors
July 17, 2016 - 2.3% errors


```