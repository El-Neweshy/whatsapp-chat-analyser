# -*- coding: utf-8 -*-
import os
import re
import pandas as pd


def read_txt_file(file_name):
    text_file_lines = open('{}'.format(file_name), encoding='utf-8').readlines()
    return text_file_lines

def analyse_lines(text_file_lines):
    '''
    There are 4 cases here for each line:
    
    Empty Line, will ignore.

    OR
    1- Taking action (Messages and calls are end-to-end encrypted, created group, added you, image omitted, ‎audio omitted, sticker omitted, This message was deleted, changed their phone number)
    2- Starting a message
    3- Continue talk
    '''
    for line in text_file_lines:
        date_time = re.findall(r'\[\d{2}\/\d{2}\/\d{4}, \d{1,2}\:\d{2}:\d{2} \w{2}\]', line)
        action = re.findall('‎', line)
        
        # In case of empty line, ignore line and remove 'new line' from other lines
        if line == '\n':
            continue
        else:
            line = line.replace('\n', '')

        # 1- In case action is has been taken
        if len(action) !=0:
            print(line)
            pass
        
        # 2- In case a new message has started
        elif len(date_time) !=0:
            date = re.findall(r'\d{2}\/\d{2}\/\d{4}', line)[0]
            time = re.findall(r'\d{1,2}\:\d{2} \w{2}', line)[0]
            # sender = re.findall(r'- [\w+ ]+', line)[0]
            # sender = sender[2:]
            # message = line.replace('{}, {} - {}: '.format(date, time, sender), '')
            
            # print('date', date, 'time', time)
        
        # 3- In case of contuniong talk
        else:
            # print(line)
            pass
    return

if __name__ == '__main__':
    text_file_lines = read_txt_file('_chat.txt')
    analyse_lines(text_file_lines)