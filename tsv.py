#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import os
import sys
import re
import pandas as pd
from datetime import date


os_path = os.path
csv_writer = csv.writer
sys_exit = sys.exit
wars = {
    '1948 Arab–Israeli War': [pd.to_datetime("November 1947"), pd.to_datetime("July 1949")],
    '1956 Suez Crisis': [pd.to_datetime("October 1956"), pd.to_datetime("November 1956")],
    '1967 Six-Day War': [pd.to_datetime("5th of June 1967"), pd.to_datetime("10th of June 1967")],
    '1967 War of Attrition': [pd.to_datetime("11th of June 1967"), pd.to_datetime("7th of August 1970")],
    '1973 Yom Kippur War': [pd.to_datetime("6th of October 1973"), pd.to_datetime("24th of October 1973")],
    '1982 Lebanon War': [pd.to_datetime("6th of June 1982"), pd.to_datetime("29th of September 1982")],
    '1987 First Intifada': [pd.to_datetime("9 December 1987"), pd.to_datetime("20 August 1993")],
    '1985 South Lebanon conflict': [pd.to_datetime("June 1985"), pd.to_datetime("24 May 2000")],
    '2000 Second Intifada': [pd.to_datetime("29 September 2000"), pd.to_datetime("2005")],
    '2006 Lebanon War': [pd.to_datetime("12th of July 2006"), pd.to_datetime("14th of August 2006")],
    '2008 Gaza War': [pd.to_datetime("27 December 2008"), pd.to_datetime("21 January 2009")],
    '2006 Operation Pillar of Defense': [pd.to_datetime("14th of November 2012"), pd.to_datetime("21th of November 2012")],
    '2014 Operation Protective Edge': [pd.to_datetime("8th of July 2014"), pd.to_datetime("26 of August 2014")],
    'Other': [pd.to_datetime("1 of January 1800"), pd.to_datetime(date.today())]
}

def get_folder(date):
    for x in wars:
        start, end = wars[x]
        if date >= start and date <= end:
            return x
    print(date)
    return 'Other'

def make_dirs():
    for x in wars:
        dir = 'E:\WorkSpace\lemlda\corpus\{0}'.format(x)
        if not os.path.exists(dir):
            os.mkdir(dir)

if __name__ == '__main__':
    file_path = 'E:\WorkSpace\lemlda\izkor-full-data-json.tsv'
    map_name = 'E:\WorkSpace\lemlda\map.txt'

    if (
        not os_path.isfile(file_path) or
        not file_path.endswith('.tsv')
    ):
        print('You must input path to .tsv file for splitting.')
        sys_exit()
    make_dirs()
    file_name = os_path.splitext(file_path)[0]
    map_file = open(map_name, 'w', newline='', encoding='utf-8')

    with open(file_path, 'r', newline='', encoding='utf-8') as tsv_file:

        chunk_file = None
        writer = None
        counter = 1
        reader = csv.reader(tsv_file, delimiter='\t')
        folder = None
        for index, chunk in enumerate(reader):
            # if index >= 5000:
            #     break
            name = re.sub('[()."]', '', chunk[0])
            if name == '':
                continue
            for c in chunk:
                if c == '':
                    continue
                if c == chunk[0]:
                    date = pd.to_datetime(name.split('_')[-1])
                    folder = get_folder(date)
                    map_file.write("{0}\t\t{1}\t\t{2}\n".format(name, index, folder))
                    continue
                chunk_name = 'E:\WorkSpace\lemlda\corpus\{0}'.format(folder)
                with open('{0}\{1}_{2}.txt'.format(chunk_name, index, counter), 'w', newline='', encoding='utf-8') as chunk_file:
                    counter += 1
                    chunk_file.write(c)
            counter = 1
            #print('File "{0} {1}" complete.'.format(name, index))
            if chunk_file is not None:
                chunk_file.close()
        map_file.close()
    print('done!')
