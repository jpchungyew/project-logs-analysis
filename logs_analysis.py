#!/usr/bin/env python2.7

import psycopg2
import datetime

DB_NAME = "news"


def get_most_popular_articles():
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(
      "select "
      "title"
      ", count(*) as views "
      "from article_logs "
      "group by title, slug "
      "order by views desc "
      "limit 3"
    )
    results = c.fetchall()
    db.close()
    return results


def get_most_popular_authors():
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(
      "select "
      "max(authors.name) as author"
      ", count(*) as views "
      "from article_logs join authors on article_logs.author = authors.id "
      "group by author "
      "order by views desc "
    )
    results = c.fetchall()
    db.close()
    return results


def get_days_with_most_errors():
    db = psycopg2.connect(database=DB_NAME)
    c = db.cursor()
    c.execute(
      "select "
      "time as date "
      ", round((error_count*1.0/log_count)*100,1) as error_percentage "
      "from daily_error_count "
      "where (error_count*1.0/log_count)*100 > 1; "
    )
    results = c.fetchall()
    db.close()
    return results


def print_results(result):
    for row in result:
        print str(row[0]) + " - " + str(row[1])


print("most popular three articles of all time")
articles = get_most_popular_articles()
for row in articles:
    print "\"" + row[0] + "\"" + " - " + str(row[1]) + " views"
print("\n")

print("most popular authors of all time")
authors = get_most_popular_authors()
for row in authors:
    print row[0] + " - " + str(row[1]) + " views"
print("\n")

print("days with more than 1% request errors")
days = get_days_with_most_errors()
for row in days:
    print row[0].strftime("%B %d, %Y") + " - " + str(row[1]) + "% errors"
print("\n")
