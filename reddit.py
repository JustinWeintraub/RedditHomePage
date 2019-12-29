import mysql.connector
import praw
from datetime import date
import json
import os
reddit = praw.Reddit(client_id=os.environ.get('client_id'), #based on environment variables
                     client_secret=os.environ.get('client_secret'), user_agent=os.environ.get('user_agent'))

with open('subreddits.json', 'r') as file:
  subreddits = json.loads(file.read())['subreddits']

def getConnection():
  return(
    mysql.connector.connect(host=os.environ.get('host'), #based on environment variables
                                     port=3306,
                                     user=os.environ.get('user'),
                                     password=os.environ.get('password'),
                                     database=os.environ.get('database'),
                                     auth_plugin='mysql_native_password'
                                     )
  )
def createData(day):
  connection = getConnection()
  cursor = connection.cursor(buffered=True)
  for subreddit in subreddits:
    for submission in reddit.subreddit(subreddit).hot(limit=10):
      url=submission.url
      #if(submission.url[8]=="v"):
      #  url = submission.media['reddit_video']['fallback_url']
      #  url = url.split("?")[0]
      insert = ('''INSERT INTO reddit.posts
      VALUES('{}','{}', '{}', {}, '{}',{})
      ''').format(submission.title.replace("'", ""), "https://reddit.com"+submission.permalink, subreddit, submission.score, day, "'"+submission.url+"'" if not submission.is_self else 'NULL')
      cursor.execute(insert)
  cursor.close()
  connection.commit()
  connection.close()
def createDatabase(day):
  connection = getConnection()
  cursor = connection.cursor(buffered=True)
  cursor.execute('''CREATE TABLE posts(
  Title varchar(1000),
  Link varchar(1000),
  Subreddit varchar(100),
  Upvotes int(11),
  Date varchar(100),
  ImageLink varchar(1000)
  ) ''')
  cursor.close()
  connection.commit()
  connection.close()

def getDatabase(day):
  connection = getConnection()
  cursor = connection.cursor(buffered=True)
  try:
    cursor.execute(('''SELECT * FROM reddit.posts 
                    WHERE DATE = '{}'
                    ORDER BY RAND()
                    ''').format(day))
    cursor.close()
    connection.commit()
    connection.close()
    if(cursor.rowcount==0):
      if(str(day.replace("/","-"))!= str(date.today())):
        return
      createData(day)
    else: 
      return cursor
    return(getDatabase(day))
  except:
    createDatabase(day)
    return(getDatabase(day))
  



