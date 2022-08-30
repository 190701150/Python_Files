import regex as re

def lab5_soru1_sorua_cozum1(args):
    string = [str(i.lower()) for i in args if i != ""]
    return "".join(string)


###
def lab5_soru1_sorua_cozum2(liste):
    result = ""
    for i in liste:
        if i=="":
            continue
        result += i.lower()
    print("lab5_soru1_sorua_cozum2: " , result)


###
def lab5_soru1_sorub_cozum1(liste):
    result = dict()
    for i in liste:
        if i % 2 == 0:
            result[i] = "cift"
            continue
        result[i] = "tek"
    return result


###
def lab5_soru1_sorub_cozum2(liste):
    result = {i:"cift" if i%2 == 0 else "tek" for i in liste}
    return (result)


####----------------------------------------------------------------------

liste = ['MukemmelDegisken', 'bunasilDegisken', 'degisken2Ismi', 'degiskenIsmi2',
'yilan_degisken', 'yilan_2degisken', 'yilan_degisken3', 'SonucDegiskeni3']
def soru2(liste):
    result = (re.findall("[A-Z]",liste))
    for i in result:
        index = re.search(i,liste).span()[0]
        if index:
            liste = (liste.replace(liste[index], "_"+liste[index].lower()))
    print(liste.lower())

    
##TEST FONKSIYONU   
print("lab5_soru1_sorua_cozum1: ", lab5_soru1_sorua_cozum1("deneme_YaziMi"))
lab5_soru1_sorua_cozum2("deneme_YaziMi")
print("lab5_soru1_sorub_cozum1: ", lab5_soru1_sorub_cozum1([2,3,5,7]))
print("lab5_soru1_sorub_cozum2: ", lab5_soru1_sorub_cozum2([2,3,5,7]))
print("lab5_soru2_cozum: ")

for i in liste:
    soru2(i)