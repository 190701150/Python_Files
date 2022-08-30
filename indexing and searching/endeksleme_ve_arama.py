from tkinter import *
import tkinter.scrolledtext as tkst
import os
import mysearchengine
from mysearchengine import searcher
root = Tk()
root.title("Endeksleme ve Arama")


class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        for i in os.listdir():
            if i == "db":
                break
            if i == os.listdir()[-1]:
                os.mkdir("./db")

        folder_name = os.path.join(os.getcwd(), "db")
        self.pagelist = ["http://books.toscrape.com/index.html"]
        self.dbtables = {'urllist': os.path.join(folder_name,'urllist.db'),
                          'wordlocation': os.path.join(folder_name,'wordlocation.db'),
                          'link': os.path.join(folder_name,'link.db'),
                          'linkwords': os.path.join(folder_name,'linkwords.db'),
                          'pagerank': os.path.join(folder_name,'pagerank.db')}


    def initUI(self):
        self.pack()
        self.text = Label(self, text='BookstoScrape Sitesinde Arama Yapilacak Kelimeyi Girin')
        self.text.grid(column=2, columnspan=20)  # 10

        self.en = Entry(self,width=50)
        self.en.grid(row=1, column=2, columnspan=20)

        self.var1 = IntVar()
        self.var2 = IntVar()
        self.var3 = IntVar()


        self.c1 = Checkbutton(self, text='Kelime Frekansi', variable = self.var1)
        self.c1.grid(row=2, column=11, sticky=W)
        self.c2 = Checkbutton(self, text='Inbound Link', variable = self.var2)
        self.c2.grid(row=3, column=11,sticky=W)
        self.c3 = Checkbutton(self, text='PageRank', variable = self.var3)
        self.c3.grid(row=4, column=11,sticky=W)

        self.endeksbutton = Button(self, text="Endeskle", command= self.endeksk)
        self.endeksbutton.grid(row=3, column=16)

        self.arabutton = Button(self, text="Ara", command= self.ara)
        self.arabutton.grid(row=3, column=17)

        self.Textbox1 = tkst.ScrolledText(self, width=94, height=20)
        self.Textbox1.grid(row=13, column=2, columnspan=20)

    def endeksk(self):
        crawler_ = mysearchengine.crawler(self.dbtables)
        crawler_.createindextables()
        crawler_.crawl(self.pagelist)
        crawler_.close()

    def ara(self):
        mysearchengine = searcher(self.dbtables)

        mysearchengine.calculatepagerank()

        result = mysearchengine.query(self.en.get(), self.var1.get(), self.var2.get(), self.var3.get())
        self.Textbox1.insert(END, "Sonuclar:\n")
        for i,j in result:
            self.Textbox1.insert(END, "{} {}".format(i, j))
            self.Textbox1.insert(END, "\n")
        # Aşağıdaki close adımı önemli!
        mysearchengine.close()


def main():
    root.geometry("780x600+300+300")
    app = Example(root)
    root.mainloop()


if __name__ == '__main__':
    main()
