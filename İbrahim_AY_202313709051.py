import sqlite3
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QDialog,
                             QLabel, QLineEdit, QPushButton, QVBoxLayout,
                             QWidget, QMessageBox, QStackedWidget,
                             QTableWidget, QTableWidgetItem, QDateEdit,
                             QComboBox,QRadioButton, QHBoxLayout)
from PyQt5.QtCore import Qt, QDate

def veritabani_baglantisi():
    conn = sqlite3.connect("kullanicilar.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kullanicilar (
            tc TEXT PRIMARY KEY,
            isim TEXT,
            soyisim TEXT,
            sifre TEXT,
            cinsiyet TEXT,
            dogum_tarihi TEXT
        )
    """)
    conn.commit()
    conn.close()

# Program başında çağır
veritabani_baglantisi()

# Geçici kullanıcı bilgileri (şifre, TC kimlik numarası)
users = {
    "ibo": {"password": "1234", "tc": "12345678901"},
    "kaan": {"password": "4321", "tc": "10987654321"}
}

appointments = []
appointments_file = "appointments.txt"
poliklinikler = {
    "Kardiyoloji": ["Dr. Ahmet Yılmaz", "Dr. Ayşe Kaya"],
    "Dermatoloji": ["Dr. Mehmet Demir", "Dr. Zeynep Şahin"],
    "Ortopedi": ["Dr. Hasan Çelik", "Dr. Fatma Yıldız"],
    "Nöroloji": ["Dr. Ali Arslan", "Dr. Elif Güneş"]
}

current_tc = ""

def save_appointments():
    if not current_tc:
        return
    file_name = f"{current_tc}_appointments.txt"
    with open(file_name, 'w') as f:
        for appointment in appointments:
            f.write(appointment + "\n")


def load_appointments():
    global appointments
    appointments = []  # Önce temizle
    if not current_tc:
        return
    file_name = f"{current_tc}_appointments.txt"
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            appointments = [line.strip() for line in f]


load_appointments()

class LoginForm(QMainWindow):
    def __init__(self, stacked_widget):
        super().__init__()
        self.setWindowTitle("Giriş Ekranı")
        self.setGeometry(200, 100, 300, 250)
        self.stacked_widget = stacked_widget

        self.tc_etiket = QLabel("TC Kimlik No:", self)
        self.tc_girdi = QLineEdit(self)
        self.sifre_etiket = QLabel("Şifre:", self)
        self.sifre_girdi = QLineEdit(self)
        self.sifre_girdi.setEchoMode(QLineEdit.Password)


        self.giris_butonu = QPushButton("Giriş", self)
        self.kayit_butonu = QPushButton("Kayıt Ol", self)
        self.reset_butonu = QPushButton("Reset", self)
        self.giris_butonu.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50; /* Yeşil */
                        color: white;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 16px;
                        margin: 4px 2px;
                        cursor: pointer;
                        border: none;
                        border-radius: 5px;
                    }

                    QPushButton:hover {
                        background-color: #45a049; /* Biraz daha koyu yeşil (isteğe bağlı) */
                    }
                """)
        self.kayit_butonu.setStyleSheet("""
                            QPushButton {
                                background-color: blue; /* Yeşil */
                                color: white;
                                padding: 10px 20px;
                                text-align: center;
                                text-decoration: none;
                                display: inline-block;
                                font-size: 16px;
                                margin: 4px 2px;
                                cursor: pointer;
                                border: none;
                                border-radius: 5px;
                            }

                            QPushButton:hover {
                                background-color: darkblue; /* Biraz daha koyu yeşil (isteğe bağlı) */
                            }
                        """)
        self.reset_butonu.setStyleSheet("""
                            QPushButton {
                                background-color: #ab0317; /* kırmızı */
                                color: white;
                                padding: 10px 20px;
                                text-align: center;
                                text-decoration: none;
                                display: inline-block;
                                font-size: 16px;
                                margin: 4px 2px;
                                cursor: pointer;
                                border: none;
                                border-radius: 5px;
                            }

                            QPushButton:hover {
                                background-color: #910314; /* Biraz daha koyu kırmızı (isteğe bağlı) */
                            }
                        """)

        layout = QVBoxLayout()
        layout.addWidget(self.tc_etiket)
        layout.addWidget(self.tc_girdi)
        layout.addWidget(self.sifre_etiket)
        layout.addWidget(self.sifre_girdi)
        layout.addWidget(self.giris_butonu)
        layout.addWidget(self.kayit_butonu)
        layout.addWidget(self.reset_butonu)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.giris_butonu.clicked.connect(self.login)
        self.kayit_butonu.clicked.connect(self.show_register_form)
        self.reset_butonu.clicked.connect(self.reset_form)

    def login(self):
        global current_tc
        tc = self.tc_girdi.text()
        password = self.sifre_girdi.text()

        conn = sqlite3.connect("kullanicilar.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kullanicilar WHERE tc = ? AND sifre = ?", (tc, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            current_tc = tc
            load_appointments()  # Burada çağır
            self.stacked_widget.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Hata", "Geçersiz TC veya şifre!")

    def show_register_form(self):
        register_dialog = RegisterDialog(self)
        register_dialog.exec_()

    def reset_form(self):
        self.tc_girdi.clear()
        self.sifre_girdi.clear()

class RegisterDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Kayıt Ol")
        self.setGeometry(150, 150, 300, 350)

        # İsim ve Soyisim alanları
        self.isim_etiket = QLabel("İsim:", self)
        self.isim_girdi = QLineEdit(self)

        self.soyisim_etiket = QLabel("Soyisim:", self)
        self.soyisim_girdi = QLineEdit(self)

        # TC Kimlik No
        self.tc_etiket = QLabel("TC Kimlik No:", self)
        self.tc_girdi = QLineEdit(self)

        # Şifre ve Onay Şifresi
        self.sifre_etiket = QLabel("Şifre:", self)
        self.sifre_girdi = QLineEdit(self)
        self.sifre_girdi.setEchoMode(QLineEdit.Password)

        self.sifre_onay_etiket = QLabel("Şifreyi Onayla:", self)
        self.sifre_onay_girdi = QLineEdit(self)
        self.sifre_onay_girdi.setEchoMode(QLineEdit.Password)

        # Cinsiyet Seçimi
        self.cinsiyet_etiket = QLabel("Cinsiyet:", self)
        self.kadin_radio = QRadioButton("Kadın", self)
        self.erkek_radio = QRadioButton("Erkek", self)

        # Doğum Tarihi
        self.dogum_tarihi_etiket = QLabel("Doğum Tarihi:", self)
        self.dogum_tarihi = QDateEdit(self)
        self.dogum_tarihi.setDisplayFormat("dd/MM/yyyy")

        # Butonlar
        self.kayit_butonu = QPushButton("Kaydet", self)
        self.reset_butonu = QPushButton("Reset", self)
        self.kayit_butonu.setStyleSheet("""
                   QPushButton {
                       background-color: #4CAF50; /* Yeşil */6
                       color: white;
                       padding: 10px 20px;
                       text-align: center;
                       text-decoration: none;
                       display: inline-block;
                       font-size: 16px;
                       margin: 4px 2px;
                       cursor: pointer;
                       border: none;
                       border-radius: 5px;
                   }

                   QPushButton:hover {
                       background-color: #45a049; /* Biraz daha koyu yeşil (isteğe bağlı) */
                   }
               """)
        self.reset_butonu.setStyleSheet("""
                   QPushButton {
                       background-color: #ab0317; /* kırmızı*/
                       color: white;
                       padding: 10px 20px;
                       text-align: center;
                       text-decoration: none;
                       display: inline-block;
                       font-size: 16px;
                       margin: 4px 2px;
                       cursor: pointer;
                       border: none;
                       border-radius: 5px;
                   }

                   QPushButton:hover {
                       background-color: #910314; /* Biraz daha koyu kırmızı (isteğe bağlı) */
                   }
               """)

        # Layout düzenlemeleri
        cinsiyet_layout = QHBoxLayout()
        cinsiyet_layout.addWidget(self.kadin_radio)
        cinsiyet_layout.addWidget(self.erkek_radio)

        layout = QVBoxLayout()
        layout.addWidget(self.isim_etiket)
        layout.addWidget(self.isim_girdi)
        layout.addWidget(self.soyisim_etiket)
        layout.addWidget(self.soyisim_girdi)
        layout.addWidget(self.tc_etiket)
        layout.addWidget(self.tc_girdi)
        layout.addWidget(self.sifre_etiket)
        layout.addWidget(self.sifre_girdi)
        layout.addWidget(self.sifre_onay_etiket)
        layout.addWidget(self.sifre_onay_girdi)
        layout.addWidget(self.cinsiyet_etiket)
        layout.addLayout(cinsiyet_layout)
        layout.addWidget(self.dogum_tarihi_etiket)
        layout.addWidget(self.dogum_tarihi)
        layout.addWidget(self.kayit_butonu)
        layout.addWidget(self.reset_butonu)

        self.setLayout(layout)

        self.kayit_butonu.clicked.connect(self.register_user)
        self.reset_butonu.clicked.connect(self.reset_form)

    def register_user(self):
        isim = self.isim_girdi.text()
        soyisim = self.soyisim_girdi.text()
        tc = self.tc_girdi.text()
        password = self.sifre_girdi.text()
        password_confirm = self.sifre_onay_girdi.text()
        cinsiyet = "Kadın" if self.kadin_radio.isChecked() else "Erkek" if self.erkek_radio.isChecked() else None
        dogum_tarihi = self.dogum_tarihi.date().toString("yyyy-MM-dd")

        if not (isim and soyisim and tc and password and password_confirm and cinsiyet):
            QMessageBox.warning(self, "Hata", "Lütfen tüm alanları doldurun!")
            return

        if password != password_confirm:
            QMessageBox.warning(self, "Hata", "Şifreler uyuşmuyor!")
            return

        # Veritabanına kayıt
        conn = sqlite3.connect("kullanicilar.db")
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO kullanicilar VALUES (?, ?, ?, ?, ?, ?)",
                           (tc, isim, soyisim, password, cinsiyet, dogum_tarihi))
            conn.commit()
            QMessageBox.information(self, "Başarılı", "Kayıt başarılı!")
            self.accept()
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Hata", "Bu TC zaten kayıtlı!")
        finally:
            conn.close()

    def reset_form(self):
        self.isim_girdi.clear()
        self.soyisim_girdi.clear()
        self.tc_girdi.clear()
        self.sifre_girdi.clear()
        self.sifre_onay_girdi.clear()
        self.kadin_radio.setChecked(False)
        self.erkek_radio.setChecked(False)
        self.dogum_tarihi.clear()

# UserManagementWidget sınıfı (Kullanıcıları listeleme ve silme)
class UserManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.user_table = QTableWidget()
        layout.addWidget(self.user_table)

        sil_layout = QHBoxLayout()
        self.tc_sil_etiket = QLabel("Silinecek TC:")
        self.tc_sil_girdi = QLineEdit()
        self.sil_butonu = QPushButton("Kullanıcı Sil")
        self.sil_butonu.clicked.connect(self.sil_kullanici)
        sil_layout.addWidget(self.tc_sil_etiket)
        sil_layout.addWidget(self.tc_sil_girdi)
        sil_layout.addWidget(self.sil_butonu)
        layout.addLayout(sil_layout)

        self.setLayout(layout)
        self.load_users()

    def load_users(self):
        conn = sqlite3.connect("kullanicilar.db")
        cursor = conn.cursor()
        cursor.execute("SELECT tc, isim, soyisim FROM kullanicilar")
        users = cursor.fetchall()
        conn.close()

        self.user_table.setRowCount(len(users))
        self.user_table.setColumnCount(3)
        self.user_table.setHorizontalHeaderLabels(["TC Kimlik No", "İsim", "Soyisim"])

        for i, user in enumerate(users):
            self.user_table.setItem(i, 0, QTableWidgetItem(user[0]))
            self.user_table.setItem(i, 1, QTableWidgetItem(user[1]))
            self.user_table.setItem(i, 2, QTableWidgetItem(user[2]))

    def sil_kullanici(self):
        tc_sil = self.tc_sil_girdi.text()
        if not tc_sil:
            QMessageBox.warning(self, "Hata", "Lütfen silinecek kullanıcının TC kimlik numarasını girin!")
            return

        conn = sqlite3.connect("kullanicilar.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kullanicilar WHERE tc = ?", (tc_sil,))
        conn.commit()
        if cursor.rowcount > 0:
            QMessageBox.information(self, "Başarılı", f"{tc_sil} TC kimlik numaralı kullanıcı silindi.")
            dosya_adi = f"{tc_sil}_appointments.txt"
            if os.path.exists(dosya_adi):
                os.remove(dosya_adi)
            self.load_users()  # Kullanıcı listesini güncelle
        else:
            QMessageBox.warning(self, "Hata", f"{tc_sil} TC kimlik numaralı kullanıcı bulunamadı!")
        conn.close()
        self.tc_sil_girdi.clear()

# AppointmentManagementWidget sınıfı (Randevuları görüntüleme ve iptal etme)
class AppointmentManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        self.appointment_table = QTableWidget()
        layout.addWidget(self.appointment_table)

        iptal_layout = QHBoxLayout()
        self.randevu_satir_etiket = QLabel("İptal Edilecek Randevu Satırı:")
        self.randevu_satir_girdi = QLineEdit()
        self.iptal_butonu = QPushButton("Randevu İptal Et")
        self.iptal_butonu.clicked.connect(self.iptal_randevu)
        iptal_layout.addWidget(self.randevu_satir_etiket)
        iptal_layout.addWidget(self.randevu_satir_girdi)
        iptal_layout.addWidget(self.iptal_butonu)
        layout.addLayout(iptal_layout)

        self.setLayout(layout)
        self.load_appointments()

    def load_appointments(self):
        all_appointments = []
        for filename in [f for f in os.listdir() if f.endswith('_appointments.txt')]:
            tc = filename.split('_')[0]
            with open(filename, 'r') as f:
                for line in f:
                    all_appointments.append((tc, line.strip()))

        self.appointment_table.setRowCount(len(all_appointments))
        self.appointment_table.setColumnCount(2)
        self.appointment_table.setHorizontalHeaderLabels(["Kullanıcı TC", "Randevu Bilgisi"])

        for i, (tc, appointment) in enumerate(all_appointments):
            self.appointment_table.setItem(i, 0, QTableWidgetItem(tc))
            self.appointment_table.setItem(i, 1, QTableWidgetItem(appointment))

    def iptal_randevu(self):
        try:
            satir_indeksi = int(self.randevu_satir_girdi.text())
            if 0 <= satir_indeksi < self.appointment_table.rowCount():
                tc = self.appointment_table.item(satir_indeksi, 0).text()
                randevu_bilgisi = self.appointment_table.item(satir_indeksi, 1).text()
                dosya_adi = f"{tc}_appointments.txt"

                if os.path.exists(dosya_adi):
                    with open(dosya_adi, 'r') as f:
                        randevular = [line.strip() for line in f]

                    if randevu_bilgisi in randevular:
                        randevular.remove(randevu_bilgisi)
                        with open(dosya_adi, 'w') as f:
                            for randevu in randevular:
                                f.write(randevu + '\n')
                        QMessageBox.information(self, "Başarılı", f"{tc} kullanıcısının '{randevu_bilgisi}' randevusu iptal edildi.")
                        self.load_appointments() # Randevu listesini güncelle
                    else:
                        QMessageBox.warning(self, "Hata", "Randevu bilgisi dosyada bulunamadı!")
                else:
                    QMessageBox.warning(self, "Hata", f"{tc} kullanıcısına ait randevu dosyası bulunamadı!")
            else:
                QMessageBox.warning(self, "Hata", "Geçersiz satır indeksi!")
        except ValueError:
            QMessageBox.warning(self, "Hata", "Lütfen geçerli bir satır numarası girin!")
        self.randevu_satir_girdi.clear()

# ClinicDoctorManagementWidget sınıfı (Poliklinik ve doktor yönetimi)
class ClinicDoctorManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        # Poliklinik Yönetimi
        poliklinik_layout = QVBoxLayout()
        poliklinik_etiket = QLabel("Poliklinik Yönetimi")
        self.poliklinik_liste = QComboBox()
        self.load_poliklinikler()
        yeni_poliklinik_layout = QHBoxLayout()
        self.yeni_poliklinik_etiket = QLabel("Yeni Poliklinik:")
        self.yeni_poliklinik_girdi = QLineEdit()
        self.poliklinik_ekle_butonu = QPushButton("Ekle")
        self.poliklinik_ekle_butonu.clicked.connect(self.ekle_poliklinik)
        yeni_poliklinik_layout.addWidget(self.yeni_poliklinik_etiket)
        yeni_poliklinik_layout.addWidget(self.yeni_poliklinik_girdi)
        yeni_poliklinik_layout.addWidget(self.poliklinik_ekle_butonu)
        poliklinik_sil_layout = QHBoxLayout()
        self.poliklinik_sil_etiket = QLabel("Silinecek Poliklinik:")
        self.poliklinik_sil_secim = QComboBox()
        self.load_poliklinikler(self.poliklinik_sil_secim)
        self.poliklinik_sil_butonu = QPushButton("Sil")
        self.poliklinik_sil_butonu.clicked.connect(self.sil_poliklinik)
        poliklinik_sil_layout.addWidget(self.poliklinik_sil_etiket)
        poliklinik_sil_layout.addWidget(self.poliklinik_sil_secim)
        poliklinik_sil_layout.addWidget(self.poliklinik_sil_butonu)
        poliklinik_layout.addWidget(poliklinik_etiket)
        poliklinik_layout.addWidget(self.poliklinik_liste)
        poliklinik_layout.addLayout(yeni_poliklinik_layout)
        poliklinik_layout.addLayout(poliklinik_sil_layout)
        layout.addLayout(poliklinik_layout)

        # Doktor Yönetimi
        doktor_layout = QVBoxLayout()
        doktor_etiket = QLabel("Doktor Yönetimi")
        doktor_ekle_layout = QHBoxLayout()
        self.doktor_poliklinik_etiket = QLabel("Poliklinik:")
        self.doktor_poliklinik_secim = QComboBox()
        self.load_poliklinikler(self.doktor_poliklinik_secim)
        self.yeni_doktor_etiket = QLabel("Yeni Doktor:")
        self.yeni_doktor_girdi = QLineEdit()
        self.doktor_ekle_butonu = QPushButton("Ekle")
        self.doktor_ekle_butonu.clicked.connect(self.ekle_doktor)
        doktor_ekle_layout.addWidget(self.doktor_poliklinik_etiket)
        doktor_ekle_layout.addWidget(self.doktor_poliklinik_secim)
        doktor_ekle_layout.addWidget(self.yeni_doktor_etiket)
        doktor_ekle_layout.addWidget(self.yeni_doktor_girdi)
        doktor_ekle_layout.addWidget(self.doktor_ekle_butonu)
        doktor_sil_layout = QHBoxLayout()
        self.doktor_sil_poliklinik_etiket = QLabel("Poliklinik:")
        self.doktor_sil_poliklinik_secim = QComboBox()
        self.load_poliklinikler(self.doktor_sil_poliklinik_secim)
        self.silinecek_doktor_etiket = QLabel("Silinecek Doktor:")
        self.silinecek_doktor_secim = QComboBox()
        self.doktor_sil_poliklinik_secim.currentIndexChanged.connect(self.load_doktorlar_for_sil)
        self.doktor_sil_butonu = QPushButton("Sil")
        self.doktor_sil_butonu.clicked.connect(self.sil_doktor)
        doktor_sil_layout.addWidget(self.doktor_sil_poliklinik_etiket)
        doktor_sil_layout.addWidget(self.doktor_sil_poliklinik_secim)
        doktor_sil_layout.addWidget(self.silinecek_doktor_etiket)
        doktor_sil_layout.addWidget(self.silinecek_doktor_secim)
        doktor_sil_layout.addWidget(self.doktor_sil_butonu)
        doktor_layout.addWidget(doktor_etiket)
        doktor_layout.addLayout(doktor_ekle_layout)
        doktor_layout.addLayout(doktor_sil_layout)
        layout.addLayout(doktor_layout)

        self.setLayout(layout)

    def load_poliklinikler(self, combo_box=None):
        if combo_box is None:
            combo_box = self.poliklinik_liste
        combo_box.clear()
        for poliklinik in poliklinikler.keys():
            combo_box.addItem(poliklinik)

    def ekle_poliklinik(self):
        yeni_poliklinik = self.yeni_poliklinik_girdi.text().strip()
        if yeni_poliklinik and yeni_poliklinik not in poliklinikler:
            poliklinikler[yeni_poliklinik] = []
            self.load_poliklinikler()
            self.load_poliklinikler(self.poliklinik_sil_secim)
            self.load_poliklinikler(self.doktor_poliklinik_secim)
            QMessageBox.information(self, "Başarılı", f"{yeni_poliklinik} polikliniği eklendi.")
            self.yeni_poliklinik_girdi.clear()
        elif yeni_poliklinik in poliklinikler:
            QMessageBox.warning(self, "Hata", f"{yeni_poliklinik} polikliniği zaten mevcut.")
        else:
            QMessageBox.warning(self, "Hata", "Lütfen bir poliklinik adı girin.")

    def sil_poliklinik(self):
        silinecek_poliklinik = self.poliklinik_sil_secim.currentText()
        if silinecek_poliklinik in poliklinikler:
            del poliklinikler[silinecek_poliklinik]
            self.load_poliklinikler()
            self.load_poliklinikler(self.poliklinik_sil_secim)
            self.load_poliklinikler(self.doktor_poliklinik_secim)
            QMessageBox.information(self, "Başarılı", f"{silinecek_poliklinik} polikliniği silindi.")
        else:
            QMessageBox.warning(self, "Hata", f"{silinecek_poliklinik} polikliniği bulunamadı.")

    def ekle_doktor(self):
        poliklinik = self.doktor_poliklinik_secim.currentText()
        yeni_doktor = self.yeni_doktor_girdi.text().strip()
        if poliklinik and yeni_doktor and yeni_doktor not in poliklinikler[poliklinik]:
            poliklinikler[poliklinik].append(yeni_doktor)
            self.load_doktorlar_for_sil()
            QMessageBox.information(self, "Başarılı", f"{poliklinik} polikliniğine {yeni_doktor} eklendi.")
            self.yeni_doktor_girdi.clear()
        elif not yeni_doktor:
            QMessageBox.warning(self, "Hata", "Lütfen bir doktor adı girin.")
        elif yeni_doktor in poliklinikler[poliklinik]:
            QMessageBox.warning(self, "Hata", f"{yeni_doktor} zaten bu poliklinikte kayıtlı.")

    def load_doktorlar_for_sil(self):
        poliklinik = self.doktor_sil_poliklinik_secim.currentText()
        self.silinecek_doktor_secim.clear()
        if poliklinik in poliklinikler:
            self.silinecek_doktor_secim.addItems(poliklinikler[poliklinik])

    def sil_doktor(self):
        poliklinik = self.doktor_sil_poliklinik_secim.currentText()
        silinecek_doktor = self.silinecek_doktor_secim.currentText()
        if poliklinik in poliklinikler and silinecek_doktor in poliklinikler[poliklinik]:
            poliklinikler[poliklinik].remove(silinecek_doktor)
            self.load_doktorlar_for_sil()
            QMessageBox.information(self, "Başarılı", f"{poliklinik} polikliniğinden {silinecek_doktor} silindi.")
        else:
            QMessageBox.warning(self, "Hata", "Doktor veya poliklinik bulunamadı.")

# Diğer sınıflar burada aynı kalır, sadece giriş kontrolü ve kullanıcı yönetimi TC üzerinden yapılır.

class AdminForm(QMainWindow):
    """Admin ekranını oluşturur."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.setWindowTitle("Admin Paneli")
        self.setGeometry(150, 150, 800, 600)  # Pencere boyutunu ayarlayabilirsiniz
        self.stacked_widget = stacked_widget

        # Ana stacked widget
        self.stacked_admin_widget = QStackedWidget()

        # Yönetim widget'larını oluştur
        self.user_manager = UserManagementWidget()
        self.appointment_manager = AppointmentManagementWidget()
        self.clinic_doctor_manager = ClinicDoctorManagementWidget()

        # Widget'ları stacked widget'a ekle
        self.stacked_admin_widget.addWidget(self.user_manager)   # İndeks 0: Kullanıcı Yönetimi
        self.stacked_admin_widget.addWidget(self.appointment_manager) # İndeks 1: Randevu Yönetimi
        self.stacked_admin_widget.addWidget(self.clinic_doctor_manager) # İndeks 2: Poliklinik/Doktor Yönetimi

        # Navigasyon butonları
        self.kullanici_yonetim_butonu = QPushButton("Kullanıcı Yönetimi")
        self.randevu_yonetim_butonu = QPushButton("Randevu Yönetimi")
        self.klinik_doktor_yonetim_butonu = QPushButton("Poliklinik/Doktor Yönetimi")
        self.geri_butonu = QPushButton("Geri Dön")

        # Butonların sinyallerini bağla
        self.kullanici_yonetim_butonu.clicked.connect(lambda: self.stacked_admin_widget.setCurrentIndex(0))
        self.randevu_yonetim_butonu.clicked.connect(lambda: self.stacked_admin_widget.setCurrentIndex(1))
        self.klinik_doktor_yonetim_butonu.clicked.connect(lambda: self.stacked_admin_widget.setCurrentIndex(2))
        self.geri_butonu.clicked.connect(self.go_back)

        # Buton layout'u
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.kullanici_yonetim_butonu)
        button_layout.addWidget(self.randevu_yonetim_butonu)
        button_layout.addWidget(self.klinik_doktor_yonetim_butonu)
        button_layout.addStretch(1)  # Butonları sola yaslar
        button_layout.addWidget(self.geri_butonu)

        # Ana layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.stacked_admin_widget)
        main_layout.addLayout(button_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def go_back(self):
        """Ana ekrana geri döner."""
        self.stacked_widget.setCurrentIndex(1)
class MainForm(QMainWindow):
    """Ana ekranı oluşturur. Kullanıcı, randevu alabilir veya randevularını görüntüleyebilir."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.setWindowTitle("Ana Ekran")
        self.setGeometry(100, 100, 400, 300)
        self.stacked_widget = stacked_widget

        # Butonlar
        self.randevu_al_butonu = QPushButton("Randevu Al", self)
        self.randevularim_butonu = QPushButton("Randevularım", self)
        self.admin_butonu = QPushButton("Admin", self)
        self.onceki_sayfa_butonu = QPushButton("Bir Önceki Sayfaya Dön", self)

        layout = QVBoxLayout()
        layout.addWidget(self.randevu_al_butonu)
        layout.addWidget(self.randevularim_butonu)
        layout.addWidget(self.admin_butonu)
        layout.addWidget(self.onceki_sayfa_butonu)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Buton bağlantıları
        self.randevu_al_butonu.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(2))
        self.randevularim_butonu.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(3))
        self.admin_butonu.clicked.connect(self.kontrol_et_ve_admin_paneline_gec) # Bağlantıyı değiştirdik
        self.onceki_sayfa_butonu.clicked.connect(self.go_back)

    def kontrol_et_ve_admin_paneline_gec(self):
        global current_tc
        yetkili_kullanicilar = ["12345678901", "10987654321"] # İbo ve Kaan'ın TC'leri

        if current_tc in yetkili_kullanicilar:
            self.stacked_widget.setCurrentIndex(4) # Admin panelinin indeksi (genellikle 4)
        else:
            QMessageBox.warning(self, "Yetkisiz Erişim", "Bu bölüme erişim yetkiniz bulunmamaktadır.")

    def go_back(self):
        """Ana ekrana geri döner."""
        self.stacked_widget.setCurrentIndex(0)

class AppointmentsListForm(QMainWindow):
    """Randevuların listeleneceği ekranı oluşturur."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.setWindowTitle("Randevularım")
        self.setGeometry(150, 150, 400, 300)
        self.stacked_widget = stacked_widget
        self.randevular_listesi = QTableWidget(self)
        self.onceki_sayfa_butonu = QPushButton("Bir Önceki Sayfaya Dön", self)

        layout = QVBoxLayout()
        layout.addWidget(self.randevular_listesi)
        layout.addWidget(self.onceki_sayfa_butonu)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.onceki_sayfa_butonu.clicked.connect(self.go_back)

    def showEvent(self, event):
        """Pencere her gösterildiğinde randevuları yeniden yükler."""
        super().showEvent(event)
        self.load_appointments_for_user()

    def load_appointments_for_user(self):
        """Giriş yapan kullanıcının randevularını dosyadan okur ve tabloya yükler."""
        if not current_tc:
            self.randevular_listesi.setRowCount(0)
            return

        file_name = f"{current_tc}_appointments.txt"
        appointments_for_user = []
        if os.path.exists(file_name):
            with open(file_name, 'r') as f:
                appointments_for_user = [line.strip() for line in f]

        self.randevular_listesi.setRowCount(len(appointments_for_user))
        self.randevular_listesi.setColumnCount(1)
        self.randevular_listesi.setHorizontalHeaderLabels(["Randevular"])
        for i, appointment in enumerate(appointments_for_user):
            self.randevular_listesi.setItem(i, 0, QTableWidgetItem(appointment))

    def go_back(self):
        """Ana ekrana geri döner."""
        self.stacked_widget.setCurrentIndex(1)
class AppointmentForm(QMainWindow):
    """Randevu alma ekranını oluşturur."""
    def __init__(self, stacked_widget):
        super().__init__()
        self.setWindowTitle("Randevu Alma")
        self.setGeometry(150, 150, 400, 300)
        self.stacked_widget = stacked_widget

        # Poliklinik seçimi
        self.poliklinik_etiket = QLabel("Poliklinik:", self)
        self.poliklinik_secim = QComboBox(self)
        self.guncelle_poliklinik_listesi() # Başlangıçta poliklinikleri yükle
        self.poliklinik_secim.currentIndexChanged.connect(self.update_doctors)

        # Doktor seçimi
        self.doktor_etiket = QLabel("Doktor:", self)
        self.doktor_secim = QComboBox(self)
        self.update_doctors() # Başlangıçta ilk polikliniğin doktorlarını yükle

        # Tarih seçimi
        self.tarih_etiket = QLabel("Tarih:", self)
        self.tarih_girdi = QDateEdit(self)
        self.tarih_girdi.setDate(QDate.currentDate())

        # Randevu al butonu
        self.randevu_al_butonu = QPushButton("Randevu Al", self)
        self.randevu_al_butonu.clicked.connect(self.book_appointment)

        layout = QVBoxLayout()
        layout.addWidget(self.poliklinik_etiket)
        layout.addWidget(self.poliklinik_secim)
        layout.addWidget(self.doktor_etiket)
        layout.addWidget(self.doktor_secim)
        layout.addWidget(self.tarih_etiket)
        layout.addWidget(self.tarih_girdi)
        layout.addWidget(self.randevu_al_butonu)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def guncelle_poliklinik_listesi(self):
        """Poliklinik ComboBox'ını güncel global poliklinikler sözlüğünden doldurur."""
        self.poliklinik_secim.clear()
        for poliklinik in poliklinikler.keys():
            self.poliklinik_secim.addItem(poliklinik)

    def update_doctors(self):
        """Seçilen polikliniğe göre doktor ComboBox'ını günceller."""
        secilen_poliklinik = self.poliklinik_secim.currentText()
        self.doktor_secim.clear()
        if secilen_poliklinik in poliklinikler:
            self.doktor_secim.addItems(poliklinikler[secilen_poliklinik])

    def book_appointment(self):
        """Yeni bir randevu alır."""
        doctor = self.doktor_secim.currentText()
        date = self.tarih_girdi.date().toString(Qt.ISODate)
        poliklinik = self.poliklinik_secim.currentText() # Polikliniği de alalım
        if doctor and date and poliklinik:
            appointments.append(f"{current_tc}_{poliklinik}-{doctor} - {date}") # Polikliniği de randevu bilgisine ekleyelim
            save_appointments()  # Randevu kaydedilsin
            QMessageBox.information(self, "Başarılı", "Randevu alındı!")
            self.stacked_widget.setCurrentIndex(1)
        else:
            QMessageBox.warning(self, "Hata", "Tüm alanları doldurun!")

    def showEvent(self, event):
        """Pencere her gösterildiğinde poliklinik listesini günceller."""
        super().showEvent(event)
        self.guncelle_poliklinik_listesi()
        self.update_doctors() # Mevcut polikliniğin doktorlarını da güncelle
# Uygulama başlatma kodu
if __name__ == "__main__":
    app = QApplication(sys.argv)
    # İşte stil tanımını yapıştırdığımız yer!
    stil = """
        QMainWindow {
            background-color: #abe2f5; /* Açık gri ana pencere */
        }
        QComboBox:focus {
                border: 2px solid pink; /* Odaklandığında mavi bir kenarlık */
                outline: lightyellow;/* İsteğe bağlı: varsayılan odaklanma çizgisini kaldırır */
            }
            QDialog {
            background-color: #abe2f5; /* Diyalog pencereleri (RegisterDialog gibi) için farklı bir renk */
        }

         QLineEdit:focus {
                border: 2px solid green;
                background-color: lightyellow; /* İsteğe bağlı */
            }
    """

    app.setStyleSheet(stil)


    # Stili uygulamak için bu satırı ekleyin
    stacked_widget = QStackedWidget()


    # Ekranları oluşturuyoruz
    # Ekranları oluşturuyoruz
    login_form = LoginForm(stacked_widget)
    main_form = MainForm(stacked_widget)
    appointment_form = AppointmentForm(stacked_widget)
    appointments_list_form = AppointmentsListForm(stacked_widget)
    admin_form = AdminForm(stacked_widget)  # Admin ekranını oluşturduk

    # Ekranları stacked_widget'e ekliyoruz
    stacked_widget.addWidget(login_form)
    stacked_widget.addWidget(main_form)
    stacked_widget.addWidget(appointment_form)
    stacked_widget.addWidget(appointments_list_form)
    stacked_widget.addWidget(admin_form)  # Admin ekranını ekledik

    # Başlangıçta giriş ekranını gösteriyoruz
    stacked_widget.setCurrentIndex(0)

    # Uygulamayı başlatıyoruz
    stacked_widget.show()
    sys.exit(app.exec_())
