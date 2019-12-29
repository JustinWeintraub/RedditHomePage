from flask import Flask, render_template, Markup
from reddit import *
import datetime

app = Flask(__name__)

@app.route('/', defaults={'day': None})
@app.route('/<day>')
def index(day):
  today = date.today()
  try:
    datetime.datetime.strptime(day, '%Y-%m-%d')
    day=day.replace("-","/")
  except:
    day=today.strftime("%Y/%m/%d")
  data = convertDataToHtml(getDatabase(day)) #gets data from reddit.py, then converts it
  day=day.replace("/","-")
  return render_template('page.html', day=day, data=data)

def convertDataToHtml(data):
  send = ""
  if(data):
    for row in data:
      send += '''<h1 style="margin-top:5%; margin-bottom:-1%;"><a href="{}" style="text-decoration: none; color:white;" > {}</a></h1>'''.format(row[1], row[0]) #Link, title
      send +='''<h3> {}, {} upvotes </h3>'''.format(row[2], row[3]) #Subreddit, upvotes
      if(row[5]!=None):
        if(row[5][8]=="i"):
          send += '''<img style="width:20%;" src="{}">'''.format(row[5]) #Image url
        else:
          send += '''<h3>Submission not an image </h3>'''

  else:
    send +='''<h1> Data for this day does not exist. </h1>'''
  return Markup(send)