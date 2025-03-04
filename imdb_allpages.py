import pandas as pd
import numpy as np
import time
from IPython.core.pylabtools import figsize
from IPython.display import HTML
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
import json
plt.style.use('fivethirtyeight')

TOKEN = 'eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYWEyNWIwZTA1OTg1N2VkYTUyZjdmN2U3MjgyMjFkZCIsIm5iZiI6MTc0MDc3MjY5NC44MDMsInN1YiI6IjY3YzIxNTU2MDlhOWI4NDk2ZGRiZDVhOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.bSQWWII0aRK_8SEn3qV7CxrNsJcyj2WJ05JugOHpki8'
API_KEY = 'caa25b0e059857eda52f7f7e728221dd'

def make_call(url):
    response = requests.get(url, headers={'Authorization': 'Bearer ' + TOKEN})
    return (response, response.json())

def date_search(date_range):
    #initial url
    url = f"https://api.themoviedb.org/3/discover/movie?&include_adult-true&primary_release_date.gte={date_range[0]}&primary_release_date.lte={date_range[1]}"
    #call for page1
    page1 = make_call(url)
    #check number of pages
    pages = page1[1]['total_pages']
    #create master list
    list_of_responses = page1[1]['results']
    #declare range
    page_range = range(2, pages+1)
    #for loop to iterate through the range
    for current_page in page_range:
        #declare paginated URL
        paginated_url = f"https://api.themoviedb.org/3/discover/movie?&include_adult-true&primary_release_date.gte={date_range[0]}&primary_release_date.lte={date_range[1]}&page={current_page}"
        #make call
        current_page_response = make_call(paginated_url)
        #print(paginated_url)
        #check response status
        if str(current_page_response[0]) == '<Response [200]>':
            #add response to master list
            list_of_responses.extend(current_page_response[1]['results'])
        else:
            print(current_page_response[0])
            print(paginated_url)
            print(current_page_response)
            break
        #wait 20ms
        time.sleep(0.01)
        #loop
    #return master list
    return list_of_responses