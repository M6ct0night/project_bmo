import tkinter as tk
import subprocess
import re
import os

# ifconfig komutunu çalıştır ve çıktısını al
result = subprocess.run(['ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Çıktıyı al
output = result.stdout

# Arayüz isimlerini almak için bir regex kullan
# Arayüzler genellikle bir satırın başında yer alır
interfaces = re.findall(r'^\S+', output, re.MULTILINE)

def change_family_members_back(event):
    # Aile üyeleri listesini belirleyin
    global interfaces

    # Şu anki metni değiştir
    current_text = label.cget("text")
    truecard=current

    # Yeni metni bulmak için mevcut metnin konumunu bul
    if current_text in interfaces:
        # Eğer mevcut metin aile üyeleri listesinde varsa, bir önceki üyeye geç
        prev_index = (interfaces.index(current_text) - 1) % len(interfaces)
        new_text = interfaces[prev_index]

    else:
        # Başlangıçta "nene" yazıyorsa ilk aile üyesine geç
        new_text = interfaces[0]

    # Label üzerindeki metni güncelle
    label.config(text=new_text)


def change_family_members(event):
    # Aile üyeleri listesini belirleyin
    global interfaces

    # Şu anki metni değiştir
    current_text = label.cget("text")

    # Yeni metni bulmak için mevcut metnin konumunu bul
    if current_text in interfaces:
        # Eğer mevcut metin aile üyeleri listesinde varsa, bir sonraki üyeye geç
        next_index = (interfaces.index(current_text) + 1) % len(interfaces)
        new_text = interfaces[next_index]
    else:
        # Başlangıçta "nene" yazıyorsa ilk aile üyesine geç
        new_text = interfaces[0]

    # Label üzerindeki metni güncelle
    label.config(text=new_text)

    # Şu anki metni değiştir
    current_text = label.cget("text")

    # Yeni metni bulmak için mevcut metnin konumunu bul
    if current_text in interfaces:
        # Eğer mevcut metin aile üyeleri listesinde varsa, bir sonraki üyeye geç
        next_index = (interfaces.index(current_text) + 1) % len(interfaces)
        new_text = interfaces[next_index]

    else:
        # Başlangıçta "nene" yazıyorsa ilk aile üyesine geç
        new_text = interfaces[0]

    # Label üzerindeki metni güncelle
    label.config(text=new_text)

cardd = ""
def stagame(event):
    global cardd
    cardd = label.cget("text")
    trueval= cardd[::-1]
    # 'card.txt' dosyasına seçilen arayüzü kaydet
    with open("card.txt", "w") as file:
        file.write(trueval)

    # 'badbmo.py' dosyasını çalıştır
    os.system("python badbmo.py")
def stgame(event):
    # Yazıyı eklemek için label'ı güncelle
    label.config(text=interfaces[0])  # Başlangıçta görülecek yazı


# Ana pencereyi oluştur
root = tk.Tk()
root.title("bmoo")
root.minsize(height=320, width=480)



try:
    resim = tk.PhotoImage(file="BMMOO.png")
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

root.mainloop()
