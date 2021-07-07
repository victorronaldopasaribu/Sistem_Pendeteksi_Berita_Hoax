from connect import mydb
from Pra_Pengolahan import pre_process

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM `news` WHERE label IN ('NON HOAX')")

myresult = mycursor.fetchall()

word = " "
temp = []
result_text = []
for i in range(len(myresult)):
    text = myresult[i][2]
    pr = pre_process()
    lower_text = pr.to_lower(text)
    sentence_tokens = pr.sentence_tokenize(lower_text)
    for each_sent in sentence_tokens:
        lemmatizzed_sent = pr.lemmatize(each_sent)
        clean_text = pr.remove_numbers(lemmatizzed_sent)
        clean_text = pr.remove_punct(clean_text)
        clean_text = pr.remove_Tags(clean_text)
        clean_text = pr.remove_single_char(clean_text)
        clean_text = pr.remove_stopwords(clean_text)
        word_tokens = pr.word_tokenize(clean_text)
        print(word_tokens)
        
    temp.append(word.join(pr.pre_process(text)))
    result_text.append(pr.stem(temp[i]))
    
    val = [(result_text[i],'nonhoax')]
  
    query = "insert into `clean_news`(`teksBerita`,`label`) values (%s,%s)"
    
    mycursor = mydb.cursor()
    mycursor.executemany(query, val)
    mydb.commit()
    
#print('Hasil Text Processing '+str(i)+': '+temp[6])
        