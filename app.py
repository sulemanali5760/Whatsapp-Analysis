import streamlit as st
import helper
import preprocessor
import matplotlib.pyplot as plt
import plotly.express as px

st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader('Choose a file')

if uploaded_file is not None:
    data = preprocessor.preprocessor(uploaded_file)

    st.dataframe(data)

# fetching all contacts

    user_list = data['name'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox('Show analysis w.r.t ',user_list)

# Analysis of Users and Stats

    if st.sidebar.button('Show Analysis'):

        num_messages,num_words, num_media, num_links = helper.fetch_stats(selected_user,data)

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(num_words)
        with col3:
            st.header("Total Media ")
            st.title(num_media)
        with col4:
            st.header("Total Links ")
            st.title(num_links)

# Busiest Users in the group
    if selected_user == 'Overall':
        st.title("Most Busy Users")
        x = helper.fetch_busy_users(data)
        col1,col2 = st.columns(2)

        fig = px.pie(values = x.values, names = x.index)
        col1.plotly_chart(fig, use_container_width=True)

        fig = px.bar(x = x.index, y = x.values)
        col2.plotly_chart(fig, use_container_width=True)

# Wordcloud
    st.title("Word Cloud (Most Used Words)")
    df_wc = helper.create_wordcloud(selected_user,data)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)

# Most Common Words
    st.title("Most Used Words By Individual and Overall")

    most_used_words = helper.most_common_words(selected_user, data)
    fig,ax = plt.subplots()
    ax.barh(most_used_words[0],most_used_words[1])
    st.pyplot(fig)

# Monthly Graph
    st.title("Interaction on monthly basis")

    timeline = helper.monthly_timeline(selected_user, data)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'])
    plt.xticks(rotation = 'vertical')
    st.pyplot(fig)

# Daily Graph
    st.title("Interaction on Daily basis")

    daily_timeline = helper.daily_timeline(selected_user, data)
    plt.figure(figsize=(18, 20))
    fig,ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'])
    plt.xticks(rotation = 'vertical')
    st.pyplot(fig)

# Week Activity Map

    st.title("Week Activity Map")
    week_activity = helper.week_activity_map(selected_user, data)
    plt.figure(figsize=(18, 20))
    fig,ax = plt.subplots()
    ax.bar(week_activity.index, week_activity.values)
    plt.xticks(rotation = 'vertical')
    st.pyplot(fig)

