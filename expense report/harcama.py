from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from xlsxwriter import *

class Example(Frame):

    def __init__(self, parent):
        Frame.__init__(self , parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.pack()
        self.var = StringVar()
        self.text = Listbox(self,width=133,height=23)
        self.text.grid(columnspan = 20)
        btn_1 = Button (self, text = "Aktar", command=self.open_txt)
        btn_1.grid(row = 1, column = 0)
        btn_2 = Button (self, text = "Secili Sil", command=self.delete_item)
        btn_2.grid(row = 1, column = 1)
        btn_3 = Button (self, text = "Hepsini Sil", command=self.clear)
        btn_3.grid(row = 1, column = 2)
        btn_4 = Button(self, text="2Excel", command=self.toexcel)
        btn_4.grid(row = 1, column = 19)
        text_1 = Label(self, text="Tarih ekle:").grid(row=3,column = 1)
        text_2 = Label(self, text="Isim ekle:").grid(row=3,column = 4)
        text_3 = Label(self, text="Kategori seç:").grid(row=3,column =10)
        text_4 = Label(self, text="Miktar ekle:").grid(row=3,column =14)

        self.date = Entry(self,width = 15)
        self.date.grid(row = 4, rowspan = 3, column = 1)
        self.name = Entry(self, width = 15)
        self.name.grid(row = 4, rowspan = 3, column = 4)
        self.combodeger = StringVar()
        self.category_list = Listbox(self,height = 7)
        self.category_list.grid(row = 4, rowspan = 3, column = 10)
        self.eleman = ["Yiyecek", "İçecek", "Giyim", "Ev", "Elektronik"]
        for indeks, harcama in enumerate(self.eleman):
            self.category_list.insert(indeks, harcama)
        self.amaount = Entry(self, width = 15)
        self.amaount.grid(row=4, rowspan=3, column=14)

        self.add = Button(self, text = "Ekle", command = self.add_line)
        self.add.grid(row = 4, rowspan=3,column = 19)


    def toexcel(self):
        workbook = Workbook("Çıktı.xlsx")
        worksheet = workbook.add_worksheet()
        for row in range(self.text.size()):
            veri = self.text.get(row).split(", ")
            for column in range(len(veri)):
                worksheet.write(row,column,veri[column])
        workbook.close()


    def open_txt(self):
        text_file = filedialog.askopenfilename()
        # # file = open("C:\\Users\\atill\Desktop\harcama_list.txt", "r")
        # file = open(text_file, "r")
        # text_file = file.read().split("\n")
        # for i in range(len(text_file)):
        #     self.text.insert(i,text_file[i])
        # file.close()
        self.veri = parse_yaml(text_file)
        asd = self.veri['Butce_Girdileri']
        for i in range(len(asd)):
            self.text.insert(i,asd[i])


    def delete_item(self):
        index = self.text.curselection()
        self.text.delete(index)

    def clear(self):
        for i in range(self.text.size()):
            self.text.delete("end")

    def add_line(self):
        date = self.date.get()
        name = self.name.get()
        index = self.category_list.curselection()
        category = self.category_list.get(index)
        amaount = self.amaount.get()
        result = f"{date}, {name}, {category}, {amaount}"
        self.text.insert('end',result)
        self.date.delete(0, "end")
        self.name.delete(0, "end")
        self.amaount.delete(0, "end")


def parse_yaml(dizin):
    """ Yaml dosyasini yukleyip bir sozluk yapisinda geri dondurur.

    Eger daha oncesinde yaml paketini yuklemediyseniz ve hata aliyorsaniz:

    pip install pyyaml

    """
    import yaml
    with open(dizin) as file:
        document = yaml.load(file, Loader=yaml.FullLoader)

    return document

def main():
    root = Tk()
    root.title('Harcama Listesi')
    root.geometry("800x650+300+300")
    app = Example(root)
    root.mainloop()

if __name__ == '__main__':
    main()