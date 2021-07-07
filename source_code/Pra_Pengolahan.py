import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from string import punctuation
from autocorrect import spell
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Koneksi import mydb


wordnet_lemmatizer = WordNetLemmatizer()

file = open("stopwords.txt","r");
st = file.read()

class pre_process:
    def __int__(self):
        pass

    def autospell(self,text):
        spells = [spell(w) for w in (nltk.word_tokenize(text))]
        return " ".join(spells)

    def to_lower(self,text):
        return text.lower()

    def remove_numbers(self,text):
        output = ''.join(c for c in text if not c.isdigit())
        return output

    def remove_punct(self,text):
        return ''.join(c for c in text if c not in punctuation)

    def remove_Tags(self,text):
        cleaned_text = re.sub('<[^<]+?>', '', text)
        return cleaned_text

    def sentence_tokenize(self,text):
        sent_list = []
        for w in nltk.sent_tokenize(text):
            sent_list.append(w)
        return sent_list
    
    def remove_single_char(self, text):
        return re.sub(r"\b[a-zA-Z]\b", "", text)

    def word_tokenize(self,text):
        return [w for sent in nltk.sent_tokenize(text) for w in nltk.word_tokenize(sent)]

    def remove_stopwords(self,sentence):
        stop_words = stopwords.words('indonesian')
        return ' '.join([w for w in nltk.word_tokenize(sentence) if not w in stop_words])
    
    def stopwords(text):
    	reg = re.compile(r"\n")
    	return reg.split(text)

    def stem(self,text):
        factory = StemmerFactory()
        stemmer = factory.create_stemmer()
        return "".join(stemmer.stem(text))

    def lemmatize(self,text):
        lemmatized_word = [wordnet_lemmatizer.lemmatize(word)for sent in nltk.sent_tokenize(text)for word in nltk.word_tokenize(sent)]
        return " ".join(lemmatized_word)

    def pre_process(self,text):
        #lower_text = self.to_lower(text)
        sentence_tokens = self.sentence_tokenize(self.to_lower(text))
        word_list = []
        for each_sent in sentence_tokens:
            lemmatizzed_sent = self.lemmatize(each_sent)
            clean_text = self.remove_numbers(lemmatizzed_sent)
            clean_text = self.remove_punct(clean_text)
            clean_text = self.remove_Tags(clean_text)
            clean_text = self.remove_single_char(clean_text)
            clean_text = self.remove_stopwords(clean_text)
            word_tokens = self.word_tokenize(clean_text)
            for i in word_tokens:
                word_list.append(i)
        return word_list
    
    def pre_processTest():
        mycursor = mydb.cursor()
    
        mycursor.execute("SELECT * FROM `testing_news`")
        
        myresult = mycursor.fetchall()
        word = " "
        temp = []
        result_text = []
        length = len(list(myresult))
        text = myresult[length-1][1]
        for i in range(1):
            pr = pre_process()   
            temp.append(word.join(pr.pre_process(text)))
            result_text.append(pr.stem(temp[i]))
            
            val = [(result_text[i])]
          
            query = "insert into `proses_testing`(`teksBerita`) values (%s)"
            
            mycursor = mydb.cursor()
            mycursor.executemany(query, val)
            mydb.commit()
    
    