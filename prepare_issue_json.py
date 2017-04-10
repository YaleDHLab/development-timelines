from __future__ import division
from pytz import timezone
from datetime import datetime, timedelta
import json, time

# try python 2, fallback to 3
try:
  from urllib2 import urlopen, Request
except:
  from urllib.request import urlopen, Request

def get_config():
  '''Return a config object'''
  with open('config.json') as f:
    return json.load(f)

def get_issues():
  '''Return issues json'''
  if config['use_saved_issue_json'] == '1':
    issues = load_json('issue-data.json')

  else:
    issues = request_issues(config['repo'], [])
    save_json('issue-data.json', issues)

  return issues

def request_issues(url, issues):
  '''Make a request for issues and return the response'''
  request = Request(url)
  request.add_header('Referer', 'http://google.com')
  request.add_header('Authorization', 'token ' + config['access_token'])
  response = urlopen(request)
  parsed_response = json.loads(response.read())
  issues = issues + parsed_response

  # get all pages of results
  try:
    link = response.info().getheader('Link') # python 2
  except:
    link = response.getheader('Link') # python 3

  if link:
    get_response()
  else:
    return issues

def save_json(path, obj):
  '''Write issue json to disk'''
  with open(path, 'w') as out:
    json.dump(obj, out)

def load_json(path):
  '''Return saved issue json'''
  with open(path) as f:
    return json.load(f)

def get_current_datetime():
  '''Return the current date'''
  tz = timezone(config['timezone'])
  return datetime.now(tz)

def get_initial_datetime():
  '''Return January 1 2017'''
  return datetime(2017, 1, 1, 1, 1, 1, 1)

def dt_to_js_time(d):
  '''Read in a datetime.datetime object and return that object in js time'''
  return time.mktime(d.timetuple()) * 1000

def get_chart_row(idx, label, start_time, end_time):
  '''Return a row of json for the chart'''
  return [
    str(idx),
    label,
    dt_to_js_time(start_time),
    dt_to_js_time(end_time)
  ]

def prepare_chart_json(issues):
  '''Prepare the json required by the timeline chart'''
  current_schedule_time = get_initial_datetime()
  scalar = 3 # see below
  chart_rows = []
  issue_idx = 0

  # make issues last in last out
  issues.reverse()

  for i in issues:
    title = i['title']
    number = i['number']
    body = i['body']
    issue_number = str(i['number'])

    try:
      first_label = i['labels'][0]['name']
    except:
      first_label = 'unlabeled'

    # time estimates are registered in issue titles, e.g.: "6 - Glossary view"
    split_title = title.split(' ')
    if split_title[1] == '-':
      hours = int(split_title[0])
      title = issue_number + ': ' + ' '.join(split_title[2:])

      # it will confuse users to see gaps for non-work hours in the chart, so
      # scale the 8 hour work day to fit within a 24 hour frame by multiplying
      # time estimates by 3
      start_time = current_schedule_time
      end_time = current_schedule_time + timedelta(hours=hours * scalar)
      
      # munge this row of data into the required format
      chart_row = get_chart_row(first_label, title, start_time, end_time)
      chart_rows.append(chart_row)

      current_schedule_time += timedelta(hours=hours * scalar)
      issue_idx += 1

  return chart_rows

if __name__ == '__main__':
  
  # get the inputs
  config = get_config()
  issues = get_issues()

  # prepare the chart json
  chart_rows= prepare_chart_json(issues)

  # save the chart json
  save_json('chart-data.json', chart_rows)
  