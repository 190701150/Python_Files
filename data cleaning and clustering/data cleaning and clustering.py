from tkinter import *
import tkinter.scrolledtext as tkst
import pandas as pd
from clusters import *

root=Tk()
root.title("Veri Ayiklama Ve Kumeleme")
class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()



    def initUI(self):
        self.pack()
        self.text = Label(self, text='Yandaki butonu kullanarak verilen dosyayı girebilirsiniz.')
        self.text.grid(column=2, columnspan=20) #10
        self.import_button = Button(self, text="Txt Dosya Sec",command = self.import_data)
        self.import_button.grid(row=0, column=5)

        self.text = Label(self, text="Kumeleme Ekrani", font="Impact 20")
        self.text.grid(row=1, column=2, columnspan=20)

        self.text1 = Label(self, text="2 Adet Kategori Secin:").grid(row=2, column=2)

        self.eleman_list = Listbox(self,width=40, selectmode=MULTIPLE)
        self.eleman_list.grid(row=3,column=2,rowspan=10)   #BU LİSTEYE KATEGORİLER EKLENECEKTİR!


        self.check = StringVar()
        self.category_check = Radiobutton(self, text='Hiyerarsik Kumeleme', value='1', variable=self.check).grid(row=3, column=3, sticky=W)
        self.company_check = Radiobutton(self, text='KMeans Kumeleme', value='2', variable=self.check).grid(row=7,column=3,sticky=W)
        self.check.set('3')

        self.text = Label(self, text='KMeans Kume Sayisi')
        self.text.grid(row=3, column=4)

        self.en = Entry(self)
        self.en.grid(row=7, column=4)

        self.kumebutton = Button(self, text="Kumele!",command = self.create_data)
        self.kumebutton.grid(row=5, column=10)                 #BU BUTONA KOMUT EKLENECEKTİR!

        self.Textbox1 = tkst.ScrolledText(self, width=94, height=20)
        self.Textbox1.grid(row=13, column=2,columnspan=20)
    def import_data(self):
        self.df = pd.read_csv("cust_seg.txt")
        for i in self.df:
            self.eleman_list.insert(END, i)

    def create_data(self):
        self.f = open('cust_seg.txt','r')
        first_pick = self.eleman_list.get(self.eleman_list.curselection()[0])
        second_pick = self.eleman_list.get(self.eleman_list.curselection()[1])
        maks = max(self.df[second_pick])
        sozluk = dict()
        features = self.f.readline()
        features = features[:-1].split(',')
        age = features.index(first_pick)
        edu = features.index(second_pick)
        for i in self.f.readlines():
            temp = i.strip('\n').split(',')
            sozluk.setdefault(float(temp[age]), {})
            for i in range(maks):
                sozluk[float(temp[age])].setdefault(float(i + 1), 0)
            sozluk[float(temp[age])].update({float(temp[edu]): sozluk[float(temp[age])][float(temp[edu])] + 1})
        self.f.close()
        data = []
        labels = []
        for key, val in sozluk.items():
            labels.append(key)
            data.append(list(val))
        if self.check.get() == "1":
            clust = hcluster(data, tanamoto)
            self.printclustt(clust, labels)
        elif self.check.get() == "2":
            clust = kcluster(data, tanamoto, int(self.en.get()))
            for i in range(len(clust)):
                self.Textbox1.insert(END, f"{i} {clust[i]}\n")

    def printclustt(self, clust, labels=None, n=0):
        for i in range(n): self.Textbox1.insert(END, " ")
        if clust.id < 0:
            self.Textbox1.insert(END,'-\n')
        else:
            if labels == None:
                self.Textbox1.insert(END,clust.id)
                self.Textbox1.insert(END,"\n")
            else:
                self.Textbox1.insert(END,labels[clust.id])
                self.Textbox1.insert(END,"\n")

        # now print the right and left branches
        if clust.left != None: self.printclustt(clust.left, labels=labels, n=n + 1)
        if clust.right != None: self.printclustt(clust.right, labels=labels, n=n + 1)

def main():
    root.geometry("780x600+300+300")
    app = Example(root)
    root.mainloop()


main()