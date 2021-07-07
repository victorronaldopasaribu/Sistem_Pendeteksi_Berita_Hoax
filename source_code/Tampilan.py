import tkinter as tk
from tkinter import Tk, BOTH, X
from tkinter.ttk import Frame, Entry
from tkinter import scrolledtext
from tkinter import messagebox

from Koneksi import mydb

import NaiveBayes as naiv
        
mycursor = mydb.cursor()

rslt = ""
global rsltt 
rsltt = 10

class frameApp(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.init_UI()
        self.countWord()
    
    def init_UI(self):
        
        root.geometry("1000x350+350+200")
        root.title("Sistem Pendeteksi Berita Hoax")
        
        self.label1 = tk.Label(root, text='Sistem Pendeteksi Berita Hoax', font="Verdana 20").grid(row=2, column=3)
        
        self.label3 = tk.Label(root, text='Masukkan Fold (k=10%) :', font="Verdana 10").grid(row=3)
        
        self.infold = Entry(root, width = 5)
        self.infold.place(x=180, y=40)
        
        tk.Button(root, text='Cek Akurasi',fg="black", bg="skyblue", command=self.checkAccuracy, width=10).grid(row=4, padx=5, pady=5)
        
        self.label2 = tk.Label(root, text='Hasil Uji :', font="Verdana 10").place(x=0, y=100)
        
        self.label4 = tk.Label(root, text='TP', font="Verdana 10").place(x=0, y=130)
        self.otp = tk.Label(root, text='', width = 4, borderwidth=2, relief="groove")
        self.otp.place(x=25, y=130)
        
        self.label5 = tk.Label(root, text='TN', font="Verdana 10").place(x=0, y=155)
        self.otn = tk.Label(root, text='', width = 4, borderwidth=2, relief="groove")
        self.otn.place(x=25, y=155)
        
        self.label6 = tk.Label(root, text='FP', font="Verdana 10").place(x=0, y=180)
        self.ofp = tk.Label(root, text='', width = 4, borderwidth=2, relief="groove")
        self.ofp.place(x=25, y=180)
        
        self.label8 = tk.Label(root, text='FN', font="Verdana 10").place(x=0, y=205)
        self.ofn = tk.Label(root, text='', width = 4, borderwidth=2, relief="groove")
        self.ofn.place(x=25, y=205)
        
        self.label9 = tk.Label(root, text='Recall', font="Verdana 10").place(x=62, y=130)
        self.rc = tk.Label(root, text='', width = 4, borderwidth=2, relief="groove")
        self.rc.place(x=130, y=130)
        
        self.label10 = tk.Label(root, text='Precision', font="Verdana 10").place(x=62, y=155)
        self.pr = tk.Label(root, text='', width = 4, borderwidth=2, relief="groove")
        self.pr.place(x=130, y=155)
        
        self.label11 = tk.Label(root, text='Accuracy', font="Verdana 10").place(x=62, y=180)
        self.ac = tk.Label(root, text='', width = 4, borderwidth=2, relief="groove")
        self.ac.place(x=130, y=180)
        
        self.label12 = tk.Label(root, text='FMeasure', font="Verdana 10").place(x=62, y=205)
        self.fm = tk.Label(root, text='', width = 4, borderwidth=2, relief="groove")
        self.fm.place(x=130, y=205)
        
        self.label7 = tk.Label(root, text='Masukkan teks berita (maks=5000 karakter) :', font="Verdana 10").grid(row=4, column=3)
        
        self.inputtxt = scrolledtext.ScrolledText(root, wrap = tk.WORD, width = 80, height = 8, font = ("Verdana", 12)) 
        self.inputtxt.grid(row=5, column=3)
        
        tk.Button(root, text='Cek Berita',fg="black", bg="skyblue", command=self.processCheck, width=10).place(x=700, y=250)
        tk.Button(root, text='Hapus Berita',fg="black", bg="skyblue", command=self.processClear, width=10).place(x=800, y=250)
        tk.Button(root, text='Keluar',fg="black", bg="darkred", command=root.destroy, width=10).place(x=900, y=250)
        
        self.label13 = tk.Label(root, text='Jumlah karakter', font="Verdana 10")
        self.label13.place(x=163, y=250)
        self.jk = tk.Label(root, text='0', width = 8, borderwidth=2, relief="groove")
        self.jk.place(x=275, y=250)
        
        
        self.label14 = tk.Label(root, text='Jenis Berita', fg="black", font="Verdana 10")
        self.label14.place(x=163, y=280)
        self.hsl = tk.Label(root, text='', width = 15, borderwidth=2, relief="groove")
        self.hsl.place(x=250, y=280)
        
    def countWord(self):
        rslt = self.inputtxt.get("1.0","end")
        return(len(rslt)-1)
        
    def checkAccuracy(self):
        global rsltt
        rsltt = self.infold.get()
        text_file = open("fold.txt", "w")
        text_file.write(rsltt)
        text_file.close()
        print(rsltt)
        tp = naiv.classifier()[5]
        self.otp.config(text=str(tp))
        tn = naiv.classifier()[6]
        self.otn.config(text=str(tn))
        fp = naiv.classifier()[7]
        self.ofp.config(text=str(fp))
        fn = naiv.classifier()[8]
        self.ofn.config(text=str(fn))
        
        vRecall = naiv.classifier()[1]
        vPrecision = naiv.classifier()[2]
        vAccuracy = naiv.classifier()[3]
        vFMeasure = naiv.classifier()[4]
        
        self.rc.config(text=str(vRecall))
        self.pr.config(text=str(vPrecision))
        self.ac.config(text=str(vAccuracy))
        self.fm.config(text=str(vFMeasure))
        
        file = open("fold.txt","r+")
        file.truncate(0)

    def processCheck(self):
        rslt = self.inputtxt.get("1.0","end")
        print(rslt)
        print("LENGTH : ",len(rslt))
        text_file = open("input.txt", "w")
        text_file.write(rslt)
        text_file.close()
        if len(rslt) <= 5000:
            if len(rslt) == 1:
                messagebox.showerror("Error", "Teks Berita Masih Kosong!!")
            else: 
                query = "insert into `testing_news`(`teksBerita`) values (%s)"
                mycursor = mydb.cursor()          
                mycursor.execute(query, (rslt,))
                mydb.commit()
                from Pra_Pengolahan import pre_process as pp
                pp.pre_processTest()
                pred = naiv.classifier()[0]
                print("prediksi:"+str(pred))
                
                if str(pred) == "['nonhoax']":
                    self.hsl.config(text='NON HOAX', fg="green")
                else:
                    self.hsl.config(text='HOAX', fg="red")
        else:
            messagebox.showerror("Error", "Berita anda lebih dari 5000 kata")
            
        self.jk.config(text=str(len(rslt)-1))
        print(naiv.classifier()[4])
      
    def processClear(self):
        self.inputtxt.delete("1.0", "end")
        self.jk.config(text='0')
        self.hsl.config(text='')
        file = open("input.txt","r+")
        file.truncate(0)


def getFold():
    global rsltt
    file = open("fold.txt","r");
    st = file.read()
    if len(st)==0:
        vlue = rsltt
    else:
        rsltt = st
        vlue = rsltt
    return float(int(vlue)/100)     

        
if __name__ == '__main__':
    root = Tk()
    app = frameApp(root)
    root.mainloop()
 
   