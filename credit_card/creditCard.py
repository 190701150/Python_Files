from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
from recommendations import *
import dbm,pickle
from pprint import pprint

class MP3(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.root = parent
        self.initUI()

    def initUI(self):
        self.grid()
        self.text = Label(self,text='Yandaki butonu kullanarak diger kullanicilari yukleyebilirsiniz.')
        self.text.grid(column = 2,columnspan = 7)
        self.import_button = Button(self,text="Csv Dosya Sec",command= self.import_csv)
        self.import_button.grid(row=0,column=8)

        self.text = Label(self,text="Kullanici Bilgilerini Gir",font="Calibri 20")
        self.text.grid(row=1, column=5,columnspan=3)

        self.text = Label(self,text="Kategoriler").grid(row=2,column=3)
        self.text = Label(self,text="Toplam Miktar").grid(row=2,column=5)
        self.text = Label(self,text="Kullanici Harcamalari").grid(row=2,column=8)

        self.categories = Listbox(self,width=30)
        self.categories.grid(row=3,column=2,columnspan=3,rowspan=6)

        self.money_entry = Entry(self,width=20)
        self.money_entry.grid(row=5,column=5)

        self.spend_button = Button(self,text="Harcama Gir",state=DISABLED,command=self.add_spend)
        self.spend_button.grid(row=5,column=6)

        self.spend_update = Button(self, text='Harcama guncelle',command=self.update_spend)
        self.spend_update.grid(row=6,column=6)

        self.spend_delete = Button(self, text='Harcama sil',command=self.delete_spend)
        self.spend_delete.grid(row=7,column=6)

        self.user_spending = Listbox(self,width=40)
        self.user_spending.grid(row=3,column=7,columnspan=4,rowspan=6)

        self.text = Label(self,text='Oneri Ekrani',font='Calibri 20')
        self.text.grid(row=9, column=6)

        self.text = Label(self,text='Oneriler').grid(row=10,column=5,columnspan=2)
        self.text = Label(self,text='Magazalar').grid(row=10,column=8,columnspan=2)


        self.check = StringVar()
        self.category_check = Radiobutton(self,text='Kategori-Tabanli-Oneri',value='1',variable=self.check).grid(row=12,column=1,sticky=W)
        self.company_check = Radiobutton(self,text='Firma-Tabanli-Oneri',value='2',variable=self.check).grid(row=14,column=1,sticky=W)
        self.check.set('3')

        self.recommend_button = Button(self,text='Oneri Yap',state=DISABLED, command = self.show_recommend)
        self.recommend_button.grid(row=12,column=2,columnspan=2)
        self.recommend_comp = Button(self,text='Benzer Magaza Bul',state=DISABLED, command = self.same_shops)
        self.recommend_comp.grid(row=14,column=2,columnspan=2)

        self.suggestions_list = Listbox(self,width=40)
        self.suggestions_list.grid(row=11,column=5,rowspan=6,columnspan=3)

        self.malls_list = Listbox(self,width=40)
        self.malls_list.grid(row=11,column=7,rowspan=6,columnspan=3)
        self.open_program()

    def open_program(self):
        self.csv_dict = dict()
        self.csv_dict.setdefault('Person',{})
        for category, money in dbm.open('person_infos.db','c').items():
            category = str(category).strip("b'")
            result = f"{category}: {pickle.loads(money)}"
            self.csv_dict['Person'].setdefault(category,pickle.loads(money))
            self.user_spending.insert(END, result)

    def import_csv(self):
        folder_name = filedialog.askopenfilename(initialdir=".", title="Veri setini seciniz",filetypes=(("csv files", ".csv"), ("all files", ".*")))
        #folder_name = 'kredikarti_veri.csv'  # değiştirmeyi unutma
        categories = set()
        df = pd.read_csv(folder_name)


        for i in range(len(df['Company'])):
            categories.add(df['Account'][i])
            company = df['Company'][i]
            self.csv_dict.setdefault(company, {})
            if df['JV Value'][i] < 0:
                continue
            self.csv_dict[company].setdefault(df['Account'][i], 0)

            self.csv_dict[company].update({df['Account'][i]: self.csv_dict[company][df['Account'][i]] + df['JV Value'][i]})

        self.recommend_button['state'] = ACTIVE
        self.spend_button['state'] = ACTIVE
        self.recommend_comp['state'] = ACTIVE
        self.import_button['state'] = DISABLED
        for i in categories:
            self.categories.insert(END,i)
        pprint(self.csv_dict) #burada person adli bir cikti da cerecek bu bizim harcama kategorisine eklediklerimiz
        

    def add_spend(self):
        db = dbm.open('person_infos.db','c')
        try:
            category = self.categories.get(self.categories.curselection())
            money = float(self.money_entry.get())
        except TclError:
            messagebox.showerror('Uyari',message='Lutfen bir adet kategori seciniz!')
            return
        except ValueError:
            messagebox.showerror('Uyari',message='Lutfen bir harcama giriniz!')
            return
        index = 0
        for row in range(self.user_spending.size()):
            temp = self.user_spending.get(row).split(": ")
            if category == temp[0]:
                money+=float(temp[1])
                self.user_spending.delete(row)
                index = row
        result = f"{category}: {money}"
        db[category] = pickle.dumps(money)
        self.csv_dict['Person'][category] = money
        self.user_spending.insert(index,result)

    def update_spend(self): ##  kodu biraz suslemek istedim
        db = dbm.open('person_infos.db', 'c')
        index = self.user_spending.curselection()
        spend = self.user_spending.get(index)
        category, _ = spend.split(': ')
        new_val = float(self.money_entry.get())
        db[category] = pickle.dumps(new_val)
        self.user_spending.delete(index)
        result = f"{category}: {new_val}"
        self.user_spending.insert(index,result)
        self.csv_dict['Person'][category] = new_val

    def delete_spend(self): ##  kodu biraz suslemek istedim
        db = dbm.open('person_infos.db', 'c')
        index = self.user_spending.curselection()
        category, val = self.user_spending.get(index).split(': ')
        del db[category]
        self.user_spending.delete(index)
        print(self.csv_dict)
        del self.csv_dict['Person'][category]
        print(self.csv_dict)

    def show_recommend(self):
        self.suggestions_list.delete(0,END)
        if self.check.get() == '2':
            result = getRecommendations(self.csv_dict,'Person',sim_pearson)
            for val, recommend in result[:3]:
                self.suggestions_list.insert(END,f'{recommend} -> {val}')
        elif self.check.get() == "1":
            item = calculateSimilarItems(self.csv_dict, 5)
            result = getRecommendedItems(self.csv_dict,item,'Person')
            for val, recommend in result[:3]:
                self.suggestions_list.insert(END,f'{recommend} -> {val}')
        else:
            messagebox.showwarning('Uyarı', message='Lutfen oneri secimini yapiniz!')

    def same_shops(self):
        self.malls_list.delete(0,END)
        result = topMatches(self.csv_dict, 'Person',similarity=sim_jaccard)
        for val, recommend in result[:3]:
            self.malls_list.insert(END,f'{recommend} -> {val}')
        

def main():
    root = Tk()
    root.title("Harcama Oneri Sistemi")
    root.geometry("950x700+450+200")
    App = MP3(root)
    root.mainloop()


if __name__ == '__main__':
    main()
