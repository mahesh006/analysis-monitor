import datetime
from expertai.nlapi.common.model import sentiment
from flask import Flask, render_template, request
from re import search
import tweepy
import os
import json
import requests
import re
from bs4 import BeautifulSoup
import database

os.environ["EAI_USERNAME"] = 'pitabi1360@pashter.com'
os.environ["EAI_PASSWORD"] = 'Testqwerty1!'

access_token = "1404336950379618307-bzj0qCKWCGxFhTLZHCcICvNKR3iSwA"
access_token_secret = "spt4yEqwtbkobpzkooBpXKwlABGQTkd7BF1ktiVkJ4TF4"

api_key = "TMiH233R2PvUpnKeXLWR0L1C9"
api_key_secret = "p89DmUnP2oyxdqLJfzkaROjR3H1a1VEjPu4Nf68Ie6ZqkMqkM7"

from expertai.nlapi.cloud.client import ExpertAiClient
client = ExpertAiClient()
import os

app = Flask(__name__)

database.create_tables()

auth = tweepy.OAuthHandler(consumer_key=api_key,consumer_secret=api_key_secret)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)



language= 'en'




@app.route("/", methods=["GET", "POST"])
def home():
    negative=[]
    positive=[]
    neutral=[]
    review=[]
    neg=[]
    comnam=[]

    
        
    if request.method == "POST":
        database.delete_entries()
        entry_content = request.form.get("content")
        r = requests.get(entry_content)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.findAll('p', {'class':re.compile('.*comment.*')})
        reviews = [result.text for result in results]

        result = soup.findAll('h1', attrs={'class':'css-11q1g5y'})
        name = [results.text for results in result]
        comnam.append(name)

        
        for info in reviews:            
            output = client.specific_resource_analysis(body={"document": {"text":  info}}, params={'language': language, 'resource': 'sentiment'})
            review.append(info)
            database.create_entry(info, datetime.datetime.today().strftime("%b %d"), output.sentiment.overall)
            
            if output.sentiment.overall>0:
                positive.append(info)
            elif output.sentiment.overall<0:
                negative.append(info)
                document = client.specific_resource_analysis(body={"document": {"text": info}}, params={'language': language, 'resource': 'relevants'})
                for mainlemma in document.main_lemmas:
                    neg.append(mainlemma.value)

            else:
                neutral.append(output.sentiment.overall)           
 
    return render_template("dashboard1.html", positive=json.dumps(positive), negative=json.dumps(negative), neutral=json.dumps(neutral), neg=neg, reviews=review, comnam=json.dumps(comnam))

@app.route("/AmazonReviews", methods=["GET", "POST"])
def AmazonReviews():
    negative=[]
    positive=[]
    neutral=[]
    review=[]
    neg=[]
     
        
    if request.method == "POST":

        entry_content = request.form.get("content")
        r = requests.get(entry_content)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.findAll('span', attrs={'data-hook':'review-body'})
        reviews = [result.text for result in results]
        
        for info in reviews:            
            output = client.specific_resource_analysis(body={"document": {"text":  info}}, params={'language': language, 'resource': 'sentiment'})
            review.append(info)
            
            if output.sentiment.overall>0:
                positive.append(info)
            elif output.sentiment.overall<0:
                negative.append(info)
                document = client.specific_resource_analysis(body={"document": {"text": info}}, params={'language': language, 'resource': 'relevants'})
                for mainlemma in document.main_lemmas:
                    neg.append(mainlemma.value)

            else:
                neutral.append(output.sentiment.overall)           
 
    return render_template("AmazonReviews.html", positive=json.dumps(positive), negative=json.dumps(negative), neutral=json.dumps(neutral), neg=neg, reviews=review)


@app.route("/Twitter-Search", methods=["GET", "POST"])
def Yelp():

    tweet=[]
    sentiment=[]
    positive=[]
    negative=[]
    neutral=[]
    
    if request.method == "POST":
        entry_content = request.form.get("content")
        tweets = tweepy.Cursor(api.search,q=entry_content).items(3)

        for info in tweets:
            tweet.append(info.text)
            output = client.specific_resource_analysis(body={"document": {"text":  info.text}}, params={'language': language, 'resource': 'sentiment'})
            sentiment.append(output.sentiment.overall)
            if output.sentiment.overall>0:
                positive.append(output.sentiment.overall)
            elif output.sentiment.overall<0:
                negative.append(output.sentiment.overall)
            else:
                neutral.append(output.sentiment.overall)

 
    return render_template("TwitterSearch.html", positive=json.dumps(len(positive)), negative=json.dumps(len(negative)), neutral=json.dumps(len(neutral)), tweet=tweet)


@app.route("/Dashboard", methods=["GET", "POST"])
def Dashboard():
    tweet=[]
    dates=[]
    sentiment=[]
    positive=[]
    negative=[]
    neutral=[]

    if request.method == "POST":
        entry_content = request.form.get("content")
        tweets = api.user_timeline(screen_name=entry_content, count=4, include_rts = False, tweet_mode = 'extended')
        
        for info in tweets:
            tweet.append(info.created_at)
            print(info.created_at)
            dates.append(info.full_text)
            print(info.full_text)
            output = client.specific_resource_analysis(body={"document": {"text":  info.full_text}}, params={'language': language, 'resource': 'sentiment'})
            sentiment.append(output.sentiment.overall)
            if output.sentiment.overall>0:
                positive.append(output.sentiment.overall)
            elif output.sentiment.overall<0:
                negative.append(output.sentiment.overall)
            else:
                neutral.append(output.sentiment.overall)
            print(output.sentiment.overall)
            print("\n")
            print(len(positive))
 
    return render_template("Dashboard.html", positive=json.dumps(len(positive)), negative=json.dumps(len(negative)), neutral=json.dumps(len(neutral)))





@app.route("/compare", methods=["GET", "POST"])
def Compare():
    negative=[]
    positive=[]
    neutral=[]
    review=[]
    neg=[]
    
    
    if request.method == "POST":
        entry_content = request.form.get("content")
        r = requests.get(entry_content)
        soup = BeautifulSoup(r.text, 'html.parser')
        results = soup.findAll('p', {'class':re.compile('.*comment.*')})
        reviews = [result.text for result in results]

        result = soup.findAll('h1', attrs={'class':'css-11q1g5y'})
        review = [result.text for result in result]
        
        for info in reviews:            
            output = client.specific_resource_analysis(body={"document": {"text":  info}}, params={'language': language, 'resource': 'sentiment'})
            review.append(info)    
            if output.sentiment.overall>0:
                positive.append(output.sentiment.overall)
            elif output.sentiment.overall<0:
                negative.append(output.sentiment.overall)
            else:
                neutral.append(output.sentiment.overall)  
    entries=database.retrieve_entries()
    return render_template("competative_analysis.html", data=json.dumps(entries),positive=json.dumps(len(positive)), negative=json.dumps(len(negative)), neutral=json.dumps(len(neutral)), neg=neg, reviews=review, entries=entries)


