import requests
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import json
import pandas as pd
from datetime import datetime, timedelta
import re
import time
import math

import undetected_chromedriver as uc
from undetected_chromedriver import Chrome


#Open MEXC exchange in google chrome
options = uc.ChromeOptions()
options.headless = False

browser = uc.Chrome(options=options, use_subprocess=True)

# Execute JavaScript to open a new tab
def refreshfundingrecordspage():
    browser.get("https://www.lbank.com/my/orders/futures/history-record/")
    time.sleep(2)

    filter = browser.find_element('xpath','//div[@class="ant-select-selector"]')
    filter.click()
    time.sleep(1)
    dropdownoptions = browser.find_elements('xpath','//div[@class="ant-select-item-option-content"]')
    dropdownoptions[5].click()
    time.sleep(1)
    searchbutton = browser.find_element('xpath','//button[@type="button"][@class="index_lbk-button__PBU3Z "]')
    searchbutton.click()

    # fundrecord = browser.find_elements('xpath','//button[@type="button"]')
    # fundrecord[3].click()
    time.sleep(1)


#connect to google sheets
credentials_path = 'credentials.json'
SPREADSHEET_ID = '1MupqF2-Z6-MCk2lcebpGH6jWFsC9uZbkAV3LC6x9reg'
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
gc = gspread.authorize(credentials)


# Open the Google Sheet by key
worksheet = gc.open_by_key(SPREADSHEET_ID).sheet1


while True:
    
    refreshfundingrecordspage()
    time.sleep(10)
    datas = browser.find_elements('xpath','//tr[@class="index_table-body-row__blMF0 undefined"]')

    fundingdatas = []
    for i in datas:
        print(i.text)
        fundingdatas.append(i.text)

    columns = ['Pair', 'Type', 'Timestamp', 'Action', 'Fee', 'Value','Funding Fee','amount']
    data = [item.split() for item in fundingdatas]

    df = pd.DataFrame(data,columns = columns)
    #combine date and time
    df['DateTime'] = pd.DataFrame(df['Timestamp'] + ' ' + df['Action'])

    alldata = worksheet.get_all_values()

    lastfundingfee = format(math.floor(float(alldata[-1][4]) * 10000) / 10000, '.4f')
    indexnumberofthelastfundingfee = df[df['Funding Fee'] == lastfundingfee].index[0]

    tobeinsrtedvalues = (df['Funding Fee'][0:indexnumberofthelastfundingfee].tolist())[::-1]
    tobeinsrtedvaluescoin = (df['Pair'][0:indexnumberofthelastfundingfee].tolist())[::-1]
    tobeinsrtedvaluesdatetime = (df['DateTime'][0:indexnumberofthelastfundingfee].tolist())[::-1]


    if tobeinsrtedvalues:#if there are values to be updated
        #get the last row in google sheets
        startingrow = int(len(worksheet.col_values(5))+1)
        randomlastrow = int(len(worksheet.col_values(5))+9)
        startingrowfee = 'E'+ str(startingrow)
        randomlastrowfee = 'E'+ str(randomlastrow)

        startingrowpair = 'A'+ str(startingrow)
        randomlastrowpair = 'A'+ str(randomlastrow)

        startingrowdatetime = 'C'+ str(startingrow)
        randomlastrowdatetime = 'C'+ str(randomlastrow)

        cell_rangefee = f'{startingrowfee}:{randomlastrowfee}'
        cell_rangepair = f'{startingrowpair}:{randomlastrowpair}'
        cell_rangedatetime = f'{startingrowdatetime}:{randomlastrowdatetime}'


        tobeinsrtedvalues_sublist = [[float(value)] for value in tobeinsrtedvalues]
        tobeinsrtedvaluescoin_sublist = [[pair] for pair in tobeinsrtedvaluescoin]
        tobeinsrtedvaluesdatetime_sublist = [[pair] for pair in tobeinsrtedvaluesdatetime]

        # Define the new values for each cell in the range

        # Update the values in the specified range
        worksheet.update(cell_rangefee, tobeinsrtedvalues_sublist)
        worksheet.update(cell_rangepair, tobeinsrtedvaluescoin_sublist)
        worksheet.update(cell_rangedatetime, tobeinsrtedvaluesdatetime_sublist)


        # Set the alignment of the cells to center
        format_body = {
            'horizontalAlignment': 'CENTER',
            'textFormat': {'fontSize': 11, 'bold': False, 'italic': False, 'fontFamily' : 'Calibri'}
        }


        # Apply formatting to the entire range
        cell_ranges = [cell_rangefee,cell_rangepair]

        for cell_range in cell_ranges:
            worksheet.format(cell_range, format_body)
        print('Data Updated. Please Wait for 4 hours')
        time.sleep(14400)
