import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import *

# BU KISIMDA, BULANIK TOPSIS'TE KULLANACAĞIMIZ FONKSİYONLARI OLUŞTURDUK.

#Karar vericilerin doldurduğu anketleri pythona aktarmaya yarayan fonksiyon.
def veri_cek(file_path,sheet_name):
    
    df = pd.read_excel(file_path,sheet_name) 

    head=np.delete(np.array(df.columns),[0,1]) #Exceldeki tarih ve kullanıcı kolonlarını sildik. Kriter kolonları kaldı

    A = np.array([]) #Boş bi dizi oluşturduk

    for item in head:    #Kriter kolonlarının verilerini boş dizimize ekledik.
        veri_cek = np.array([df[[item]]])
        A = np.append(A,veri_cek)

    #shape = int(sqrt(len(A)))

   # A=A.reshape(shape,shape) #Dizimi nxn lik matris haline getirdik. n=kriter sayısı
    
    return A

#Karar vericilerin sözel ifadelerini bulanık sayılara çeviren fonksiyon.        
def bulanik_sayilar (karar_verici):
    bulanik_d=np.array([])     
                    
    for i in range (0,len(karar_verici)):
        
        if karar_verici[i] == 'Çok Kötü':
            bulanik = np.array([0,0,1,2])
            bulanik_d=np.concatenate((bulanik_d,bulanik))      
            
        elif karar_verici[i] == 'Kötü':
            bulanik = np.array([0,2,2,3])
            bulanik_d=np.concatenate((bulanik_d,bulanik))
            
        
        elif karar_verici[i] == 'Biraz Kötü':
            bulanik = np.array([2,3,4,5])
            bulanik_d=np.concatenate((bulanik_d,bulanik))
            
        
        elif karar_verici[i] == 'Orta':
            bulanik = np.array([4,5,5,6])
            bulanik_d=np.concatenate((bulanik_d,bulanik))
            
        
        elif karar_verici[i] == 'Biraz İyi':
            bulanik = np.array([5,6,7,8])
            bulanik_d=np.concatenate((bulanik_d,bulanik))
            
            
        elif karar_verici[i] == 'İyi':
            bulanik = np.array([7,8,8,9])
            bulanik_d=np.concatenate((bulanik_d,bulanik))
            
        
        elif karar_verici[i] == 'Çok İyi':
            bulanik = np.array([8,9,10,10])
            bulanik_d=np.concatenate((bulanik_d,bulanik))
            
                                   
    return bulanik_d   

# Bulanık karar matrisini hesaplayan fonksiyon
def bulanik_km(dizi1,dizi2,dizi3):
    ortak_dizi = np.array([])
    
    for i in range (0,65):
        ortak_l = min(dizi1[i][0],dizi2[i][0],dizi3[i][0])
        ortak_dizi = np.append(ortak_dizi,ortak_l)
        
        ortak_m1 = (dizi1[i][1]+dizi2[i][1]+dizi3[i][1])/3
        ortak_dizi = np.append(ortak_dizi,ortak_m1)
        
        ortak_m2 = (dizi1[i][2]+dizi2[i][2]+dizi3[i][2])/3
        ortak_dizi = np.append(ortak_dizi,ortak_m2)
        
        ortak_u = max(dizi1[i][3],dizi2[i][3],dizi3[i][3])
        ortak_dizi = np.append(ortak_dizi,ortak_u)
    
    return ortak_dizi   

# Bulanık Karar Matrisini normalize eden fonksiyon
def normalize (dizi):
    
    #Kriterleri sırasıyla 'fayda' / 'maliyet' şeklinde sınıflandırdık.
    kriterler = ['fayda']*13
    
    r=np.array([[[0]*4]*5]*13)
    r=r.astype('float64')
    
    for i in range(0,13):
        
        kolon_maks = np.amax(dizi[i], axis=0)
        u_maks = kolon_maks[3]
        kolon_min = np.amin(dizi[i],axis=0)
        l_min = kolon_min[0]
        
        if kriterler[i]=='fayda':
            r[i]=dizi[i]/u_maks
        
        elif kriterler[i]=='maliyet':
            for j in range(0,5):
                m=3
                for k in range(0,4):
                    
                    r[i][j][k]= l_min/(dizi[i][j][m])
                    m=m-1                   
                                   
    return r 

# Duyarlılık Analizi yapabilmek için, kriter ağırlıklarını excelden çekmemizi yarayan fonk.
def agirlik_cek(file_path,sheet_name):
    
    df = pd.read_excel(file_path,sheet_name) 
    # df = df.astype("float64")
    A = np.array([]) #Boş bi dizi oluşturduk
    # A = A.astype("float64")
    veri_cek = np.array([])
    veri_cek = veri_cek.astype("float64")
    for item in df:    #Kriter kolonlarının verilerini boş dizimize ekledik.
    
        veri_cek = np.array([df[[item]]])
        
        A = np.append(A,veri_cek)

    
    return A

#Ağırlıklı matrisi hesaplamaya yarayan fonksiyon
def agirlikli_matris (dizi, agirlik):
    
    agirlikli_matris = np.array([])
    
    for i in range(0,13):
        eleman =dizi[i]*agirlik[i]
        agirlikli_matris = np.append(agirlikli_matris,eleman)
    
    return agirlikli_matris 

#İdeal Çözümü hesaplayan fonksiyon
def ideal_cozum (dizi):
    pozitif = np.array([])
    negatif = np.array([])
    
    for i in range(0,13):
        kolon_maks = np.amax(dizi[i], axis=0)
        u_maks = kolon_maks[3]
        pozitif = np.append(pozitif,u_maks)
        
        kolon_min = np.amin(dizi[i],axis=0)
        l_min = kolon_min[0]
        negatif = np.append(negatif,l_min)
        
    return pozitif,negatif 

#Bulanık Pozitif ve Negatif İdeal Çözümden Uzaklıklar Uzaklıkları hesaplayan fonk.
def uzaklik (agirlik,ideal):
    
    #İki yamuk bulanık sayı arasındaki uzaklığı hesaplayan fonk.
    def verteks (dizi1,dizi2):
        toplam=0
        for i in range(0,4): 
            islem = pow((dizi1[i]-dizi2[i]),2)
            toplam = toplam + islem
        
        uzaklik = toplam/4
        uzaklik = pow(uzaklik,0.5)
    
        return uzaklik
    
    alt_matris = np.array([])
    for i in range(0,5):
        for j in range(0,13):
            alt_matris = np.append(alt_matris, agirlik[j][i])
            
    alt_matris = alt_matris.reshape(5,13,4)        
    mesafe = np.array([])
    
    for i in range (0,5):
        for j in range(0,13):
            uzak = verteks(alt_matris[i][j], ideal[j])
            mesafe = np.append(mesafe,uzak)
    
    return mesafe

# Yakınlık katsayısını hesaplamaya yarayan fonk.
def yakinlik_katsayisi (dizi1,dizi2):
    d_i_pozitif = np.array([])
    d_i_negatif = np.array([])
    cc_i = np.array([])
    
    for i in range (0,5):
        satir_toplam_p = np.sum(dizi1[i])
        d_i_pozitif = np.append(d_i_pozitif,satir_toplam_p)        
        
        satir_toplam_n = np.sum(dizi2[i])
        d_i_negatif = np.append(d_i_negatif,satir_toplam_n)
        
        cci_eleman = (satir_toplam_n)/(satir_toplam_n + satir_toplam_p)
        cc_i = np.append(cc_i,cci_eleman)
        
    return d_i_pozitif, d_i_negatif, cc_i


#BU KISIMDA, OLUŞTURDUĞUMUZ FONKSİYONLAR YARDIMIYLA HESAPLAMALARIMIZI GERÇEKLEŞTİRDİK.

#Excel dosya yolunu belirterek, yukarıda yazdığımız "veri_cek" fonk. aracılığıyla verileri çektik.
file_path = "D:\\alper\\Industrial Engineering\\Lectures\\4th Grade\\Bitirme Tezi\\Uygulama\\alternatif_TOPSIS.xlsx" 
sheet_name = "Form Yanıtları 1"    
veri = veri_cek(file_path,sheet_name)


#Elimizdeki karışık verileri, karar verici bazında sınıflandırdık.
kv_1 = np.array([]) #1. Karar verici için boş bir dizi oluşturduk.
kv_2 = np.array([]) #2. Karar verici için boş bir dizi oluşturduk.
kv_3 = np.array([]) #3. Karar verici için boş bir dizi oluşturduk.


i=0
for item in veri:
    i=i+1
    if i%3==1:
        kv_1=np.append(kv_1,item) #1. Karar vericinin sözel ifadelerini içeren dizi
    elif i%3==2:
        kv_2=np.append(kv_2,item) #2. Karar vericinin sözel ifadelerini içeren dizi
    else:
        kv_3=np.append(kv_3,item) #3. Karar vericinin sözel ifadelerini içeren dizi
  
       
             
#bulanik_sayilar fonk. ile karar vericilerin ifadelerini bulanık sayılara çevirdik.
bulanik_kv1 = bulanik_sayilar(kv_1)
bulanik_kv1 = bulanik_kv1.reshape(65,4)
bulanik_kv2 = bulanik_sayilar(kv_2)
bulanik_kv2 = bulanik_kv2.reshape(65,4)
bulanik_kv3 = bulanik_sayilar(kv_3)
bulanik_kv3 = bulanik_kv3.reshape(65,4)          
        
              
#bulanik_km fonk. ile bulanık karar matrisini oluşturup matrisi şekillendirdik.
bulanik_km = bulanik_km(bulanik_kv1,bulanik_kv2,bulanik_kv3)
bulanik_km = np.round(bulanik_km,3)
bulanik_km = bulanik_km.reshape(13,5,4)        
                      
                   
#Normalize fonk. ile Bulanık Karar Matrisini normalize ettik.
norm_matris=normalize(bulanik_km)       


# Excel dosya yolunu belirterek, yukarıda yazdığımız "agirlik_ext" fonk. aracılığıyla ağırlık verilerini çektik.
file_path = "D:\\alper\\Industrial Engineering\\Lectures\\4th Grade\\Bitirme Tezi\\Uygulama\\agirliklar.xlsx" 
sheet_name = "Sheet1"    
agirlik = agirlik_cek(file_path,sheet_name)        


# agirlikli_matris fonk. ile ağırlıklı normalize matrisi hesapladık.
agirlik_matris = agirlikli_matris(norm_matris, agirlik)    
agirlik_matris = agirlik_matris.reshape(13,5,4)    
        

# ideal_cozum fonk. ile pozitif ve negatif ideal çözümleri hesapladık.       
ideal_cozum = ideal_cozum(agirlik_matris)
pozitif_ic = ideal_cozum[0]
pozitif_ic = np.column_stack((pozitif_ic,pozitif_ic)*2)    
negatif_ic = ideal_cozum[1]
negatif_ic = np.column_stack((negatif_ic,negatif_ic)*2)    


# Pozitif ve negatif ideal çözümlerden uzaklığı hesapladık.
d_a_pozitif = uzaklik(agirlik_matris,pozitif_ic)  
d_a_pozitif = d_a_pozitif.reshape(5,13)
d_a_negatif = uzaklik(agirlik_matris,negatif_ic)  
d_a_negatif = d_a_negatif.reshape(5,13)


#yakinlik_katsayisi fonk. ile yakınlık katsayısını hesapladık.
sonuclar = yakinlik_katsayisi(d_a_pozitif, d_a_negatif)
d_i_pozitif = sonuclar[0]
d_i_negatif = sonuclar [1]
cc_i = sonuclar[2]
cc_i = np.round(cc_i,5)

#Yakınlık katsayısı değerlerimizi yazdırdık.     
print(cc_i)
