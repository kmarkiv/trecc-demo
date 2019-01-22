#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import sys
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)
import gspread

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
import json
from oauth2client.client import SignedJwtAssertionCredentials

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = ''
SAMPLE_RANGE_NAME = 'Class Data!A2:E'
SAMPLE_RANGE_NAME = 'A1:C6'


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    json_key = json.load(open('creds.json'))  # json credentials you downloaded earlier
    scope = ['https://spreadsheets.google.com/feeds']

    credentials = SignedJwtAssertionCredentials(json_key['client_email'], json_key['private_key'].encode(),
                                                scope)  # get email and key from creds

    gc = gspread.authorize(credentials)  # authenticate with Google

    sh = gc.open_by_key(SAMPLE_SPREADSHEET_ID)
    I = 1
    KEY_LIST = []
    for I in range(1,5):
        worksheet = sh.get_worksheet(I)

        # print(values_list)
        # loop through colums
        rows = worksheet.row_values(1)
        FRENCH_KEY = 0
        FILE_NAME_KEY = 0
        i = 0
        for roww in rows:
            # print roww
            i += 1
            if "French" in roww:
                FRENCH_KEY = i
                #print roww
            if "Recording Filename" in roww:
                FILE_NAME_KEY = i
                #print roww

        #print FRENCH_KEY, FILE_NAME_KEY
        files_list = worksheet.col_values(FILE_NAME_KEY)
        french_list = worksheet.col_values(FRENCH_KEY)
        for i in range(1, len(files_list)):
            #print files_list[i], french_list[i]
            KEY_LIST.append([files_list[i].strip(), french_list[i].strip().replace("\"","'")])
        # print values_list
        # find filename, french keys

        # loop through data

        # create keys

        # print(sheets)

    #print KEY_LIST
    print_tokens(KEY_LIST)



def print_tokens(rows):
    print "<?php "
    print "return [",

    for row in rows:
        try:
            print "\"%s\"       =>      \"%s\","%(row[0],row[1])
        except Exception as e:
            #print e
            #print row[0],row[1]
            a=1

    print "];"
    print ""

if __name__ == '__main__':
    main()
