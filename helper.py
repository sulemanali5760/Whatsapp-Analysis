import streamlit
from urlextract import  URLExtract
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd

extractor = URLExtract()


def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

# Number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

# Number of Media
    num_media = df[df['message'] == '<Media omitted>'].shape[0]

# Number of Links
    links = []
    for link in df['message']:
        links.extend(extractor.find_urls(link))


    num_messages = df.shape[0]
    num_words = len(words)
    num_links = len(links)

    return num_messages, num_words, num_media, num_links



def fetch_busy_users(df):
    x = df['name'].value_counts().head()
    return x

# Wordcloud

def create_wordcloud(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    temp = df[df['name'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    temp = temp[temp['message'] != 'deleted']


    wc = WordCloud(width=500,height=500,min_font_size=10, background_color= 'white')
    df_wc = wc.generate(temp['message'].str.cat(sep = " "))

    return df_wc


def most_common_words(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    temp = df[df['name'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    temp = temp[temp['message'] != 'deleted']

    f = open('stop_words.txt', 'r', encoding='Utf-8')
    stop_words = f.read()

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    df['month_num'] = df['date'].dt.month
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + '-' + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    df['only_date'] = df['date'].dt.date
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

# User Weekly Activity Map

def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    df['day_name'] = df['date'].dt.day_name()
    return df['day_name'].value_counts()

# User Engagement

def user_engaged_hours(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['name'] == selected_user]

    h = []
    for i in range(len(df['hours'])):
        h.append(str(df.iloc[i, 8]) + '-' + str(df.iloc[i, 2]))
        df['period'] = h
        engaged_hours = df.groupby('period').count()['message']

    return engaged_hours