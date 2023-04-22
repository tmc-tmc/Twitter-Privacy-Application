import tweepy
import json
from tkinter import * 
import nltk


b_token='AAAAAAAAAAAAAAAAAAAAAAe2kQEAAAAA1R82X51MUKlYmmX%2BP%2BOKjew3ZpA%3D2WqE3HjJnJQOHSzt8cF7p0Uydi3ocKLQXPZL1duelZ1D0FdVqw'
c_key='5xomEnJ42rkapiOpdE2XiM0U7'
c_secret='uCOm9RfA3rKYFptJJ9j9tTqXI62TJhVBYVW1bp8EWaZu4Jzr6p'
a_token = '1602954257874944000-PPvZDvmEgMAmwrOgHQBGF7V3lLl5Dw'
a_token_secret = 'fhYgljnzrLYfymdeMfKfpY6Nh8BEiJU6OfBLgRrkQUx85'

try:

    client = tweepy.Client(bearer_token=b_token, consumer_key=c_key, consumer_secret=c_secret, 
    access_token=a_token,access_token_secret=a_token_secret)

except:
    pass


window = Tk()
window.title('Tweet Searcher')


def window2():
   topwindow = Toplevel(window)
   topwindow.title('Privacy Search')
   topwindow.geometry('800x400')

   def breakdown():
    with open('stored.txt') as f: 
        x = f.read()
    with open('test1.txt') as g: 
        v = g.read()
    token_stored_1 = nltk.word_tokenize(x)
    token_stored_2 = nltk.word_tokenize(v)

    test = []
    
    for word in token_stored_2: 
        if word in token_stored_1:
            test.append(word)

    r =  Message(topwindow, text=test).pack()

   Button(topwindow, text='Hello', command=breakdown).pack()
   Label(topwindow, text='Use this window to observe any potential privacy issues within tweets that have been scraped and saved.').pack()
   topwindow.mainloop()
    
def choice(u_choice):
    username_query = 'from:' + u_choice
    try:
        tweets = client.search_recent_tweets(query=username_query, tweet_fields=['author_id', 'created_at'], max_results=5)
        for tweet in tweets.data:
            text = tweet.text
            print(text)
            with open('stored.txt', 'a') as f:
                f.write(text + '\n')
        usernamesave(u_choice)
    except:
        print('Hello')


def usernamesave(test):
    
    json_object = json.dumps(dict, indent = 4)
    
    with open('maintest.json', 'w') as f:
        f.write(json_object)    

def button_press():
    test = entry1.get()
    print(test)
    choice(test)

def delete():
    with open('maintest.json', 'w') as f:
        f.close()
        print('Delete Successful')

entry1 = Entry(window, width = 20)
entry1.pack()

def buttons():
    s_tweet_button = Button(window, text = 'Search Tweets', command=button_press).pack()
    hello = Button(window, text = 'Delete Stored Tweets', command=(delete)).pack()
    Button(window, text='Show Keywords Found', command=window2).pack()

list_val = StringVar(window)
list_val.set('Previously used...')

def optionsmenu():
    try:
       with open('maintest.json', 'r') as f: 
        r = json.load(f)
        c = r['username']
        w = OptionMenu(window, list_val, c)
        w.pack()
    except:
        pass
    
def display():
    choice = list_val.get()
    print(choice)

optionsmenu()
buttons()


window.geometry('700x400')
window.resizable(False, False)
window.mainloop()


#Tom63805437
