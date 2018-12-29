import sqlite3
from random import randint

DEBUG = 1
USER_ID = 4

def get_db():
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    return c


def get_content_db():
    conn = sqlite3.connect('content.db')
    c = conn.cursor()
    return c


def get_child_unit(user_id):
    # get child unit
    conn = get_db()

    # table mirrors metabase users_to_units table
    conn.execute("SELECT unit_id FROM user_units WHERE user_id=%s AND current='true'" % user_id)
    unit_id = conn.fetchone()[0]
    debug("CURRENT UNIT = %s"%unit_id)
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
        debug("Question_Type Scores")
        debug(units)
        debug("Difficult Question_Type = %s"%units[0][0])
    return units[0][0]


def debug(message):
    if DEBUG:
        print "DEBUG: ", message


def head(message):
    print "##"*20
    print message
    print "##" * 20

def play(message):
    conn = get_content_db()
    conn.execute("SELECT * FROM parents WHERE ContentID='%s' " % message)
    data = conn.fetchone()
    debug("CONTENTID %s"%message)
    debug(data)
    debug("playing message ... %s "%message)
    if data:
        print "  ",data[6]
    else:
        print " PLAY (%s)" % message
    print " "
    return


def lesson_support_options_difficult():
    UNIT_ID = get_child_unit(USER_ID)
    QUESTION_TYPE_ID = get_difficult_question_type_for_unit(USER_ID, UNIT_ID)

    play("QuestionSummary_%s_%s" % (UNIT_ID, QUESTION_TYPE_ID))

    # play from Syllabus
    play("EXAMPLE_QUESTION_TYPE_UNIT_%s_QUESTION_TYPE_%s" % (UNIT_ID, QUESTION_TYPE_ID))
    # play from Syllabus
    play("HINT_UNIT_%s_QUESTION_TYPE_%s" % (UNIT_ID, QUESTION_TYPE_ID))


def lesson_support_options_suggestion():
    SUGGESTION = randint(1, 5)
    play("SupportSuggestion_%s" % (SUGGESTION))


if __name__ == "__main__":
    head("Lesson Support - Difficult Questions")
    lesson_support_options_difficult()

    head("Lesson Support - Suggestion")
    lesson_support_options_suggestion()

"""

# output expected

########################################
Lesson Support - Difficult Questions
########################################
DEBUG:  CURRENT UNIT = 4
DEBUG:  Question_Type Scores
DEBUG:  [(3, 0.2), (4, 0.3333333333333333), (7, 0.6), (5, 0.8)]
DEBUG:  Difficult Question_Type = 3
DEBUG:  CONTENTID QuestionSummary_4_3
DEBUG:  (None, u'16', u'QuestionSummary', u'QuestionSummary_4_3', 4, 3, u'In this unit.. your child is having the most difficulty with naming the sound that two letters make when combined', u"Bonjour.. et bienvenue aux cours d'alphab\xe9tisation Allo Alphabet fran\xe7ais!", u'Kaja.. does this seem right?', u'CMU,', None, None, None, None, None)
DEBUG:  playing message ... QuestionSummary_4_3 
   In this unit.. your child is having the most difficulty with naming the sound that two letters make when combined
 
DEBUG:  CONTENTID EXAMPLE_QUESTION_TYPE_UNIT_4_QUESTION_TYPE_3
DEBUG:  None
DEBUG:  playing message ... EXAMPLE_QUESTION_TYPE_UNIT_4_QUESTION_TYPE_3 
 PLAY (EXAMPLE_QUESTION_TYPE_UNIT_4_QUESTION_TYPE_3)
 
DEBUG:  CONTENTID HINT_UNIT_4_QUESTION_TYPE_3
DEBUG:  None
DEBUG:  playing message ... HINT_UNIT_4_QUESTION_TYPE_3 
 PLAY (HINT_UNIT_4_QUESTION_TYPE_3)
 
########################################
Lesson Support - Suggestion
########################################
DEBUG:  CONTENTID SupportSuggestion_3
DEBUG:  (None, u'17', u'SupportSuggestions', u'SupportSuggestion_3', None, None, u"Let your child know why you think it's important for them to learn to read in French!", u"Bonjour.. et bienvenue aux cours d'alphab\xe9tisation Allo Alphabet fran\xe7ais!", None, u'CMU,', None, None, None, None, None)
DEBUG:  playing message ... SupportSuggestion_3 
   Let your child know why you think it's important for them to learn to read in French!




"""
