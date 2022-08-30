def mergeSort(arr):
    if len(arr) > 1:
 
        # Dizinin ortasini bulmak
        mid = len(arr)//2
 
        # Dizi elemanlarinin bölünmesi
        L = arr[:mid]
 
        # 2. yari
        R = arr[mid:]
 
        # İlk yariyi siralamak
        mergeSort(L)
 
        # İkinci yarinin siralanmasi
        mergeSort(R)
 
        i = j = k = 0
 
        # Verileri L [] ve R [] gecici dizilerine kopyala
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
 
        # Herhangi bir elemanin kalip kalmadigini kontrol etme
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
 
# Listeyi yazdirma kismi
def printList(arr):
    for i in range(len(arr)):
        print(arr[i], end=" --- ")
    print()
    
    

def borsa(arr):
    p = 1
    
    while True:
        
        ParaMax = int(arr[-p][0:1])
        print("max para: ",ParaMax)
        
        ParaMax_gun = int(arr[-p][8:9])
        print("Paranin Max oldugu gun: ",ParaMax_gun)
        
        ParaMin = int(arr[0][0:1])
        print("min para: ",ParaMin)
        
        ParaMin_gun = int(arr[0][8:9])
        print("Paranin Min oldugu gun: ",ParaMin_gun)
        
        if ParaMin_gun < ParaMax_gun:
            kar = ParaMax - ParaMin
            print("elde edilebilecek max kar: ", end="\n")
            return kar
        else:
            p += 1
            ParaMax = int(arr[-(p)][0:1])
            print("yeni max para: ",ParaMax)
    

if __name__ == '__main__':
    arr = ['9 TL => 1.gun','1 TL => 2.gun','5 TL => 3.gun','4 TL => 4.gun']

    print("Oynanmamis gunluk dizi", end="\n")
    printList(arr)
    mergeSort(arr)
    
    print("Paraya gore siralanmis dizi: ", end="\n")
    printList(arr)
    
    print(borsa(arr))
