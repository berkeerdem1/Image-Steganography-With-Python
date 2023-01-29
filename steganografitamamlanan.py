from PIL import Image
import time
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#
# 8-bite çevirme

def genData(data):  #girilen verileri 8-bite çevirecek
# ikili kodların listesini oluşturma

    newd = []  # verilen veri

    for i in data:
        newd.append(format(ord(i), '08b')) #8bite çevir--ord
    return newd     #8-bite çevrilen veriyi döndür


# pikselleri değiştir
# 8-bit ikili veri sonda döndürülüyor

def modPix(pix, data):      #ÖZET görüntünüN piksellerini değiştirme işlemi
    datalist = genData(data) #veri listesi
    lendata = len(datalist) #veri uzunluğu fonksiyonu
    imdata = iter(pix) #pikseller içinde gezmek için

    for i in range(lendata):

        # bir seferde 3 piksel çıkarma
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]

        # piksel değeri yapma
        #  1 için tek 0 için çift / değiştirdim

        # pix[j] -= 1
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1

            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if (pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        # her setin sekizinci pikselini söyler
        # dur ya da devamını oku.
        # 0 okumaya devam et anlamına gelir; 1 demektir
        #
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if (pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix) #piksellerin listesi
        yield pix[0:3]  #pikselleri değişirme
        yield pix[3:6]  #''
        yield pix[6:9]  #''

def encode_enc(newimg, data):       #ÖZET değiştirilen pikseller resme yerleştiriliyor
    w = newimg.size[0] #yeniresmin boyutu
    (x, y) = (0, 0)


    for pixel in modPix(newimg.getdata(), data):
        # değiştirilmiş pixelleri yeni resme yerleştirme
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

def encode(x,y,z):  #x:resim  y:yeni resim z:yeni resmi kaydet
    #dosyanın adres yolu
    image = Image.open(x, 'r')

    time.sleep(0.5)
    if (len(y) == 0): #veri girilmezse
        raise ValueError('Data is empty') #veri boş

    newimg = image.copy()  #yeni resmi kopyala
    encode_enc(newimg, y)  #yeni resimde encode_enc --> yeni pikselleri yeni resme yerleştirme işlemini gönder

    newimg.save(z, str(z.split(".")[1].upper())) #kaydet


def decode(a):   # a:resim
    img = a
    image = Image.open(img, 'r')#adres yolu

    data = ''
    imgdata = iter(image.getdata()) #verilerin içinde gez

    while (True): #3piksel çıkarma
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        binstr = '' #metninn karakterlerini ikiliye çeviriyor

        for i in pixels[:8]: #sekizinci pikseli çıkar
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

# Main fonksiyon
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()

class MyWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MyWindow,self).__init__()
        uic.loadUi('projeArayüz.ui', self)

        main_title = "Image Stegonagraphy"
        self.setWindowTitle(main_title)


        #textbrowserların boyut ve şekil özellikleri
        self.textBrowser_2=QLineEdit(self)
        self.textBrowser_2.setGeometry(QtCore.QRect(20, 190, 451, 31))
        self.textBrowser_3=QLineEdit(self)
        self.textBrowser_3.setGeometry(QtCore.QRect(20, 270, 451, 31))
        self.textBrowser_4=QLineEdit(self)
        self.textBrowser_4.setGeometry(QtCore.QRect(20, 350, 451, 31))
        self.textBrowser_5=QLineEdit(self)
        self.textBrowser_5.setGeometry(QtCore.QRect(510, 210, 441, 31))
        self.textBrowser_6=QLineEdit(self)
        self.textBrowser_6.setGeometry(QtCore.QRect(510, 290, 441, 110))
        self.pushButton.clicked.connect(self.clicked1)#save
        self.pushButton_2.clicked.connect(self.clicked2)#outputdata
        self.pushButton_3.clicked.connect(self.exit2)#quit

    def clicked1(self):             #save butonu için encode içindeki metin kısımlarını ekleme
        encode(self.textBrowser_2.text(),self.textBrowser_3.text(),self.textBrowser_4.text())
        self.textBrowser_2.setText("")
        self.textBrowser_3.setText("")
        self.textBrowser_4.setText("")

    def clicked2(self):             #outpu data decode içindek metin kısımlarını ekleme
        data1 = decode(self.textBrowser_5.text())       #verinin çıkarıldığı kısım
        self.textBrowser_6.setText(data1)               #adres yolu kısmı



    def exit2(self):           #çık
        sys.exit()

if __name__ == '__main__':
    # ana fonk
    main()
