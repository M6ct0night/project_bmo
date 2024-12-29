def read_card2():
    try:
        with open("card2.txt", "r") as file:
            card_value = file.read().strip()  # Dosyadan değeri oku ve boşlukları temizle
        return card_value
    except FileNotFoundError:
        print("değer bulunamadı")# Eğer dosya bulunamazsa, bir hata yerine bir varsayılan değer döndür
        return None