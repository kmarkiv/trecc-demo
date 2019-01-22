import io
import os.path
import sqlite3

import sox
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1 import types

GS_FILE = "lexi-dev-64e930423c37.json"

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GS_FILE
file = open(GS_FILE, "r")
GOOGLE_CLOUD_SPEECH_CREDENTIALS = file.read()

encoding = enums.RecognitionConfig.AudioEncoding.FLAC
sample_rate_hertz = 44100
language_code = 'fr-FR'
config3 = {'language_code': language_code,
           'encoding': enums.RecognitionConfig.AudioEncoding.LINEAR16}

DEBUG = 1
USER_ID = 4

dirs = [""]
DIR = "/Users/vkamath/Downloads/Fabrice/"
databases = ["adult", "core", "number", "question"]
database_names = ["adult", "core", "numbers", "questions"]
database_keys = ["FileName", "FileName", "FileName,Spelling", "FileName"]
FILE_NAMES = ["AdultSupporterContent", "CoreProductContent", "PhonenumberSpelling", "Questions"]
CLEAN_DIR = "CleanFiles"
client = speech.SpeechClient()
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    language_code=language_code,
    sample_rate_hertz=sample_rate_hertz)


def get_db(database):
    conn = sqlite3.connect("csv_content/%s.db" % database)
    c = conn.cursor()
    return c, conn


def transcribe_audio():
    I = 4
    try:
        alter_db(I)
    except Exception as e:
        print e

    conn, c = get_db(databases[I])
    conn.execute("SELECT %s FROM %s LIMIT 1 " % (database_keys[I], database_names[I]))
    rows = conn.fetchall()
    for row in rows:
        #print row
        audio_file = "%s%s/%s.wav" % (DIR, FILE_NAMES[I], row[0])
        audio_file = copy_files(audio_file, row[0])
        print audio_file

        if os.path.isfile(audio_file):
            with io.open(audio_file, 'rb') as audio_file2:
                content = audio_file2.read()
            audio_data = types.RecognitionAudio(content=content)
            # try:
            response = client.recognize(config, audio_data)

            transcript = "-1"
            confidence = 0
            if len(response.results):
                    result = response.results[0]
                    if result.alternatives:
                        transcript = result.alternatives[0].transcript
                        confidence = result.alternatives[0].confidence
            print response

            #score = get_jaccard_sim()

            sql = "UPDATE " + database_names[I] + " SET transcript=?,confidence=? WHERE Filename=? "
            print sql
            conn.execute(sql, (transcript, confidence, row[0]))
            c.commit()

            # except Exception as e:
            #    print e

            # exit()

def cleaning(text):

    import string
    exclude = set(string.punctuation)

    import re
    # remove new line and digits with regular expression
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\d', '', text)
    # remove patterns matching url format
    url_pattern = r'((http|ftp|https):\/\/)?[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?'
    text = re.sub(url_pattern, ' ', text)
    # remove non-ascii characters
    text = ''.join(character for character in text if ord(character) < 128)
    # remove punctuations
    text = ''.join(character for character in text if character not in exclude)
    # standardize white space
    text = re.sub(r'\s+', ' ', text)
    # drop capitalization
    text = text.lower()
    #remove white space
    text = text.strip()

    return text

def get_jaccard_sim(str1, str2):
    a = set(str1.split())
    b = set(str2.split())
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def alter_db(I):
    conn, c = get_db(databases[I])
    sql = "alter table %s add column transcript text" % (database_names[I])
    print sql
    conn.execute(sql)
    c.commit()
    sql = "alter table %s add column confidence text" % (database_names[I])
    conn.execute(sql)
    c.commit()
    sql = "alter table %s add column score text" % (database_names[I])
    conn.execute(sql)
    c.commit()


def copy_files(file_name, file):
    tfm = sox.Transformer()
    tfm.convert(samplerate=44100)
    new_file = "%s%s/%s.wav" % (DIR, CLEAN_DIR, file)
    tfm.build(file_name, new_file)
    return new_file


if __name__ == "__main__":
    transcribe_audio()
