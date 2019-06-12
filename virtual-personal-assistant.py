#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 11 01:59:54 2019

@author: suryakantkumar
"""

import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import vlc
import urllib
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipedia
import random
from time import strftime
import datetime


def aliannaResponse(audio):
    "speaks audio passed as command/argument"
    print(audio)
    for line in audio.splitlines():
        os.system("say " + audio)


def myCommand():
    "listens for commands"
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print('You said: ' + command + '\n')
    except sr.UnknownValueError:
        print('....')
        command = myCommand();
    return command


def assistant(command):
    "Some rule based learning"
    greetings = ['hey there', 'hello', 'hi', 'hai', 'hey', 'hey']
    question = ['how are you', 'how are you doing']
    responses = ['Okay', "I am fine, Thanks for asking", "I am pretty good", "Not too shabby", "Very well,Thank you",
                 "Happy as a clamShell Mac", " I feel good", "I am Happy as a happy mac",
                 "I am happy as finder, Actually no...no Noone can be happy as finder",
                 "If i were any better, vitamins would be taking me"]
    creation = ['who made you', 'who created you', 'who build you', 'who invented you']
    creation_reply = ['I was created by Suryakant right in his Mac', 'Suryakant', 'Some guy whom i never got to know',
                      'I, alianna, designed by Suryakant in his Mac']
    intro = ["who are you", "what is your name", "introduce", "introduce yourself"]
    intro_reply = [" I am alianna, here to help", "Who I am is not important", "I am alianna", "My name, its alianna",
                   "i am alianna, but i do not like talking about myself", "alianna",
                   "i am just a humble virtual assistant", "My name is alianna, but you knew that already",
                   "alianna, pleased to meet you"]
    google = ['open browser', 'open google', "google", "let me google", "open chrome", "open any browser",
              "open default browser", "open google for me"]
    song = ['song', 'play some music', 'play music', 'play songs', 'play a song', 'open music player',
            'alianna play some music', 'open itunes', 'sing a song', 'song please']
    video = ['open youtube', 'i want to watch a video', 'i want to watch video', 'i want to watch some videos',
             'i am feeling boring']
    close = ['exit', 'close', 'goodbye', 'nothing', 'shut down', "go alianna take some rest", "alianna take some rest",
             "bye", "bye alianna"]
    color = ['what is your color', 'what is your colour', 'your color', 'what color you wear',
             'what color you are wearing', 'what color you made of']
    color_reply = ['Right now its rainbow', "Hey what's with all that personal questions", 'Right now its transparent',
                   'It depends on the lighting, and on my mood', 'the color of omniscience']
    fav_color = ['what is your favourite colour', 'your favourite color', 'favourite color', 'what color do you like']
    compliment = ['thank you', 'thankyou', 'thanks', 'thanks a lot', 'thanks buddy', 'thanks alianna',
                  'thanks a lot alianna', 'thank you alianna']
    compliment_reply = ['youre welcome', 'glad i could help you', 'Sure thing', 'dont mention it', 'no problem',
                        'no worries', 'my pleasure']

    # open reddit (Give command like this: open reddit for me)
    if 'open reddit' in command:
        reg_ex = re.search('open reddit (.*)', command)
        url = 'https://www.reddit.com/'
        if reg_ex:
            subreddit = reg_ex.group(1)
            url = url + 'r/' + subreddit
        webbrowser.open(url)
        aliannaResponse('The Reddit content has been opened for you Sir.')

    # open google (Give command like this: open google for me)
    elif command in google:
        webbrowser.open('https://www.google.com/')
        aliannaResponse('The browser has been opened for you Sir.')

    # open youtube (Give any command from list named "video")
    elif command in video:
        reply = random.choice(video)
        webbrowser.open('https://www.youtube.com/')
        aliannaResponse('I think youtube is a good platform to watch. Enjoy your song sir')

    # open any website (Give command like this: open facebook.com)
    elif 'open' in command:
        reg_ex = re.search('open (.+)', command)
        if reg_ex:
            domain = reg_ex.group(1)
            print(domain)
            url = 'https://www.' + domain
            webbrowser.open(url)
            aliannaResponse('The website you have requested has been opened for you Sir.')
        else:
            pass

    # greetings (Greet in any ways from list named "greeting")
    elif command in greetings:
        day_time = int(strftime('%H'))
        if day_time < 12:
            aliannaResponse('Hello Sir. Good morning. What can i do for you?')
        elif 12 <= day_time < 18:
            aliannaResponse('Hello Sir. Good afternoon. What can i do for you?')
        else:
            aliannaResponse('Hello Sir. Good evening. What can i do for you?')

    # Tasks (It will tell, what tasks it can perfrom)
    elif 'help me' in command:
        aliannaResponse("I am allowed to do some sort of work like: Open reddit subreddit, Open any website, Send email, Current weather in any city, Greetings, play any video, change wallpaper, news for today, Current time, top stories from google news, or anything limited to my knowledge")

    # joke (Give command like this: tell me some joke)
    elif 'joke' in command:
        res = requests.get(
            'https://icanhazdadjoke.com/',
            headers={"Accept": "application/json"})
        if res.status_code == requests.codes.ok:
            aliannaResponse(str(res.json()['joke']))
        else:
            aliannaResponse('oops!I ran out of jokes')

    # top stories from google news (Give command like this: Tell me news for today)
    elif 'news for today' in command:
        try:
            news_url = "https://news.google.com/news/rss"
            Client = urlopen(news_url)
            xml_page = Client.read()
            Client.close()
            soup_page = soup(xml_page, "xml")
            news_list = soup_page.findAll("item")
            for news in news_list[:5]:
                aliannaResponse(news.title.text)
        except Exception as e:
            print(e)

    # current weather (Give command like this: Current weather in London or pinCode)
    elif 'current weather' in command:
        reg_ex = re.search('current weather in (.*)', command)
        if reg_ex:
            city = reg_ex.group(1)
            owm = OWM(API_key='1ad8a325429ff07a9229415c22ffa76b')
            obs = owm.weather_at_place(city)
            w = obs.get_weather()
            h = w.get_humidity()
            k = w.get_detailed_status()
            x = w.get_temperature(unit='celsius')
            aliannaResponse('Current weather in %s is %s, The current temperature is %0.1f degeree celcius, maximum temperature is %0.1f, and the minimum temperature is %0.1f degree celcius, climate contains %0.1f percent humidity' % (city, k, x['temp'], x['temp_max'], x['temp_min'], h))

    # time (Give command like this: what is current time?)
    elif 'time' in command:
        now = datetime.datetime.now()
        aliannaResponse('Current time is %d hours %d minutes' % (now.hour, now.minute))

    # email (Give command like this: Send an email for me)
    elif 'email' in command:
        sender_email = 'yoyoroadies@gmail.com'
        sender_email_password = 'Enter-password'
        receiver_email = 'skantgo@gmail.com'
        aliannaResponse('Who is the recipient?')
        recipient = myCommand()
        if 'suryakant' in recipient:
            aliannaResponse('What should I say to him?')
            content = myCommand()
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.ehlo()
            mail.starttls()
            mail.login(sender_email, sender_email_password)
            mail.sendmail(sender_email, receiver_email, content)
            mail.close()
            aliannaResponse('Email has been sent successfuly. You can check your inbox.')
        else:
            aliannaResponse('I don\'t know what you mean!')

    # launch any application on the system/MacOS (Give command like this: Launch itunes)
    elif 'launch' in command:
        reg_ex = re.search('launch (.*)', command)
        if reg_ex:
            appname = reg_ex.group(1)
            appname1 = appname + ".app"
            subprocess.Popen(["open", "-n", "/Applications/" + appname1], stdout=subprocess.PIPE)
            aliannaResponse('I have launched the desired application')


    # play youtube song (Give command like this: Play me a song)
    elif 'play me a song' in command:
        path = '/Users/suryakantkumar/aliannaAssistant/downloads/'
        folder = path
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        aliannaResponse('What song shall I play Sir?')
        mysong = myCommand()
        if mysong:
            flag = 0
            url = "https://www.youtube.com/results?search_query=" + mysong.replace(' ', '+')
            response = urlopen(url)
            html = response.read()
            soup1 = soup(html, "lxml")
            url_list = []
            for vid in soup1.findAll(attrs={'class': 'yt-uix-tile-link'}):
                if ('https://www.youtube.com' + vid['href']).startswith("https://www.youtube.com/watch?v="):
                    flag = 1
                    final_url = 'https://www.youtube.com' + vid['href']
                    url_list.append(final_url)
            url = url_list[0]
            ydl_opts = {}
            os.chdir(path)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            vlc.play(path)
            if flag == 0:
                aliannaResponse('I have not found anything in Youtube ')


    # changes wallpaper from splash (Give command like this: Change wallpaper)
    elif 'change wallpaper' in command:
        folder = '/Users/suryakantkumar/aliannaAssistant/wallpaper/'
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)
        api_key = '1ab94638c94b887262e5a4d180c078f12929c6bea5c3e420e4a7eee7b41fb7d'
        url = 'https://api.unsplash.com/photos/random?client_id=' + api_key  # pic from unspalsh.com
        f = urlopen(url)
        json_string = f.read()
        f.close()
        parsed_json = json.loads(json_string)
        photo = parsed_json['urls']['full']
        # Location where we download the image to.
        urllib.request.urlretrieve(photo, '/Users/suryakantkumar/aliannaAssistant/wallpaper/a.jpg')
        subprocess.call(["killall Dock"], shell=True)
        aliannaResponse('wallpaper changed successfully')

    # askme anything (Give command like this: Tell me about Elon musk)
    elif 'tell me about' in command:
        reg_ex = re.search('tell me about (.*)', command)
        try:
            if reg_ex:
                topic = reg_ex.group(1)
                wiki = wikipedia.page(topic)
                aliannaResponse(wiki.content[:500])
        except Exception as e:
            print(e)
            aliannaResponse(e)

    # Ask about (Give any command from list named "question")
    elif command in question:
        reply = random.choice(responses)
        aliannaResponse(reply)

    # Ask about creation of it (Give any command from list named "creation")
    elif command in creation:
        reply = random.choice(creation_reply)
        aliannaResponse(reply)

    # Compliment (Give any command from list named "compliment")
    elif command in compliment:
        reply = random.choice(compliment_reply)
        aliannaResponse(reply)

    # Listen songs from iTunes (Give any command from list named "song")
    elif command in song:
        appname = 'iTunes.app'
        subprocess.Popen(["open", "-n", "/Applications/" + appname], stdout=subprocess.PIPE)

    # Assistant's color (Give any command from list named "color")
    elif command in color:
        reply = random.choice(color_reply)
        aliannaResponse(reply)
        # aliannaResponse('It keeps changing every micro second')

    # Favourite color (Give any command from list named "fav_color")
    elif command in fav_color:
        reply = random.choice(color_reply)
        aliannaResponse(reply)

    # Introduction (Give any command from list named "intro")
    elif command in intro:
        reply = random.choice(intro_reply)
        aliannaResponse(reply)

    # Shut Down (Give any command from list named "close")
    elif command in close:
        aliannaResponse('Bye bye Sir. See you later.')
        sys.exit()


aliannaResponse('Hi Suryakant, I am alianna. I am your personal voice assistant, Please give a command or say "help me" and I will tell you what all I can do for you.')
# loop to continue executing multiple commands
while True:
    assistant(myCommand())