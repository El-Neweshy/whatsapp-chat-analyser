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
        else:
            line = line.replace('\n', '')

        # 1- In case action is has been taken
        if len(action_symbol) != 0:
            line = line.replace(date_time[0], '')
            line = line.replace(action_symbol[0], '')
            try:
                split = re.split(':', line)
                sender = split[0]
                message = split[1]
                date = dates[0]
                time = times[0]
                action = True
            except:
                message = line

        # 2- In case a new message has started
        elif len(date_time) != 0:
            line = line.replace(date_time[0], '')
            try:
                split = re.split(':', line)
                sender = split[0]
                message = split[1]
                date = dates[0]
                time = times[0]
            except:
                message = line

        # 3- In case of contuniong talk
        else:
            message = line
            action = False

        info = {'date': date, 'time': time, 'sender': sender,
                'message': message, 'action': action}
        data.append(info)
    return data


if __name__ == '__main__':
    text_file_lines = read_txt_file('_chat.txt')
    data = analyse_lines(text_file_lines)
    print(data[0])