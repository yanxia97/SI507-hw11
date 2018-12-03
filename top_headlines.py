from flask import Flask, render_template
from secrets import *
import requests
import time

app = Flask(__name__)

@app.route('/')
def index():    
    return '<h1>Welcome!</h1>'

# part 2
# gets stories from a particular section of NY times
def get_stories(section):
    baseurl = 'https://api.nytimes.com/svc/topstories/v2/'
    extendedurl = baseurl + section + '.json'
    params={'api-key': nyt_key}
    return requests.get(extendedurl, params).json()

def get_headlines(nyt_results_dict, num):
    results = nyt_results_dict['results']
    headlines = []
    for i,r in enumerate(results):
        if i < num:
            headlines.append(r['title']+" ("+r['url']+")")
    return headlines

def get_greeting():
    t = time.localtime( time.time() )
    if t[3]<12:
        greeting = "morning"
    elif t[3]<16:
        greeting = "afternoon"
    elif t[3]<20:
        greeting = "evening"
    else:
        greeting = "night"
    return greeting

# part 1 and extra credit 2
@app.route('/user/<nm>')
def hello_name(nm):
    story_list_json = get_stories('technology')
    headlines = get_headlines(story_list_json, 5)
    gre = get_greeting()
    return render_template('user.html', name=nm, my_list=headlines, section='technology', greeting=gre)

# extra credit 1 and extra credit 2
@app.route('/user/<nm>/<sec>')
def hello_name_section(nm,sec):
    story_list_json = get_stories(sec)
    headlines = get_headlines(story_list_json, 5)
    gre = get_greeting()
    return render_template('user.html', name=nm, my_list=headlines, section=sec, greeting=gre)

if __name__ == '__main__':  
    print('starting Flask app', app.name)  
    app.run(debug=True)