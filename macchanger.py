import tkinter as tk
import random
import subprocess
import time
import os
from cardvalue import read_card

arayuz = read_card()


def change_family_members_back(event):
    # Aile üyeleri listesini belirleyin
    new_members = ["5","10","15","30"]

    # Şu anki metni değiştir
    current_text = label.cget("text")

    # Yeni metni bulmak için mevcut metnin konumunu bul
    if current_text in new_members:
        # Eğer mevcut metin aile üyeleri listesinde varsa, bir önceki üyeye geç
        prev_index = (new_members.index(current_text) - 1) % len(new_members)
        new_text = new_members[prev_index]
    else:
        # Başlangıçta "nene" yazıyorsa ilk aile üyesine geç
        new_text = new_members[0]

    # Label üzerindeki metni güncelle
    label.config(text=new_text)


def change_family_members(event):
    # Aile üyeleri listesini belirleyin
    new_members = ["5","10","15","30"]

    # Şu anki metni değiştir
    current_text = label.cget("text")

    # Yeni metni bulmak için mevcut metnin konumunu bul
    if current_text in new_members:
        # Eğer mevcut metin aile üyeleri listesinde varsa, bir sonraki üyeye geç
        next_index = (new_members.index(current_text) + 1) % len(new_members)
        new_text = new_members[next_index]
    else:
        # Başlangıçta "nene" yazıyorsa ilk aile üyesine geç
        new_text = new_members[0]

    # Label üzerindeki metni güncelle
    label.config(text=new_text)

def generate_mac():
    return ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))

def stagame(event):
    current_text = label.cget("text")
    z = int(current_text)
    label.config("mac değiştiriliyor")
    def macChanger(arayuz):
        mac = generate_mac()
        try:
            subprocess.call(["ifconfig", arayuz, "down"])
            subprocess.call(["ifconfig", arayuz, "hw", "ether", mac])
            subprocess.call(["ifconfig", arayuz, "up"])
        except Exception as e:
            print(f"Hata: MAC adresi değiştirilemedi. Detay: {e}")
            exit(1)
    try:
        while True:
            macChanger(arayuz)
            countdown(z * 60)  # Geri sayım için

def stgame(event):
    # Yazıyı eklemek için label'ı güncelle
    label.config(text="5")  # Başlangıçta görülecek yazı


# Ana pencereyi oluştur
root = tk.Tk()
root.title("macchanger")
root.minsize(height=320, width=480)



try:
    resim = tk.PhotoImage(file="BADBMMOO.png")
    # Arka plan resmi eklemek için bir Label widget'ı oluştur
    background_label = tk.Label(root, image=resim)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Etiketin pencereye tam oturmasını sağlar
except Exception as e:
    print(f"Resim yüklenemedi: {e}")


# Label widget'ını oluştur ve yazıyı ekle
label = tk.Label(root, text="", font=("Arial", 24), fg="black",
                 bg="#C6E4C0")  # bg ekleyerek daha görünür yapabilirsiniz

label.pack(side="bottom", pady=20, )


# 'Enter' tuşu ile yazıyı ekle
root.bind("<Return>", stgame)


# 'A' tuşu ile bir önceki oyunu seç
root.bind("<a>", change_family_members_back)
root.bind("<A>", change_family_members_back)


# 'D' tuşu ile bir sonraki oyunu seç
root.bind("<d>", change_family_members)
root.bind("<D>", change_family_members)


# 'W' tuşu ile seçilen oyunu başlat
root.bind("<w>", stagame)
root.bind("<W>", stagame)


root.bind("Z",lambda event: os.system("python badbmo.py"))
root.bind("s",lambda event:root.quit() )
root.mainloop()