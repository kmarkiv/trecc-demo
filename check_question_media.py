import mysql.connector
from slugify import slugify

cnx = mysql.connector.connect(user='', password='',
                              host='',
                              database='')
cursor = cnx.cursor()

media_query = ("SELECT name FROM media")
cursor.execute(media_query)

FILE_NAMES = []
for (name,) in cursor:
    FILE_NAMES.append(name)

FILE_NAMES.append("silence")
MISSING_KEYS = []
MISSING_QUESTION_KEYS = []
media_query = ("SELECT question_recordings,id,trial_id FROM cms_questions")
#media_query = ("SELECT option_text,id,question_id FROM cms_options WHERE correct=1")
#media_query = ("SELECT soundfile_name,id,id FROM cms_tokens")

cursor.execute(media_query)
for (question_recordings, question_id, trial_id) in cursor:
    # print question_recordings
    # recording_list = [question_recordings]
    recording_list = eval(question_recordings)
    for recording in recording_list:
        r = slugify(recording, separator='_')
        if (r not in FILE_NAMES) and (len(r) > 0):
            print r, recording, question_recordings, question_id, trial_id
            MISSING_KEYS.append(r)
            MISSING_QUESTION_KEYS.append(question_id)

MISSING_KEYS_SET = set(MISSING_KEYS)

print MISSING_QUESTION_KEYS
print len(MISSING_QUESTION_KEYS), ": Questions with missing Keys"
print MISSING_KEYS_SET
print len(MISSING_KEYS_SET), ": Missing Files "
