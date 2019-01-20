#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

DEBUG = 1
USER_ID = 4

dirs = [""]
FILE_PATH = "/Users/vkamath/Downloads/Fabrice/Tokens_All/"

CORRECT_FILE_PATH = "/Users/vkamath/Downloads/Tokens_Clean/"

databases = ["adult.db", "core.db", "token.db"]
database_names = ["adult", "core", "tokens"]
database_keys = ["FileName", "FileName", "Phonetics,ID"]


def get_db(database):
    conn = sqlite3.connect('csv_content/' + database)
    c = conn.cursor()
    conn.text_factory = str
    return c, conn


def get_missing_keys(db, i):
    conn, c = get_db(db)
    files = "SELECT %s FROM %s WHERE Recorded=0" % (database_keys[i], database_names[i])
    # print files
    conn.execute(files)
    rows = conn.fetchall()
    return rows


def get_missing_token_names(rows):
    conn, c = get_db("syllabus.db")
    keys = []
    nums = []
    for row in rows:
        # print row[1]
        files = "SELECT ID,Name FROM syllabus WHERE ID=%s" % (row[1])
        # print files
        conn.execute(files)
        row = conn.fetchone()
        keys.append([row[1]])
        nums.append([row[0]])
    print_tokens(nums, "token_keys", True)
    return keys


def print_tokens(rows, file_name, is_int=False):
    print "$%s_missing_keys =array(" % file_name,

    for row in rows:
        if not is_int:
            print '"' + row[0] + '",',
        else:
            print "%s," % row[0],

    print ");"
    print ""


def get_array():
    i = 0
    all_keys = []
    for db in databases:
        rows = get_missing_keys(db, i)
        if i == 2:
            rows = get_missing_token_names(rows)
        all_keys.extend(rows)
        print rows

        print_tokens(rows, database_names[i], )

        i += 1
    print_tokens(all_keys, "all")


# def get_missing_token():


if __name__ == "__main__":
    get_array()
