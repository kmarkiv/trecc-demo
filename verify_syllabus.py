import os.path
import sqlite3

DEBUG = 1
USER_ID = 4

dirs = [""]
FILE_PATH = "/Users/vkamath/Downloads/Tokens_Clean/"


def get_db():
    conn = sqlite3.connect('csv_content/syllabus.db')
    c = conn.cursor()
    return c, conn


def get_token_db():
    conn = sqlite3.connect('csv_content/token.db')
    c = conn.cursor()
    conn.text_factory = str
    return c, conn


def debug(message):
    if DEBUG:
        print "DEBUG: ", message


def check_file(file_path):
    # print file_path
    file_path = FILE_PATH + file_path + ".wav"
    # print file_path
    if os.path.isfile(file_path):
        return True
    return False


def clear_content_info():
    conn, c = get_db()
    conn.execute("UPDATE syllabus SET Recorded=0")
    c.commit()
    # conn.commit()


def update_content_info(conn, row):
    # print row
    conn.execute("UPDATE syllabus SET Recorded=1 WHERE Filename=?", (row,))
    # conn.commit()


def update_content_data():
    # get child unit
    conn, c = get_db()

    # table mirrors metabase users_to_units table
    conn.execute("SELECT Name,Phonetics_auditory FROM syllabus")
    rows = conn.fetchall()
    for row in rows:
        # print row
        for d in dirs:
            if check_file(d + row[0]):
                # update_content_info(conn, row[0])
                # c.commit()
                r = 3
            else:
                conn, c = get_token_db()
                conn.execute("SELECT Phonetics, Recorded,ID FROM tokens WHERE Recorded =1 AND Phonetics=?", (row[1],))

                rows = conn.fetchone()
                if rows:
                    print row[0],row[1]
                    print "Error"
                #print row[0]

    return True


def get_stats():
    conn, c = get_db()
    conn.execute("SELECT COUNT (*) FROM syllabus")
    stuff = conn.fetchone()
    total = stuff[0]
    conn.execute("SELECT COUNT (*) FROM syllabus WHERE Recorded=1 ")
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

        # table mirrors metabase users_to_units table
        token = file.replace(".wav", "")
        # print token
        conn.execute("SELECT * FROM syllabus WHERE Name=?", (token,))

        rows = conn.fetchone()
        # print rows
        if not rows:
            print token, " ERROR"

    return 0


if __name__ == "__main__":
    # clear_content_info()
    update_content_data()
    # get_stats()
    # check_directory()
