import html_to_json
import requests
import urllib.request
import json
import boto3
from bs4 import BeautifulSoup
from datetime import date

def handler(event, context):
 
  s3 = boto3.resource('s3')
  #page = requests.get('https://www.bbc.com/')
  #soup = BeautifulSoup(page.text, 'html.parser')
  #section_items = soup.find_all('html')
  today = date.today()
  year = str(today.year)
  month = str(today.month)
  day = str(today.day)
  
  #directory_periodic = "/headlines/raw/periodico/year="+year+"/month="+month+"/day="+day
  bbc_name = "bbc"
  cnn_name = "UltimaHoraCol"

  directory_periodic_bbc = "/headlines/raw/periodico="+bbc_name+"/year="+year+"/month="+month+"/day="+day
  directory_periodic_cnn = "/headlines/raw/periodico="+cnn_name+"/year="+year+"/month="+month+"/day="+day


  #bbc_news = urllib.request.urlopen("https://www.bbc.com/").read()
  #cnn_news = urllib.request.urlopen("https://edition.cnn.com/").read()
 
  bbc_news  = requests.get('https://www.bbc.com/')
  cnn_news = requests.get('https://ultimahoracol.com/')
  #bbc_news = html_to_json.convert(bbc_news_)
  #cnn_news = html_to_json.convert(cnn_new_)
  #page_bbc = json.dumps(output_json)
  #page_cnn = json.dumps(output_json_2)
  #contents_2 = urllib.request.urlopen("https://edition.cnn.com/").read()
  #bbc_news = json.loads()
  #cnn_news = json.loads(contents_2)
 
  s3Object_1 = s3.Object('zappa-g8rvvmpli',directory_periodic_bbc+'/bbc_news.html')
  s3Object_1.put(
        Body=bbc_news.content

  )
  s3Object = s3.Object('zappa-g8rvvmpli', directory_periodic_cnn+'/cnn_news.html')
  s3Object.put(
        Body=cnn_news.content
  )
  

  return {}
