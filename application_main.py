import tkinter as tk
import json
import tweepy
from tkinter import messagebox
import email_function
from geotext import GeoText
import re
import random_storage
import requests
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
import os
from datetime import datetime

class mainwindow():
    def __init__(self, master):
        self.master = master
        master.title('OSINT - Twitter Privacy Search')
        master.geometry('560x250')
        master.resizable(False, False)
        
        
        main_information = tk.Label(master, text='-A TOOL FOR FINDING POTENTIAL PRIVACY CONCERNS IN TWEETS-')

        self.search_tweet_button = tk.Button(master, text = 'Search Tweets', command=self.main_tweet_store)
        self.delete_tweet_button = tk.Button(master, text = 'Delete Stored Tweets', command=self.delete_stored_tweets)
        self.keyword_tweet_button= tk.Button(master, text='Privacy Report', command=self.newwindow)
        self.dev_inp_button = tk.Button(master, text='Developer Key(s) Menu', command=self.dev_input)
        self.tweets_number_entry = tk.Entry(master)
        self.username_get = tk.Entry(master)
        label_username = tk.Label(master, text='Enter Username (Specific Search)')
        label_query = tk.Label(master, text='Enter Query (Random Search)')
        label_user_amount = tk.Label(master, text='Enter Amount (Specific Search)')
        self.randomtweet_amount_get=tk.Entry(master)
        randomtweet_amount_label = tk.Label(master, text='Enter Amount (Random Search)')
        self.random_search_query = tk.Entry(master)
        self.random_search_button = tk.Button(master, text='Random Search', command=self.random)
    
        label_username.place(x= 50, y= 50)
        self.username_get.place(x=50, y=75, width=200)
        self.search_tweet_button.place(x=90, y=150)
        label_user_amount.place(x=50, y=100)
        self.tweets_number_entry.place(x=50, width=200, y=125)
        main_information.place(x=67, y= 10)
        label_query.place(x=330, y=50)
        self.random_search_query.place(x=330, y= 75, width=170)
        self.random_search_button.place(x=355, y=150)
        self.delete_tweet_button.place(x=350, y=200)
        self.keyword_tweet_button.place(x=230, y= 200)
        self.dev_inp_button.place(x=55, y= 200)
        self.randomtweet_amount_get.place(x=330, y= 125, width=175)
        randomtweet_amount_label.place(x=330, y=100)

    def newwindow(self):
        self.new_window_init = tk.Toplevel(self.master) 
        self.test = privacyview(self.new_window_init)

    def dev_input(self):
        self.dev_inp_init = tk.Toplevel(self.master)
        self.dev_inp_1 = twitter_dev_input(self.dev_inp_init)
    
    def main_tweet_store(self):
        
        try:
            with open('devkey.json', 'r') as f:
                temp_list = json.load(f)

            client = tweepy.Client(bearer_token=temp_list['b_token'], consumer_key=temp_list['c_token'], consumer_secret=temp_list['c_secret'], 
            access_token=temp_list['a_token'],access_token_secret=temp_list['a_secret'])

            self.get = self.username_get.get()
            self.max_results = int(self.tweets_number_entry.get())
            if self.max_results > 10:
                messagebox.showerror(title='Warning', message='Cant be more than 10')
    
            elif self.max_results <= 10: 
                tweets = client.search_recent_tweets(query=f'from:{self.get}',tweet_fields=['author_id', 'created_at'], max_results = self.max_results)
                for tweets in tweets.data:
                     tweet_text = tweets.text
                     print(tweet_text)
                     with open('stored.txt', 'a') as f: 
                            f.write(tweet_text + '\n')
            
            messagebox.showinfo(title='Information', message='Tweets Saved')
            
        except tweepy.errors.HTTPException as e:
           messagebox.showerror(title='Warning', message='Username is invalid.')
           print(e)

        except UnicodeEncodeError:
            pass
        
        except json.decoder.JSONDecodeError:
            messagebox.showerror(title='Warning', message='No dev keys eneted. Please do so.')

    def delete_stored_tweets(self):
        warning = messagebox.askyesno('Warning', 'Are you sure you want to do this?')
        if warning == True:
            with open('stored.txt', 'w') as f:
                f.close()
                messagebox.showinfo(title='', message='Deleted')
                print('Delete Successful')
        else:
            pass

    def random(self):
        
        self.therandom = self.random_search_query.get()
        amount = self.randomtweet_amount_get.get()
        amount_int = int(amount)
        
        if self.therandom == '' or amount == '':
                messagebox.showinfo('!!', 'Please enter a value')

        if amount_int > 10:
            messagebox.showinfo('!!', 'Amount must be 10 or below')

        else: 
                random_storage.themain(self.therandom, amount)
                messagebox.showinfo('!!', 'Search Complete')

        

class privacyview(mainwindow):
    def __init__(self, master):
        self.master = master
        master.title('')
        master.geometry('300x260')
        information = tk.Label(master, text='Create a PDF Report (Specific):')
        information2= tk.Label(master, text='Create a PDF Report (Random):')
        self.button2 = tk.Button(master, text='Create', command=self.report_random)
        self.button = tk.Button(master, command = self.test, text='Create')
        email_info = tk.Label(master, text='Alternatively, email yourself the report.')
        email_info2= tk.Label(master, text='Just enter your email below:')
        master.resizable(False, False)
        self.receive_entry = tk.Entry(master)
        press_to_email =  tk.Button(master, text='Email Report', command=self.emailing)

        information.place(x = 10, y = 10)
        information2.place(x = 10, y = 55)
        self.button.place(x = 210, y=8)
        self.button2.place( x = 210, y= 50)
        self.receive_entry.place(x=13, y=170)
        press_to_email.place(x = 15, y=205)
        email_info.place(x = 10, y= 120)
        email_info2.place(x=10, y= 140)

       # if not os.path.isfile('report.pdf'):
#            press_to_email.configure(state='disabled', text='REPORT DOES NOT EXIST', fg='red', background='white')
 #       else:
  #          press_to_email.configure(state='normal')
            
  
    def breakdown(self):
        with open('names.csv') as f:
            self.name_list = []
            names = [line.split(',')[0] for line in f]
            with open('stored.txt', 'r') as read:
                x = read.read()
                for word in names:
                    if word in x: 
                        self.name_list.append(word)

        with open('stored.txt', 'r') as p:
             r = p.read()
             h = GeoText(r)
             self.locations = h.cities

        with open('stored.txt', 'r') as email_word:
            self.email_list = []
            for line in email_word:
                for word in line.split(): 
                     if '.co.uk' in word:
                       self.email_list.append(word)  
                     if '.com' in word:
                       self.email_list.append(word)
            

        with open('stored.txt', 'r') as f:
            text = f.read()
            self.phone_number = re.findall(r"07\d{9}", text)
                    
            
    def test(self):
        self.breakdown()
        self.report()
         
        self.button.configure(state='disabled', text='Disabled')
        messagebox.showinfo(title='--', message=f'Report saved to "report.pdf"')

        
    def report(self):
        API_KEY = "cvsEqrTSw5uo"
        with open('stored.txt', 'r') as file:
          file_read_text = file.read()
        stored_text = []
        stored_max = []
        for line in file_read_text.split('\n'):
            file_read_text = line.strip()
            url = f"https://api.uclassify.com/v1/uClassify/iab-content-taxonomy-v3/classify/?readkey={API_KEY}&text={file_read_text}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                max_value = max(data.values())
                max_key = [key for key, value in data.items() if value == max_value][0]
                stored_text.append(f'TWEET: {file_read_text}')
                stored_max.append(f' | This is most likely {max_key}')


        pdf_file = 'report.pdf'
        c = canvas.Canvas(pdf_file, pagesize=letter)
        page_width, page_height = c._pagesize
        
        c.setFillColorRGB(0, 0, 255)
        c.setFont('Helvetica', 22)
        y = 750
        c.drawString(150, y, '- TWITTER PRIVACY REPORT -')
        y -= 50
        c.setFillColorRGB(0, 0, 0)
        c.setFont('Helvetica', 12)   
        c.drawString(50, y, 'POTENTIAL LOCATIONS: ')
        y -= 20
        if len(self.locations) == 0:
            c.drawString(50, y, 'None Found')
        else:
            c.drawString(50, y, ', '.join(self.locations))
        y -= 30
        c.drawString(50, y, 'POTENTIAL NAMES: ')
        y -= 20
        if len(self.name_list) == 0:
            c.drawString(50, y, 'None Found')
        else:
             c.drawString(50, y, ', '.join(self.name_list))
        y -= 30
        c.drawString(50, y, 'POTENTIAL EMAILS: ')
        y -= 20
        if len(self.email_list) == 0:
           c.drawString(50, y, 'None Found')
        else:
            c.drawString(50, y, ', '.join(self.email_list))
        y -= 30
        c.drawString(50, y, 'POTENTIAL NUMBERS: ')
        y -= 20
        if len(self.phone_number) == 0:
            c.drawString(50, y, 'None Found')
        else:
             c.drawString(50, y, ', '.join(self.phone_number))
        y -= 50
        c.setFillColorRGB(0, 0, 255)
        c.setFont('Helvetica', 22)
        c.drawString(158, y, '- SENTIMENT ANALYSIS -')
        y -= 50

        for i, text in enumerate(stored_text):
            if y < 50:
                c.showPage()
                y = page_height - 50

            c.setFont('Helvetica', 12)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(50, y, text)
            y -= 20
            c.setFont('Courier', 12)
            c.drawString(50, y, stored_max[i])
            y -= 20

        c.save()

    def report_random(self):
        API_KEY = "cvsEqrTSw5uo"
        with open('stored_random.txt', 'r') as file:
          text111 = file.read()
        stored_text = []
        stored_test = []
        for line in text111.split('\n'):
            text111 = line.strip()
            url = f"https://api.uclassify.com/v1/uClassify/iab-content-taxonomy-v3/classify/?readkey={API_KEY}&text={text111}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                max_value = max(data.values())
                max_key = [key for key, value in data.items() if value == max_value][0]
                stored_text.append(f'TWEET: {text111}')
                stored_test.append(f' | This is most likely {max_key}')


        pdf_file = 'report_random.pdf'
        c = canvas.Canvas(pdf_file, pagesize=letter)
        page_width, page_height = c._pagesize
        

        c.setFillColorRGB(0, 0, 255)
        c.setFont('Helvetica', 22)
        y = 750
        c.drawString(158, y, '- SENTIMENT ANALYSIS -')
        y -= 25
        c.setFont('Helvetica', 16)
        c.drawString(225, y, 'Random Tweets')
        y -= 50

        for i, text in enumerate(stored_text):
            if y < 50:
                c.showPage()

            c.setFont('Helvetica', 12)
            c.setFillColorRGB(0, 0, 0)
            c.drawString(50, y, text)
            y -= 20
            c.setFont('Courier', 12)
            c.drawString(50, y, stored_test[i])
            y -= 20

        c.save()

        messagebox.showinfo(title='!!', message='Random Report Generated')

    def emailing(self):

        receiver=self.receive_entry.get() 
        email_function.body(receiver)
       
class twitter_dev_input():
    def __init__(self, master):
        self.master = master
        master.title('Developer Code Input')
        master.geometry('400x240')
        master.resizable(False, False)
        self.input_user_entries = tk.Button(master, text='Save to File', command=self.user_input_to_file).grid(pady=10, column=1, row=5)
        
        self.user_bearer_token = tk.Entry(master)
        self.user_consumer_token = tk.Entry(master)
        self.user_consumer_secret = tk.Entry(master)
        self.user_access_token = tk.Entry(master)
        self.user_access_token_secret = tk.Entry(master)

        self.user_bearer_token.grid(column=1, row=0, pady=5, padx=10)
        self.user_consumer_token.grid(column=1, row = 1, pady=5, padx=10)
        self.user_consumer_secret.grid(column=1, row=2, pady=5, padx=10)
        self.user_access_token.grid(column=1, row=3, pady=5, padx=10)
        self.user_access_token_secret.grid(column=1, row=4, pady=5, padx=10)
    
        self.labels(master)

    def labels(self, master):
        bearer_token_label = tk.Label(master, text='Bearer Token Entry').grid(column=0, row=0, padx=10)
        user_consumer_token_label = tk.Label(master, text='User Cosumer Token').grid(column=0, row=1, padx=10)
        user_consumer_secret_label = tk.Label(master, text='Cosumer Secret').grid(column=0, row=2, padx=10)
        user_access_token_label = tk.Label(master, text='User Access Token').grid(column=0, row=3, padx=10)
        access_token_secret_label = tk.Label(master,text = 'Access Token Secret').grid(column=0, row=4, padx=10)
    
    def user_input_to_file(self):
        stored_dictionary = {
                                "b_token": self.user_bearer_token.get(), 
                                "c_token": self.user_consumer_token.get(),
                                "c_secret": self.user_consumer_secret.get(),
                                "a_token": self.user_access_token.get(),
                                "a_secret": self.user_access_token_secret.get()      
                                
                            }

        with open('devkey.json', 'w') as f: 
           json.dump(stored_dictionary, f)
    
    

if __name__ == '__main__':
    root = tk.Tk()
    mainwindow(root)
    root.mainloop()

