import boto3
import json
import pandas as pd
import html_to_json
import requests
import urllib.request
from bs4 import BeautifulSoup
from datetime import date



def handler(event, context):

   
   today = date.today()
   year = str(today.year)
   month = str(today.month)
   day = str(today.day)
   bbc_name = "bbc"
   cnn_name = "UltimaHoraCol"

   directory_periodic_bbc = "/headlines/raw/periodico="+bbc_name+"/year="+year+"/month="+month+"/day="+day
   directory_periodic_cnn = "/headlines/raw/periodico="+cnn_name+"/year="+year+"/month="+month+"/day="+day
   directory_search_bbc = "/headlines/raw/periodico="+bbc_name+"/year="+year+"/month="+month+"/day="+day+"/bbc_news.html"
   directory_search_cnn = "/headlines/raw/periodico="+cnn_name+"/year="+year+"/month="+month+"/day="+day+"/cnn_news.html"
   s3 = boto3.resource('s3')
   
   try:
        # Get the uploaded file's information
        bucket = event['Records'][0]['s3']['bucket']['zappa-g8rvvmpli'] # Will be my-bucket
        key = event['Records'][0]['s3']['object'][directory_search_bbc] # Will be the file path of whatever file was uploaded.
        key2 = event['Records'][0]['s3']['object'][directory_search_cnn] 
        # Get the bytes from S3
        #s3.download_file(bucket, key, '/tmp/' + key) # Download this file to writable tmp space.
        #file_bytes = open('/tmp/' + key).read()
   except:
        bucket = []
        key = []

   content_object = s3.Object('zappa-g8rvvmpli', directory_search_bbc)
   file_content = content_object.get()['Body'].read()
   print(file_content)

   content_object_ = s3.Object('zappa-g8rvvmpli', directory_search_cnn)
   file_content_ = content_object_.get()['Body'].read()   
   
    
   soup = BeautifulSoup(file_content, 'html.parser')
   section_items = soup.find_all('section')
   bbc_news_data = []

   alfa_header = []
   alfa_category = []
   alfa_href = []

   for i_section in section_items:
      header = i_section.find(class_='media__title')
      alfa_header.append(str(header).split("\n"))
      category = i_section.find(class_='media__tag tag tag--news')
      alfa_category.append(str(category).split(">"))
      href = i_section.find(class_='media__link')
      alfa_href.append(str(href).split('"'))

   href = []
   for i in alfa_href:
      if i[0] != 'None':  
        href.append(i[3])
      else:
        href.append("null")

   category = []
   for i in alfa_category:
      if i[0] != 'None':
        category.append(i[1].split("<")[0])
      else:
        category.append("null")

   header = []
   for key, i in enumerate(alfa_header):
      if i[0] != 'None':
        #a = i.split("\t")
        alfa_text = i[2].split("</a>")
        a21 = alfa_text[0].strip()
        header.append(a21)
      else:
        header.append("null")

   bbc_news_data = {"title":header, "category":  category, "href":href}
   df =  pd.DataFrame.from_dict(bbc_news_data)
   #bbc_news_dat =  ",".join(header)+",".join(category)+",".join(href)
   #bbc_news_data = [bbc_news_dat]
   #df =  pd.DataFrame(bbc_news_data)
   csv = df.to_csv(index = False, sep=",")

   s3Object_1 = s3.Object('zappa-3z24biloe',directory_periodic_bbc+'/bbc_news.csv')
   s3Object_1.put(
        Body=csv
   )


   soup = BeautifulSoup(file_content_, 'html.parser')
   section_items_ = soup.find_all('body')

   tag = soup.body
   alfa_title = []
   alfa_category = []
   alfa_link = []
   count = 0
   for i in tag.descendants:
      if type(i) == "NavigableString":
        continue
      else:
        if i.name == "a":
           count = len(i.text.strip().split("\t")[0])
           #alfa_link.append(i["href"])
           if count > 15:
              titulo,link, categoria = i.text.strip().split("\t")[0], i["href"], i.text.strip().split("\n")[0]
              alfa_title.append(titulo)
              alfa_link.append(link)
              alfa_category.append(categoria)

   cnn_news_data = {"title":alfa_title,"category": alfa_category, "href":alfa_link}
   df_ =  pd.DataFrame.from_dict(cnn_news_data)

   #cnn_news_dat = ",".join(alfa_title)+",".join(alfa_category)+",".join(alfa_link)
   #cnn_news_data = [cnn_news_dat]
   #df_ =  pd.DataFrame(cnn_news_data)
   csv_ = df_.to_csv(index = False, sep=",")

   s3Object_1 = s3.Object('zappa-3z24biloe',directory_periodic_cnn+'/cnn_news.csv')
   s3Object_1.put(
        Body=csv_
   )

   return {}
