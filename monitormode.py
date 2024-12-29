import tkinter as tk
import sys
import subprocess
from sys import maxsize
from cardvalue import read_card

# Kartı okuma
interface = read_card()

# 'ifconfig' komutunun sistemde mevcut olup olmadığını kontrol etme
try:
    subprocess.call(["ifconfig"])
except FileNotFoundError:
    print("Hata: 'ifconfig' komutu bulunamadı. Sisteminizde yüklü mü?")
    exit(1)

# Airmon-ng ile arayüzü monitör moduna alma
try:
    subprocess.run(["sudo", "airmon-ng", "start", interface], check=True)
except subprocess.CalledProcessError as e:
    print(f"Hata: 'airmon-ng' komutunu çalıştırırken bir sorun oluştu: {e}")
    exit(1)

# Yeni ağ adaptörü adı
new_interface_name = ""

# iwconfig komutunu çalıştırarak arayüzü kontrol etme
result = subprocess.run(["iwconfig", interface], capture_output=True, text=True)

# Arayüz monitör modunda mı kontrol et
if "Mode:Monitor" in result.stdout:
    print(f"{interface} şu anda monitör modunda.")

    # Monitör modunda olan kartın adını kontrol et
    new_interface = [line for line in result.stdout.splitlines() if "Monitor" in line]
    if new_interface:
        new_interface_name = new_interface[0].split()[0]
        print(f"Yeni ağ adaptörü adı: {new_interface_name}")
else:
    print(f"{interface} monitör modunda değil.")

with open("card2.txt", "w") as file:
    file.write(new_interface_name)