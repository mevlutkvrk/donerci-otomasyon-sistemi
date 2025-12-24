from giris_dosyasi import Ui_Dialog
from PyQt5.QtWidgets import *
import pymongo
from datetime import datetime
import tasarim

class GirisEkrani(QDialog, Ui_Dialog):
    def __init__(self):
        super(GirisEkrani, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Güvenlik ve Kayıt Ekranı")
        
        self.client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = self.client["DonerciDB"]

        self.setStyleSheet(tasarim.get_login_style())

        self.btn_giris.clicked.connect(self.giris_yap)
        self.btn_kayit.clicked.connect(self.kayit_ol)

    def giris_yap(self):
        kadi = self.txt_kadi.text()
        sifre = self.txt_sifre.text()
        
        kullanici = self.db["kullanicilar"].find_one({"kadi": kadi, "sifre": sifre})
        
        if kullanici:
            self.accept()
        else:
            QMessageBox.warning(self, "Hata!", "Kullanıcı adı veya şifre yanlış.\nKaydınız yoksa 'Kayıt Ol' butonunu kullanınız.")

    def kayit_ol(self):
        kadi = self.txt_kadi.text()
        sifre = self.txt_sifre.text()
        
        if not kadi or not sifre:
            QMessageBox.warning(self, "Eksik Bilgi!", "Lütfen kullanıcı adı ve şifre belirleyin!")
            return
            
        var_mi = self.db["kullanicilar"].find_one({"kadi": kadi})
        
        if var_mi:
            QMessageBox.warning(self, "Hata!", "Bu kullanıcı adı zaten alınmış.")
        else:
            self.db["kullanicilar"].insert_one({
                "kadi": kadi, 
                "sifre": sifre,
                "kayit_tarihi": datetime.now().strftime("%Y-%m-%d")
            })
            QMessageBox.information(self, "Başarılı!", "İşletme kaydı oluşturuldu.\nŞimdi 'Giriş Yap' butonuna basabilirsiniz.")

