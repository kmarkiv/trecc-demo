#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os.path
import sqlite3
from shutil import copyfile

DEBUG = 1
USER_ID = 4

dirs = [""]
FILE_PATH = "/Users/vkamath/Downloads/Fabrice/Tokens_All/"

CORRECT_FILE_PATH = "/Users/vkamath/Downloads/Tokens_Clean/"


def get_db():
    conn = sqlite3.connect('csv_content/token.db')
    c = conn.cursor()
    conn.text_factory = str
    return c, conn


def get_syllabus_db():
    conn = sqlite3.connect('csv_content/syllabus.db')
    c = conn.cursor()
    conn.text_factory = str
    return c, conn


def debug(message):
    if DEBUG:
        print "DEBUG: ", message


def copy_file(file_path, new_file_path):
    new_file_path.replace(" ","")
    correct_file_path = FILE_PATH + file_path + ".wav"
    new_file_path = CORRECT_FILE_PATH + new_file_path + ".wav"
    import os.path
    if not os.path.isfile(correct_file_path):
        print correct_file_path
    copyfile(correct_file_path, new_file_path)


def check_file(file_path):
    # print file_path
    file_path = FILE_PATH + file_path + ".wav"
    # print file_path
    if os.path.isfile(file_path):
        return True
    return False


def clear_content_info():
    conn, c = get_db()
    conn.execute("UPDATE tokens SET Recorded=0")
    c.commit()
    # conn.commit()


def get_file_name(token):
    conn, c = get_syllabus_db()
    c.text_factory = str
    conn.execute("SELECT Name,Phonetics_auditory,ID FROM syllabus WHERE Phonetics_auditory=?", (token,))
    rows = conn.fetchone()
    if rows:
        return rows[0]
    else:
        print token
        return False


def update_content_info(conn, row):
    # print row
    conn.execute("UPDATE tokens SET Recorded=1 WHERE Phonetics=?", (row,))
    # conn.commit()


def update_content_data():
    # get child unit
    conn, c = get_db()

    # table mirrors metabase users_to_units table
    conn.execute("SELECT Phonetics, Recorded,ID FROM tokens")
    rows = conn.fetchall()
    for row in rows:
        # print row
            if check_file(dirs[0] + row[0]):
                update_content_info(conn, row[0])
                c.commit()
                file = get_file_name(row[0])
                #print file, row[0]
                if file:
                    copy_file(row[0], file)
                else:
                    print "Error",row[0]
                    print "==============================="

    return True


def get_stats():
    conn, c = get_db()
    c.text_factory = str
    conn.execute("SELECT COUNT (*) FROM tokens")
    stuff = conn.fetchone()
    total = stuff[0]
    conn.execute("SELECT COUNT (*) FROM tokens WHERE Recorded=1 ")
    stuff = conn.fetchone()
    sound = stuff[0]
    print sound, "/", total


def check_directory():
    # check directory
    from os import walk

    f = []
    for (dirpath, dirnames, filenames) in walk(FILE_PATH):
        f.extend(filenames)

        break
    for file in f:
        conn, c = get_db()
        c.text_factory = str
        #conn.decode('utf8')

        # table mirrors metabase users_to_units table
        token = file.replace(".wav","")
        conn.execute("SELECT Phonetics, Recorded,ID FROM tokens WHERE Phonetics=?",(token,))

        rows = conn.fetchone()
        # print rows
        if not rows:
            print token," ERROR"

    return 0


if __name__ == "__main__":
    clear_content_info()
    update_content_data()
    get_stats()
    #check_directory()
