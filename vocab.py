import sqlite3
import en_core_web_sm
from sqlite3 import OperationalError
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES

reading_score = []
nlp = en_core_web_sm.load()
conn = sqlite3.connect("reading_level")
cursor = conn.cursor()
try:
    cursor.execute('''CREATE TABLE words(word text,lemma text, pos text, class number, chapter number)''')
except OperationalError:
    None

a = [[1,4,5,7,8],[1,2,4,5,7,8],[1,2,4,7,8],[1,2,4,5,7,8],[1,2,4,5,7],[1,2,4,5,8],
     [1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],[1,2,3,4,5,6,7,8,9,10,11,12],
     [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],
     [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34],
     [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34]]

state1 = 'SELECT * FROM words WHERE word='#+word
state2 = 'INSERT INTO words VALUES'# ('kamal','NN',1,1)
state3 = 'INSERT INTO levels VALUES'# ('33',1,1)
#for token in doc:

lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
for i in range(1,13):
    for j in range(len(a[i-1])):
        class_no = i
        chapter_no = a[i-1][j]
        file_name = "class"+str(class_no)+"_chapter"+str(chapter_no)+".txt"
        class_folder = "class"+str(class_no)
        file_full_path = "books_txt/"+ class_folder + "/" + file_name
        print(file_full_path)
        file = open(file_full_path).read()
        file = file.replace("’"," ")
        file = file.replace("'", " ")
        doc = nlp(file)
        # score = textstat.flesch_reading_ease(file)
        # ro = "INSERT INTO levels VALUES (%d, %d, %d)" % (score, class_no, chapter_no)
        # print(ro)
        #cursor.execute(ro)
        #conn.commit()
        #waste’
        for token in doc:
            if token.pos_ != 'PUNCT':
                # ro = state1 + "'" + token.text+ "'"
                print(token.pos_)
                print(token.text)
                wo = token.text.lower()
                lem = token.lemma_.lower()
                lemma_word = lemmatizer(wo, token.pos_)
                ro = '''SELECT * FROM words WHERE lemma ="%s"''' % lemma_word
                cursor.execute(ro)
                result = cursor.fetchall()
                if len(result) == 0:
                    #wo = token.text.lower()
                    ro = '''INSERT INTO words VALUES ("%s","%s","%s", %d, %d)''' % (wo,lem, token.pos_, class_no, chapter_no)
                    print(ro)
                    cursor.execute(ro)
                    conn.commit()





conn.close()

# 2 NN,VB, FW, 2 JJ, 2 RB
# file = open("books_txt/class8/class1_chapter1.txt").read()
# doc = nlp(file)
# sentences= list(doc.sents)
# state1 = 'SELECT * FROM words WHERE word='#+word
# state2 = 'INSERT INTO words VALUES'# ('kamal',1,1)
# for sent in sentences:
#     score = textstat.flesch_reading_ease(sent)
#     # reading_score.append(score)
#     for token in sent:
#         a,b,c = (token.text, token.pos_, token.tag_)
#         tag_list = ['NN','VB','FW','JJ','RB']
#         if token.tag_[:2] in tag_list:
#             exe = state1+'"'+token.text+'"'
#             print (exe)
#             cursor.execute(str(exe))
#             result = cursor.fetchall()
#             if len(result) == 0:
#                 second = "(" +'"'+ token.text+'"'+","+"'"+token.pos_+"'"+","+"'8'"+","+"'1'"+")"
#                 exe = state2 +second
#                 print (exe)
#                 cursor.execute(exe)
#                 conn.commit()
#
# #print (mean(reading_score))
# #f = io.open("data/class8/1.txt", mode="r", encoding="utf-8")
# #open(Filename, 'r', encoding='utf-8')
# conn.close()
#lower
# https://stackoverflow.com/questions/38763007/how-to-use-spacy-lemmatizer-to-get-a-word-into-basic-form
#save state and follow