# -*- coding: utf-8 -*-
import os
import re
import pandas as pd


def read_txt_file(file_name):
    text_file_lines = open('{}'.format(file_name),
                           encoding='utf-8').readlines()
    return text_file_lines


def analyse_lines(text_file_lines):
    '''
    There are 4 cases here for each line:
    Either
    Empty Line, will ignore.
    OR
    1- Taking action (Messages and calls are end-to-end encrypted, created group, added you, image omitted, ‎audio omitted, sticker omitted, This message was deleted, changed their phone number, location)
    2- Starting a message
    3- Continue talk
    '''

    sender = None
    date = None
    time = None
    action = False
    message = None
    action_type = None

    data = []

    for line in text_file_lines:
        date_time = re.findall(
            r'\[\d{2}\/\d{2}\/\d{4}, \d{1,2}\:\d{2}:\d{2} \w{2}\]', line)
        dates = re.findall(r'\d{2}\/\d{2}\/\d{4}', line)
        times = re.findall(r'\d{1,2}\:\d{2} \w{2}', line)
        action_symbol = re.findall('‎', line)

        # In case of empty line, ignore line and remove 'new line' from other lines
        if line == '\n':
            continue
        elif 'Messages and calls are end-to-end encrypted. No one outside of this chat, not even WhatsApp, can read or listen to them.' in line:
            continue
        else:
            line = line.replace('\n', '')

        # 1- In case action is has been taken
        if len(action_symbol) != 0:
            line = line.replace(date_time[0], '')
            line = line.replace(action_symbol[0], '')
            try:
                if ':' in line:
                    split = re.split(':', line)
                    sender = split[0]
                    action_type = split[1]
                elif 'created' in line:
                    split = re.split('created', line)
                    sender = split[0]
                    action_type = 'created' + split[1]
                elif 'changed' in line:
                    split = re.split('changed', line)
                    sender = split[0]
                    action_type = 'changed' + split[1]
                elif 'added' in line:
                    split = re.split('added', line)
                    sender = split[0]
                    action_type = 'added' + split[1]
                
                message = None
                date = dates[0]
                time = times[0]
            except:
                action_type = line

        # 2- In case a new message has started
        elif len(date_time) != 0:
            line = line.replace(date_time[0], '')
            try:
                split = re.split(':', line)
                sender = split[0]
                message = split[1]
                date = dates[0]
                time = times[0]
                action_type = None
            except:
                message = line

        # 3- In case of contuniong talk
        else:
            message = line
            action_type = None

        # Appending data
        info = {'date': date, 'time': time, 'sender': sender,
                'message': message, 'action type': action_type}
        data.append(info)
    
    return data


def create_csv(lst):
    df = pd.DataFrame(columns=['date', 'time', 'sender', 'message', 'action type'])

    for dict in lst:
        df = df.append(dict, ignore_index=True)

    # strip all spaces
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Write data in a csv
    df.to_csv('results.csv', sep=',', encoding='utf-8-sig')

    return df


if __name__ == '__main__':
    text_file_lines = read_txt_file('_chat.txt')
    data = analyse_lines(text_file_lines)
    create_csv(data)