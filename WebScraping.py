#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


l=[]
base_url='http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s='

for page in range(0,30,10):
    link=base_url+str(page)+'.html'
    r = requests.get(link, 
                     headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})

    soup = BeautifulSoup(r.text)

    all=soup.find_all("div",{"class":"propertyRow"})

    all[0].find('h4',{"class":"propPrice"}).text.replace('\n','').replace(' ','')


    for item in all:
        d={}
        d['Price']=item.find('h4',{'class':"propPrice"}).text.replace('\n','').replace(' ','')
        d['Address']=item.find_all('span',{'class':'propAddressCollapse'})[0].text
        d['Locality']=item.find_all('span',{'class':'propAddressCollapse'})[1].text
        try:
            d['Beds']=item.find('span',{'class':'infoBed'}).text
        except:
            d['Beds']=None

        try:
            d['Area']=item.find('span',{'class':'infoSqFt'}).text
        except:
            d['Area']=None

        try:
            d['Half Baths']=item.find('span',{'class':'infoValueHalfBath'}).text
        except:
            d['Half Baths']=None

        try:
            d['Full Baths']=item.find('span',{'class':'infoValueFullBath'}).text
        except:
            d['Full Baths']=None

        for column_group in item.find_all('div',{'class':'columnGroup'}):
            # print(column_group)
            for feature_group, feature_name in zip(column_group.find_all('span',{'class':'featureGroup'}), column_group.find_all('span',{'class':'featureName'})):
                # print(feature_group.text, feature_name.text)
                if 'Lot Size' in feature_group.text:
                    d['Lot Size']=feature_name.text
        l.append(d) 


df=pd.DataFrame(l)

df

