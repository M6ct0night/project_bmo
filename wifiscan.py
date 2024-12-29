import subprocess
import re
from cardmon import read_card2
import tkinter as tk
from tkinter import messagebox
import os

# Ağ kartı arayüzünü okuma
interface2 = read_card2()


# Ağ taramasını yapan fonksiyon
def scan_network(interface):
    # Airmon-ng komutunu kullanarak, ağ taraması yapmak için kullanılan arayüzü başlatıyoruz
    subprocess.run(['airmon-ng', 'start', interface])

    # İstenilen ağları tarama komutunu çalıştırıyoruz
    output = subprocess.check_output(['airodump-ng', '--output-format', 'csv', '--write', 'network_scan', interface])

    # CSV dosyasındaki bilgileri okuyoruz
    with open('network_scan-01.csv', 'r') as file:
        lines = file.readlines()

    networks = []
    for line in lines:
        # SSID'yi ayıklıyoruz
        if 'BSSID' in line:
            continue
        parts = line.split(';')
        if len(parts) > 5:
            ssid = parts[13]  # Sadece SSID'yi alıyoruz
            networks.append(ssid)

    return networks


# Verileri dosyaya kaydetme fonksiyonu
def save_networks_to_file(networks):
    # Önce dosyayı sıfırlıyoruz
    with open('networks.txt', 'w') as file:
        for i, ssid in enumerate(networks):
            file.write(f"{i + 1}. SSID: {ssid}\n")


# Tkinter ile ağ bilgilerini ekranda gösterme fonksiyonu
def display_networks(networks):
    root = tk.Tk()
    root.title("Ağ Tarama Sonuçları")

    # Pencere boyutunu ayarlıyoruz
    root.geometry("320x480")

    label = tk.Label(root, text="Ağ Bilgileri", font=('Arial', 14))
    label.pack(pady=10)

    listbox = tk.Listbox(root, width=40, height=15)  # Ekran boyutuna göre listbox boyutu ayarlandı
    listbox.pack(pady=10)

    # Listeyi güncelleme fonksiyonu
    def update_listbox():
        listbox.delete(0, tk.END)  # Eski ağları sil
        for i, ssid in enumerate(networks):
            listbox.insert(tk.END, f"{i + 1}. SSID: {ssid}")  # SSID'leri numaralandırarak ekliyoruz

    # Ağ taramasını başlatan fonksiyon
    def start_scanning():
        try:
            new_networks = scan_network(interface2)
            save_networks_to_file(new_networks)
            networks.clear()
            networks.extend(new_networks)
            update_listbox()  # Listbox'ı güncelle
        except Exception as e:
            messagebox.showerror("Hata", f"Ağ taraması sırasında bir hata oluştu: {e}")

        # Tarama işlemini belirli bir aralıkla tekrar başlatıyoruz (2 saniye aralıklarla)
        root.after(2000, start_scanning)

    # Başlangıçta taramayı başlatıyoruz
    start_scanning()

    # Enter tuşuna basıldığında tarama işlemi duracak ve program kapanacak
    def on_enter(event):
        root.quit()  # Tkinter penceresini kapatır

    # Enter tuşunu dinleyerek on_enter fonksiyonunu çalıştırıyoruz
    root.bind('<Return>', on_enter)

    root.mainloop()


# Ana fonksiyon
def main():
    try:
        networks = []  # Ağları saklamak için bir liste
        display_networks(networks)
    except Exception as e:
        messagebox.showerror("Hata", f"Ağ taraması sırasında bir hata oluştu: {e}")


if __name__ == "__main__":
    main()
