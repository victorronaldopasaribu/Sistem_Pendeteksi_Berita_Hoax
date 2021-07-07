import pandas as pd
import re
from Koneksi import mydb
from sklearn.metrics import accuracy_score, precision_score
from ConfusionMatrix import confusionMatrix
from Pra_Pengolahan import pre_process as pp
import Tampilan as tm
import time

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM `clean_news`")
myresult = mycursor.fetchall()

file = open("stopwords.txt","r");
st = file.read()
stopwords = pp.stopwords(st)

def classifier():
    lrows = []
    for row in myresult:
        lrows.append(list(row))
    df = pd.DataFrame(lrows, dtype=object)
    
    tsize = tm.getFold()
    
    #Menentukan fold : tsize 0.60 --> data uji = 300
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test =train_test_split(df[1],df[2],test_size=tsize,random_state=100,shuffle=True)
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords, max_df=0.7)
    tfidf_train = tfidf_vectorizer.fit_transform(X_train.values)
    tfidf_test = tfidf_vectorizer.transform(X_test)
    #print(tfidf_train)
    
    from sklearn.naive_bayes import MultinomialNB
    import sklearn.metrics as metrics
    from sklearn import svm
    
    nb_classifier = MultinomialNB(alpha=0.1)
    start_time1 = time.clock()
    nb_classifier.fit(tfidf_train,y_train)
    #print("NB : ",round(time.clock() - start_time1,5), "seconds")
    start_time2 = time.clock()
    pred = nb_classifier.predict(tfidf_test)
    #print("NB : ",round(time.clock() - start_time2,5), "seconds")
     
    SVM = svm.SVC(gamma='auto')
    start_time3 = time.clock()
    SVM.fit(tfidf_train,y_train)
    #print("SVM : ",round(time.clock() - start_time3,5), "seconds")
    start_time4 = time.clock()
    pred2 = SVM.predict(tfidf_test)
    #print("SVM : ",round(time.clock() - start_time4,5), "seconds")

    # Menghitung skor accuracy mlearning
    score1 = metrics.accuracy_score(y_test,pred)
    score2 = metrics.accuracy_score(y_test,pred2)

    ac = score1*100
    print("Accuracy NB : ", round(score1*100,3) ,"%")
    #print("Accuracy SVM : ", round(score2*100,3) ,"%")
    #print("Precision : ", round(score2*100,3) ,"%")
    
    # Confusion matrix
    cm = metrics.confusion_matrix(y_test, pred, labels=['hoax','nonhoax'])
    print(cm)
    
    #Menghitung nilai recall, precision dan accuracy menggunakan Confusion Matrix
    vRecall = round(confusionMatrix.recall(cm, cm[0][0], cm[1][0])*1,2)
    vPrecision = round(confusionMatrix.precision(cm, cm[0][0], cm[0][1])*1,2)
    vAccuracy = round(confusionMatrix.acuracy(cm, cm[0][0], cm[1][1], cm[0][1], cm[1][0])*1,2)
    vFMeasure = round(confusionMatrix.fmeasure(cm, vRecall, vPrecision)*1,2)

   
    class_labels = nb_classifier.classes_
    #print("class_labels" , class_labels)
    print(" ")
    
    feature_names = tfidf_vectorizer.get_feature_names()
    #print("feature_names" , feature_names)
    print(" ")
    
    feat_with_weights = sorted(zip(nb_classifier.coef_[0], feature_names))
    
    #print(class_labels[0], feat_with_weights[:20])
    print(" ")
    
    #print(class_labels[0], feat_with_weights[-20:])
    
    tfidf_vectorizer = TfidfVectorizer(analyzer='word',stop_words=stopwords,lowercase = True)
    tfidf_vectorizer.fit_transform(X_train.values.tolist())
    #print(tfidf_vectorizer.vocabulary_)
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    vocab = tfidf_vectorizer.vocabulary_
    tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords,vocabulary=vocab)
    
    mycursor2 = mydb.cursor()
    mycursor2.execute("SELECT * FROM `proses_testing`")
    myresult2 = mycursor2.fetchall()
    length = len(list(myresult2))
    #print("teksnya :"+myresult2[length-1][1])
    x = str(myresult2[length-1][1])
    x=[x,]
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    tfidf_vectorizer = TfidfVectorizer(stop_words=stopwords, max_df=0.7)
    tfidf_train = tfidf_vectorizer.fit_transform(X_train)
    tfidf_test = tfidf_vectorizer.transform(x)
    codes_list = ['hoax','nonhoax']
    
    nb_classifier = MultinomialNB(alpha=0.1)
    nb_classifier.fit(tfidf_train,y_train)
    tfidf_test = tfidf_vectorizer.transform(x)
    pred = nb_classifier.predict(tfidf_test)
    
    pred
    
    start = "\033[1m"
    end = "\033[0;0m"
    print('Berita Anda Adalah  ' + start + str(pred) + end)

    return pred, vRecall, vPrecision, vAccuracy, vFMeasure, cm[0][0], cm[1][1], cm[0][1], cm[1][0]