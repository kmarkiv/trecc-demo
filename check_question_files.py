import os.path
import sqlite3

DEBUG = 1
USER_ID = 4

dirs = [""]


def get_db():
    conn = sqlite3.connect('csv_content/question.db')
    c = conn.cursor()
    return c, conn


def debug(message):
    if DEBUG:
        print "DEBUG: ", message


def check_file(file_path):
    # print file_path
    file_path = "/Users/vkamath/Downloads/Fabrice/Questions/" + file_path + ".wav"
    # print file_path
    if os.path.isfile(file_path):
        return True
    return False


def clear_content_info():
    conn, c = get_db()
    conn.execute("UPDATE questions SET Recorded=0")
    c.commit()
    # conn.commit()


def update_content_info(conn, row):
    print row
    conn.execute("UPDATE questions SET Recorded=1 WHERE Filename=?", (row,))
    # conn.commit()


def update_content_data():
    # get child unit
    conn, c = get_db()

    # table mirrors metabase users_to_units table
    conn.execute("SELECT Filename, Recorded FROM questions")
    rows = conn.fetchall()
    for row in rows:
        #print row
        for d in dirs:
            if check_file(d + row[0]):
                update_content_info(conn, row[0])
                c.commit()

    return True


def get_stats():
    conn, c = get_db()
    conn.execute("SELECT COUNT (*) FROM questions")
    stuff = conn.fetchone()
    total = stuff[0]
    conn.execute("SELECT COUNT (*) FROM questions WHERE Recorded=1 ")
    stuff = conn.fetchone()
    sound = stuff[0]
    print sound, "/", total


if __name__ == "__main__":
    clear_content_info()
    update_content_data()
    get_stats()
