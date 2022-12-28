import re
import pandas as pd

def preprocessor(uploaded_file):

    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    # df = pd.DataFrame(re.findall(r'\d{1,2}\/\d{1,2}\/\d{1,2}, (\d+:\d+) (.*) - (.*): (.*)', data))
    df = pd.DataFrame(re.findall(r'(\d+\/\d+\/\d+), (\d+:\d+) (.*) - (.*): (.*)',data))

    df.rename(columns={0: 'date', 1: 'time', 2: 'AM/PM', 3: 'name', 4: 'message'}, inplace=True)

    hours = []
    minutes = []

    for i in range(len(df)):
        s = df.iloc[i,1]
        hours.append(s.split(':')[0])
        minutes.append(s.split(':')[1])

    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hours'] = hours
    df['minutes'] = minutes

    for i in range(len(df['name'])):
        if re.search(':',df.iloc[i,3]):
            df.iloc[i,3] = df.iloc[i,3].split(':')[0]

    return df






# ???????????????????????????????????????????????????????????????
    # file = open(filepath, encoding='utf-8')
    # raw = []
    # df = []
    # count = 0
    #
    # for index, line in enumerate(file.readlines()):
    #     x = re.search(r'(.+), (\d+:\d+) (.*) - (.*): (.*)', line)
    #
    #     if x == None:
    #         pass
    #     else:
    #         raw.append([*x.groups()])
    # file.close()
    #
    # df = pd.DataFrame(raw)
    # df.rename(columns={0: 'date', 1: 'time', 2: 'AM/PM', 3: 'name', 4: 'message'}, inplace=True)
    #
    # df['date'] = pd.to_datetime(df['date'])
    # df['year'] = df['date'].dt.year
    # df['month'] = df['date'].dt.month_name()
    # df['day'] = df['date'].dt.day
    #
    # hours = []
    # minutes = []
    # for i in range(len(df['time'])):
    #     s = df.iloc[i, 1]
    #     hours.append(s.split(':')[0])
    #     minutes.append(s.split(':')[1])
    #
    # df['hours'] = hours
    # df['minutes'] = minutes
    #
    # return df