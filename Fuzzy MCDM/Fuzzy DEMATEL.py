import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from math import *

# BU KISIMDA, BULANIK DEMATEL'DE KULLANACAĞIMIZ FONKSİYONLARI OLUŞTURDUK

#Karar vericilerin doldurduğu anketleri fonksiyon yardımıyla pythona aktarmayı yarayan fonksiyon.
def veri_cek(file_path,sheet_name):
    
    df = pd.read_excel(file_path,sheet_name) 

    head=np.delete(np.array(df.columns),[0,1]) #Exceldeki tarih ve kullanıcı kolonlarını sildik. Kriter kolonları kaldı

    veri = np.array([]) #Boş bi dizi oluşturduk

    for item in head:    #Kriter kolonlarının verilerini boş dizimize ekledik.
        veri_cek = np.array([df[[item]]])
        veri = np.append(veri,veri_cek)

    return veri

#Karar vericilerin sözel ifadelerini bulanık sayılara çeviren fonksiyon. 
def bulanik_sayilar (karar_verici):
    fuzzy_d = np.array([[[0]*4]*13]*13)
    fuzzy_d = fuzzy_d.astype('float64')     
    n=13                
    for i in range (0,n):
        for j in range (0,n):
            
            if karar_verici[i][j] == 'Etki Yok':
                fuzzy = np.array([0,0,0,0])
                fuzzy_d[i][j] = fuzzy      
                
            elif karar_verici[i][j] == 'Çok Düşük Derecede Etki':
                fuzzy = np.array([0,0,0.05,0.2])
                fuzzy_d[i][j] = fuzzy      
                
            
            elif karar_verici[i][j] == 'Düşük Derecede Etki':
                fuzzy = np.array([0.05,0.2,0.3,0.45])
                fuzzy_d[i][j] = fuzzy      
                
            
            elif karar_verici[i][j] == 'Orta Derecede Etki':
                fuzzy = np.array([0.3,0.45,0.55,0.7])
                fuzzy_d[i][j] = fuzzy      
                
            
            elif karar_verici[i][j] == 'Yüksek Derecede Etki':
                fuzzy = np.array([0.55,0.7,0.8,0.95])
                fuzzy_d[i][j] = fuzzy      
                
                
            elif karar_verici[i][j] == 'Çok Yüksek Derecede Etki':
                fuzzy = np.array([0.8,0.95,1,1])
                fuzzy_d[i][j] = fuzzy         
        
         
           
    return fuzzy_d

#Karar vericilerin birleştirilmiş "direkt ilişki matrisini" aritmetik ortalama ile oluşturan fonksiyon.
def di_matris(dm1,dm2,dm3):
   		

    kv1_agirligi =  1/3 # 1. Karar Vericinin ağırlığı
    kv2_agirligi = 1/3 # 2. Karar Vericinin ağırlığı
    kv3_agirligi = 1/3 # 3. Karar Vericinin ağırlığı   
    
    ortak_matris= (kv1_agirligi*dm1) + (kv2_agirligi*dm2) + (kv3_agirligi*dm3)
    
    return ortak_matris

#Direkt İlişki Matrisini normalize eden fonksiyon
def normalize(A):
    n=13 #matris boyutu nxn
    columns_sums = np.array([])
    norm_matris = np.array([])
    for i in range(0,n):
          column_sum = 0
          for j in range(0,n):
              column_sum = column_sum + A[j][i][3]
             
          columns_sums=np.append(columns_sums,column_sum)    
    
    r = max(columns_sums)
    norm_matris = A/r
    
    return norm_matris

#Bulanık sayıların birinci(l), ikinci(m1), üçüncü(m2) ve dördüncü(u) değerlerini ayrı matrisler haline getirdik.
def ayirma (dizi):
    a = np.array([]) #Üçgensel bulanık sayının 1. değeri için matris
    b = np.array([]) #Üçgensel bulanık sayının 2. değeri için matris
    c = np.array([]) #Üçgensel bulanık sayının 3. değeri için matris
    d= np.array([]) ##Üçgensel bulanık sayının 4. değeri için matris
   
    for i in range(0,4):
        for j in range(0,len(dizi)):
            for m in range(0,len(dizi)):
                if i==0:
                    a = np.append(a,dizi[j][m][i])
                elif i==1:
                    b = np.append(b,dizi[j][m][i])
                elif i==2:
                    c = np.append(c,dizi[j][m][i])    
                elif i==3:
                    d = np.append(d,dizi[j][m][i])
    a=a.reshape(13,13)
    b=b.reshape(13,13)
    c=c.reshape(13,13)
    d=d.reshape(13,13)           
    return a,b,c,d

#l,m1,m2 ve u değerleri için toplam ilişki matrisini hesaplayan fonksiyon.
def toplam_iliski(array):
    I = np.eye(13) #nxn birim matris oluşturduk.
    I_array = I-array  #I-X matrisini oluşturduk
    inverse = np.linalg.inv(I_array) #I-X matrisinin tersini aldık
    carpim = array.dot(inverse) #X matrisi ile I-X matrisinin tersini çarptık
    return carpim

#İşlem kolaylığı için ayrılan bulanık sayı değerlerini, işlem sonrası tekrar birleştirmek için kullanılan fonk. (Toplam İlişki Matrisi)
def toplam_iliski_matrisi(l,m1,m2,u):        
    
    matris = np.array([[[0]*4]*13]*13)
    matris = matris.astype('float64')
    
    for i in range(0,4):
        for j in range(0,13):
            for n in range(0,13):
                if i==0:
                    matris[j][n][i] = l[j][n]
                    
                elif i==1:
                    matris[j][n][i] = m1[j][n]
                   
                elif i==2:
                    matris[j][n][i] = m2[j][n]    
                
                elif i==3:
                    matris[j][n][i] = u[j][n]                
    return matris  

#Toplam ilişki matrisindeki bulanık sayıları tek bir sayı haline getiren fonk. (Durulaştırma)
def durulastirma (dizi):
    duru_matris = np.array([])
    
    for i in range(0,13):
        for j in range(0,13):
            duru = ( (dizi[i][j][0]) + (2*dizi[i][j][1]) + (2*dizi[i][j][2]) + (dizi[i][j][3]) )/6
            duru_matris=np.append(duru_matris,duru) 
           
        
    return duru_matris

#D ve R değerlerini hesapladığımız fonk.
def D_R (dizi):
    
    D = np.array([])    
    D_toplam = np.sum(dizi,axis=1) #Satırlar toplamı
    D = np.append(D,D_toplam)
    
    R = np.array([])
    R_toplam = np.sum(dizi,axis=0) #Sütunlar toplamı
    R = np.append(R,R_toplam)
        
    return D,R


#BU KISIMDA, OLUŞTURDUĞUMUZ FONKSİYONLAR YARDIMIYLA HESAPLAMALARIMIZI GERÇEKLEŞTİRDİK.

#Excel dosya yolunu belirterek, yukarıda yazdığımız "veri_cek" fonk. aracılığıyla verileri çektik.
file_path = "D:\\alper\\Industrial Engineering\\Lectures\\4th Grade\\Bitirme Tezi\\Uygulama\\B_DEMATEL.xlsx" 
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


#Karar vericilerin sözel ifadelerini 13x13'lük matris haline getirdik.
kv_1 = kv_1.reshape(13,13)
kv_2 = kv_2.reshape(13,13)
kv_3 = kv_3.reshape(13,13)
bulanik_kv1 = bulanik_sayilar(kv_1) #1. Karar vericinin sözel ifadelerini bulanık sayılara çevirdik.
bulanik_kv2 = bulanik_sayilar(kv_2) #2. Karar vericinin sözel ifadelerini bulanık sayılara çevirdik.
bulanik_kv3 = bulanik_sayilar(kv_3) #3. Karar vericinin sözel ifadelerini bulanık sayılara çevirdik.


#di_matris fonk. ile "Direkt İlişki Matrisi"ni oluşturduk.
di_matris = di_matris(bulanik_kv1,bulanik_kv2,bulanik_kv3) 


#Yukarıda yazdığımız normalize fonk. ile Direkt İlişki Matrisini normalize ettik.
norm_matris = normalize(di_matris)



#İşlem kolaylığı açısından ayirma fonk. ile normalize matrisinin l,m1,m2,u değerlerini ayrı matrisler haline getirdik.
ayirma=ayirma(norm_matris)
l = ayirma[0]
m1 = ayirma[1]
m2 = ayirma[2]
u = ayirma[3]


#toplam_iliski fonk. ile değerlerin toplam ilişki hesaplamalarını yaptık.
ti_l = toplam_iliski(l)
ti_m1 = toplam_iliski(m1)
ti_m2 = toplam_iliski(m2)
ti_u = toplam_iliski(u)

          
#toplam_iliski_matrisi fonk. ile l,m1,m2,u değerlerini tekrardan tek matriste topladık.             
toplam_iliski_matrisi = toplam_iliski_matrisi(ti_l,ti_m1,ti_m2,ti_u)


#durulastirma fonk. ile toplam ilişki matrisini durulaştırdık. D,R değerleri bu matris üzerinden hesaplanacaktır.
duru_tim = durulastirma(toplam_iliski_matrisi) #Bu matris ANP'de kriter ağırlıklandırmada da kullanılacaktır.
duru_tim = duru_tim.reshape(13,13) #Matrisi 13x13 şekline getirdik.


#D_R fonk. D ve R değerlerini hesapladık.
D_R = D_R(duru_tim)
D = D_R[0] # D değerleri
D = np.round(D,3)
R = D_R[1] # R değerleri
R = np.round(R,3)


# D+R ve D-R değerlerini hesapladık
D_toplam_R = D+R  # D+R değerleri
D_toplam_R = np.round(D_toplam_R,3)
D_fark_R = D-R # D-R değerleri
D_fark_R = np.round(D_fark_R,3)


#D+R ve D-R değerlerini yazdırdık
print(D_toplam_R,D_fark_R)
