from PyQt5.QtWidgets import *
import sys
from arayuz_dosyasi import Ui_MainWindow
from PyQt5.QtGui import QColor
import pymongo
from datetime import datetime
from bson.objectid import ObjectId
from giris_penceresi import GirisEkrani
import tasarim
from PyQt5.QtCore import Qt

class DonerciApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(DonerciApp, self).__init__()
        
        self.setupUi(self)
        self.setWindowTitle("Dönerci Otomasyon Sistemi v1.0")
        self.tasarimi_guzellestir()
        self.baglanti_kur()
        self.menuyu_yukle()
        self.btn_onayla.clicked.connect(self.siparisi_kaydet)
        self.depoyu_yukle() 
        self.btn_depo_yenile.clicked.connect(self.depoyu_yukle)
        self.takibi_yukle()
        self.btn_teslim_et.clicked.connect(self.siparisi_teslim_et)
        self.btn_stok_ekle.clicked.connect(self.stoga_ekle)
        self.stok_combobox_doldur()
        self.btn_analiz_yenile.clicked.connect(self.analizi_yukle)
        
    def baglanti_kur(self):

        client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.db = client["DonerciDB"]

    def menuyu_yukle(self):
        self.menu_alani.setFixedWidth(240)

        self.tbl_sepet.setColumnCount(3)
        self.tbl_sepet.setHorizontalHeaderLabels(["Ürün Adı", "Fiyat", "Adet"])
        header = self.tbl_sepet.horizontalHeader()
        header.setSectionResizeMode(0, header.Stretch)
        
        menu_koleksiyonu = self.db["menu"].find()

        layout = self.menu_alani.layout()
            
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget: widget.deleteLater()

        for yemek in menu_koleksiyonu:
            urun_adi = yemek["urun_adi"]
            fiyat = yemek["fiyat"]
            
            btn = QPushButton(f"{urun_adi}\n\n{fiyat} TL")
            btn.setMinimumHeight(80)
            btn.setStyleSheet(tasarim.get_menu_btn_style())
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            
            btn.clicked.connect(lambda ch, ad=urun_adi, fyt=fiyat: self.sepete_ekle(ad, fyt))
            layout.addWidget(btn)
            
        layout.addStretch()

    def sepete_ekle(self, ad, fiyat):
        
        satir_sayisi = self.tbl_sepet.rowCount()
        
        self.tbl_sepet.insertRow(satir_sayisi)
        
        self.tbl_sepet.setItem(satir_sayisi, 0, QTableWidgetItem(ad))
        self.tbl_sepet.setItem(satir_sayisi, 1, QTableWidgetItem(str(fiyat)))
        self.tbl_sepet.setItem(satir_sayisi, 2, QTableWidgetItem("1"))
        
        self.toplami_hesapla()

    def toplami_hesapla(self):
        toplam = 0
        satir_sayisi = self.tbl_sepet.rowCount()
        
        for i in range(satir_sayisi):
            fiyat_item = self.tbl_sepet.item(i, 1)
            if fiyat_item:
                fiyat = float(fiyat_item.text())
                toplam += fiyat
        
        self.lbl_toplam.setText(f"Toplam Tutar: {toplam} TL")

    
    def siparisi_kaydet(self):
        
        if self.tbl_sepet.rowCount() == 0:
            QMessageBox.warning(self, "Hata!", "Sepet boş, ürün seçiniz.")
            return

        musteri_adi = self.txt_musteri_ad.text()
        if not musteri_adi:
            QMessageBox.warning(self, "Eksik Bilgi!", "Müşteri ismi giriniz.")
            return

        if self.stok_kontrolu_yap() == False:
            return 
        
        toplam_tutar = 0
        satilan_urunler = []
        satir_sayisi = self.tbl_sepet.rowCount()

        for i in range(satir_sayisi):
            urun_adi = self.tbl_sepet.item(i, 0).text()
            fiyat = float(self.tbl_sepet.item(i, 1).text())
            toplam_tutar += fiyat
            satilan_urunler.append(urun_adi)
            
            yemek = self.db["menu"].find_one({"urun_adi": urun_adi})
            if yemek and "icerik" in yemek:
                for malz in yemek["icerik"]:
                    self.db["stoklar"].update_one(
                        {"urun_adi": malz["stok_adi"]},
                        {"$inc": {"miktar": -malz["kullanilan_miktar"]}}
                    )

        yeni_siparis = {
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "musteri_adi": musteri_adi,
            "urunler": satilan_urunler,
            "toplam_tutar": toplam_tutar,
            "durum": "Hazırlanıyor"
        }
        self.db["siparisler"].insert_one(yeni_siparis)
        
        self.takibi_yukle()
        
        self.tbl_sepet.setRowCount(0)
        self.lbl_toplam.setText("Toplam: 0 TL")
        self.txt_musteri_ad.clear()

    def stok_kontrolu_yap(self):
        satir_sayisi = self.tbl_sepet.rowCount()
        ihtiyac_listesi = {}

        for i in range(satir_sayisi):
            urun_adi = self.tbl_sepet.item(i, 0).text()
            yemek = self.db["menu"].find_one({"urun_adi": urun_adi})
            
            if yemek and "icerik" in yemek:
                for malz in yemek["icerik"]:
                    stok_adi = malz["stok_adi"]
                    miktar = malz["kullanilan_miktar"]
                    ihtiyac_listesi[stok_adi] = ihtiyac_listesi.get(stok_adi, 0) + miktar

        for stok_adi, gerekli_miktar in ihtiyac_listesi.items():
            depodaki_urun = self.db["stoklar"].find_one({"urun_adi": stok_adi})
            
            if not depodaki_urun or depodaki_urun["miktar"] < gerekli_miktar:
                QMessageBox.warning(self, "Stok Yetersiz!", f"Depoda yeterli '{stok_adi}' kalmadı!")
                return False
        return True

    def depoyu_yukle(self):
        
        self.tbl_depo.setColumnCount(3)
        self.tbl_depo.setHorizontalHeaderLabels(["Ürün Adı", "Miktar", "Birim"])
        
        header = self.tbl_depo.horizontalHeader()
        header.setSectionResizeMode(0, header.Stretch)
        
        stoklar = self.db["stoklar"].find()
        
        self.tbl_depo.setRowCount(0)
        
        for stok in stoklar:
            satir = self.tbl_depo.rowCount()
            self.tbl_depo.insertRow(satir)
            
            item_ad = QTableWidgetItem(stok["urun_adi"])
            item_miktar = QTableWidgetItem("{:.2f}".format(stok["miktar"]))
            item_birim = QTableWidgetItem(stok["birim"])
            
            kritik_sinir = 5.0 #adet birimleri icin
            
            if stok["birim"] == "kg":
                kritik_sinir = 2.0 #kg birimleri icin
            
            if stok["miktar"] < kritik_sinir:
                kirmizi_renk = QColor(255, 200, 200)
                item_ad.setBackground(kirmizi_renk)
                item_miktar.setBackground(kirmizi_renk)
                item_birim.setBackground(kirmizi_renk)
            
            self.tbl_depo.setItem(satir, 0, item_ad)
            self.tbl_depo.setItem(satir, 1, item_miktar)
            self.tbl_depo.setItem(satir, 2, item_birim)


    def stok_combobox_doldur(self):
        self.cmb_stok_urun.clear()
        stoklar = self.db["stoklar"].find({}, {"urun_adi": 1})
        
        for stok in stoklar:
            self.cmb_stok_urun.addItem(stok["urun_adi"])


    def stoga_ekle(self):
        secilen_urun = self.cmb_stok_urun.currentText()
        eklenecek_miktar = self.spin_stok_miktar.value()
        
        if eklenecek_miktar <= 0:
            QMessageBox.warning(self, "Hata!", "Lütfen geçerli bir miktar giriniz.")
            return
            
        self.db["stoklar"].update_one(
            {"urun_adi": secilen_urun},
            {"$inc": {"miktar": eklenecek_miktar}}
        )
        QMessageBox.information(self, "Başarılı!", f"{eklenecek_miktar} birim {secilen_urun} depoya eklendi.")
        self.depoyu_yukle()
        self.spin_stok_miktar.setValue(0)

    def analizi_yukle(self):
        
        self.tbl_analiz_detay.setColumnCount(3)
        self.tbl_analiz_detay.setHorizontalHeaderLabels(["Ürün Adı", "Satış Adedi", "Toplam Gelir"])

        header = self.tbl_analiz_detay.horizontalHeader()
        header.setSectionResizeMode(0, header.Stretch)
        header.setSectionResizeMode(2, header.Stretch) 

        siparisler = self.db["siparisler"].find()
        
        urun_istatistikleri = {}
        genel_toplam_ciro = 0

        for siparis in siparisler:
            genel_toplam_ciro += siparis["toplam_tutar"]
            
            for urun_adi in siparis["urunler"]:
                menu_urunu = self.db["menu"].find_one({"urun_adi": urun_adi})
                if menu_urunu:
                    fiyat = menu_urunu["fiyat"]
                
                if urun_adi in urun_istatistikleri:
                    urun_istatistikleri[urun_adi]["adet"] += 1
                    urun_istatistikleri[urun_adi]["gelir"] += fiyat
                else:
                    urun_istatistikleri[urun_adi] = {"adet": 1, "gelir": fiyat}

        self.tbl_analiz_detay.setRowCount(0)
        
        en_cok_satan_isim = " "
        en_cok_satan_adet = 0

        for urun_adi, veri in urun_istatistikleri.items():
            satir = self.tbl_analiz_detay.rowCount()
            self.tbl_analiz_detay.insertRow(satir)
            
            self.tbl_analiz_detay.setItem(satir, 0, QTableWidgetItem(urun_adi))

            item_adet = QTableWidgetItem(str(veri["adet"]))
            item_adet.setTextAlignment(Qt.AlignCenter)
            self.tbl_analiz_detay.setItem(satir, 1, item_adet)

            item_gelir = QTableWidgetItem(f"{veri["gelir"]} TL")
            item_gelir.setTextAlignment(Qt.AlignCenter)
            self.tbl_analiz_detay.setItem(satir, 2, item_gelir)
            
            if veri["adet"] > en_cok_satan_adet:
                en_cok_satan_adet = veri["adet"]
                en_cok_satan_isim = urun_adi

        self.lbl_analiz_ciro.setText(f"Toplam Ciro: {genel_toplam_ciro} TL")
        
        if en_cok_satan_adet > 0:
            QMessageBox.information(self, "Günlük Analiz", 
                                    f"En çok talep gören ürün: {en_cok_satan_isim}\n"
                                    f"Yarına hazırlık için stokta bu ürünün malzemelerine öncelik verilmeli!")

    def takibi_yukle(self):
        self.tbl_takip.setColumnCount(4)
        self.tbl_takip.setHorizontalHeaderLabels(["ID", "Müşteri", "İçerik", "Durum"])
        self.tbl_takip.setColumnHidden(0, True)
        
        header = self.tbl_takip.horizontalHeader()
        header.setSectionResizeMode(1, header.Stretch)
        header.setSectionResizeMode(2, header.Stretch)
        
        aktif_siparisler = self.db["siparisler"].find({"durum": "Hazırlanıyor"})
        
        self.tbl_takip.setRowCount(0)
        
        for siparis in aktif_siparisler:
            satir = self.tbl_takip.rowCount()
            self.tbl_takip.insertRow(satir)
            
            siparis_id = str(siparis["_id"])
            musteri = siparis.get("musteri_adi", "Misafir") 
            urunler = ", ".join(siparis["urunler"])
            durum = siparis["durum"]
            
            self.tbl_takip.setItem(satir, 0, QTableWidgetItem(siparis_id))
            
            item_musteri = QTableWidgetItem(musteri)
            item_musteri.setCheckState(Qt.Unchecked) 
            self.tbl_takip.setItem(satir, 1, item_musteri)
            
            self.tbl_takip.setItem(satir, 2, QTableWidgetItem(urunler))
            self.tbl_takip.setItem(satir, 3, QTableWidgetItem(durum))

        self.tbl_takip.setCurrentItem(None)

    def siparisi_teslim_et(self):
        islem_yapildi = False
        satir_sayisi = self.tbl_takip.rowCount()
        
        for i in range(satir_sayisi):
            
            item = self.tbl_takip.item(i, 1)
            
            if item.checkState() == Qt.Checked:
                siparis_id = self.tbl_takip.item(i, 0).text()
                
                self.db["siparisler"].update_one(
                    {"_id": ObjectId(siparis_id)},
                    {"$set": {"durum": "Teslim Edildi", "teslim_tarihi": datetime.now()}}
                )
                islem_yapildi = True

        if islem_yapildi:
            QMessageBox.information(self, "Başarılı!", "Seçilen siparişler teslim edildi.")
            self.takibi_yukle()
        else:
            QMessageBox.warning(self, "Uyarı!", "Lütfen teslim edilecek siparişlerin kutucuğunu işaretleyiniz.")

    def tasarimi_guzellestir(self):
        self.setStyleSheet(tasarim.get_main_style())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    giris = GirisEkrani()
    if giris.exec_() == QDialog.Accepted:
        window = DonerciApp()
        window.show()
        sys.exit(app.exec_())
    else:
        sys.exit()