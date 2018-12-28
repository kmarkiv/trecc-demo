# questions with lowest average score

import sqlite3

DEBUG = 1


def get_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    return c


def get_child_unit(user_id):
    # get child unit
    conn = get_db()

    # table mirrors metabase users_to_units table
    conn.execute("SELECT unit_id FROM user_units WHERE user_id=%s AND current='true'" % user_id)
    unit_id = conn.fetchone()[0]
    if DEBUG:
        print "CURRENT UNIT = ", unit_id
    return unit_id


def get_difficult_question_type_for_unit(user_id, unit_id):
    # get difficult question_type

    conn = get_db()

    # table mirrors metabase answer_stats table
    conn.execute(
        "SELECT trial_id,AVG(correct) as correct_avg FROM answer_stats WHERE user_id=%s AND unit_id=%s "
        "GROUP BY trial_id ORDER BY correct_avg ASC" % (
            user_id, unit_id))
    units = conn.fetchall()
    # print units
    # return most difficult question type
    if DEBUG:
        print "Question_Type Scores", units
        print "Difficult Question_Type = ", units[0][0]
    return units[0][0]


def play(message):
    # @todo connect to spread sheet
    print "playing message ... ", message
    return


def lesson_support_struggle():

    USER_ID = 4
    # debug user id
    UNIT_ID = get_child_unit(USER_ID)

    QUESTION_TYPE_ID = get_difficult_question_type_for_unit(USER_ID, UNIT_ID)

    play("QUESTION_SUMMARY_UNIT_%s_QUESTION_TYPE_%s" % (UNIT_ID, QUESTION_TYPE_ID))
    play("EXAMPLE_QUESTION_TYPE_UNIT_%s_QUESTION_TYPE_%s" % (UNIT_ID, QUESTION_TYPE_ID))
    play("HINT_UNIT_%s_QUESTION_TYPE_%s" % (UNIT_ID, QUESTION_TYPE_ID))


if __name__ == "__main__":
    lesson_support_struggle()

"""

# output expected

CURRENT UNIT =  4
Question_Type Scores [(3, 0.2), (4, 0.3333333333333333), (7, 0.6), (5, 0.8)]
Difficult Question_Type =  3
playing message ...  QUESTION_SUMMARY_UNIT_4_QUESTION_TYPE_3
playing message ...  EXAMPLE_QUESTION_TYPE_UNIT_4_QUESTION_TYPE_3
playing message ...  HINT_UNIT_4_QUESTION_TYPE_3



"""