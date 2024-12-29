import pygame
import random
def spacewariors():
    # Pygame'i başlat
    pygame.init()

    # Ekran boyutları
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Space Warriors - Ters Roket Düşmanlar")

    # Renkler
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    YELLOW = (255, 255, 0)
    GRAY = (169, 169, 169)  # Duman rengi

    # FPS ayarı
    clock = pygame.time.Clock()
    FPS = 60

    # Oyun fonksiyonu
    def game_loop():
        # Oyuncu konumu
        player_x = WIDTH // 2
        player_y = HEIGHT - 100
        player_speed = 5

        # Mermiler
        bullets = []
        bullet_speed = 7

        # Düşmanlar
        enemy_count = 5
        enemies = [{"x": random.randint(0, WIDTH - 50), "y": random.randint(-100, -40), "speed": random.randint(1, 3)} for _ in range(enemy_count)]

        # Puanlama
        score = 0
        font = pygame.font.Font(None, 36)

        # Oyun durumu
        game_over = False

        # Oyuncu roketini çiz
        def draw_rocket(x, y):
            # Roket gövdesi
            pygame.draw.polygon(screen, WHITE, [(x + 25, y), (x, y + 50), (x + 50, y + 50)])
            # Roket motoru
            pygame.draw.rect(screen, RED, (x + 10, y + 50, 10, 20))
            pygame.draw.rect(screen, RED, (x + 30, y + 50, 10, 20))
            # Roket kanatları
            pygame.draw.polygon(screen, RED, [(x + 5, y + 40), (x + 25, y + 35), (x + 45, y + 40)])
            # Duman
            pygame.draw.circle(screen, GRAY, (x + 25, y + 70), 5)

        # Düşman roketini ters çiz
        def draw_enemy_rocket(x, y):
            # Düşman roketinin gövdesi
            pygame.draw.polygon(screen, WHITE, [(x, y), (x + 50, y), (x + 25, y + 50)])
            # Düşman roket motoru
            pygame.draw.rect(screen, RED, (x + 10, y - 20, 10, 20))
            pygame.draw.rect(screen, RED, (x + 30, y - 20, 10, 20))
            # Düşman roket kanatları
            pygame.draw.polygon(screen, RED, [(x + 5, y + 10), (x + 25, y + 5), (x + 45, y + 10)])
            # Duman
            pygame.draw.circle(screen, GRAY, (x + 25, y - 30), 5)

        # Oyun döngüsü
        running = True
        while running:
            screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Ateş etme
                if not game_over and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullets.append({"x": player_x + 22, "y": player_y})

                # Enter tuşuna basıldığında oyunu yeniden başlat
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and game_over:
                    game_loop()  # Yeni oyun başlat

                # Z tuşuna basıldığında pencereyi kapat
                if event.type == pygame.KEYDOWN and event.key == pygame.K_z:
                    running = False

            # Oyuncu hareketi (WASD tuşları ile)
            if not game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a] and player_x > 0:  # A tuşu ile sola hareket
                    player_x -= player_speed
                if keys[pygame.K_d] and player_x < WIDTH - 50:  # D tuşu ile sağa hareket
                    player_x += player_speed
                if keys[pygame.K_w] and player_y > 0:  # W tuşu ile yukarı hareket
                    player_y -= player_speed
                if keys[pygame.K_s] and player_y < HEIGHT - 50:  # S tuşu ile aşağı hareket
                    player_y += player_speed

            # Mermileri hareket ettir
            for bullet in bullets[:]:
                bullet["y"] -= bullet_speed
                if bullet["y"] < 0:
                    bullets.remove(bullet)

            # Düşmanları hareket ettir ve çarpışma kontrolü
            for enemy in enemies[:]:
                enemy["y"] += enemy["speed"]
                if enemy["y"] > HEIGHT:
                    enemy["x"] = random.randint(0, WIDTH - 50)
                    enemy["y"] = random.randint(-100, -40)
                    enemy["speed"] = random.randint(1, 3)

                # Mermi ve düşman çarpışması
                for bullet in bullets[:]:
                    if enemy["x"] < bullet["x"] < enemy["x"] + 50 and enemy["y"] < bullet["y"] < enemy["y"] + 50:
                        enemies.remove(enemy)
                        bullets.remove(bullet)
                        score += 1
                        break

                # Oyuncu ve düşman çarpışması
                if enemy["x"] < player_x < enemy["x"] + 50 and enemy["y"] + 50 > player_y:
                    game_over = True

            # Yeni düşman oluştur
            while len(enemies) < enemy_count:
                enemies.append({"x": random.randint(0, WIDTH - 50), "y": random.randint(-100, -40), "speed": random.randint(1, 3)})

            # Oyuncu roketini çiz
            if not game_over:
                draw_rocket(player_x, player_y)

            # Mermileri çiz
            for bullet in bullets:
                pygame.draw.rect(screen, YELLOW, (bullet["x"], bullet["y"], 5, 10))

            # Düşman roketlerini ters çiz
            for enemy in enemies:
                draw_enemy_rocket(enemy["x"], enemy["y"])

            # Skor ekrana yazdır
            score_text = font.render(f"Score: {score}", True, WHITE)
            screen.blit(score_text, (10, 10))

            # Game Over mesajı
            if game_over:
                game_over_text = font.render("GAME OVER", True, RED)
                screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 20))
                restart_text = font.render("Press ENTER to Restart", True, WHITE)
                screen.blit(restart_text, (WIDTH // 2 - 150, HEIGHT // 2 + 20))

            pygame.display.flip()
            clock.tick(FPS)

    # İlk oyun başlatma
    game_loop()

    # Pygame'i kapat
    pygame.quit()


import pygame
import random

# Değişkenlerin başlangıç değerlerini dışarıda tanımlıyoruz
user_choice = None
computer_choice = None
result = ""

def rps():
    global user_choice, computer_choice, result  # Bu değişkenlerin global olarak kullanılacağını belirtiriz
    pygame.init()

    # Renkler
    WHITE = (255, 255, 255)
    BLACK = (120, 25, 33)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    # Ekran boyutu
    WIDTH, HEIGHT = 600, 400
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Taş, Kağıt, Makas")

    # Yazı fontu
    font = pygame.font.Font(None, 36)

    # Seçenekler
    choices = ["S", "D", "A"]  # Taş (S), Kağıt (D), Makas (A)

    # Seçim talimatlarını çiz
    def draw_instructions():
        instruction_text = font.render("Taş için 'S', Kağıt için 'D', Makas için 'A' tuşlayın.", True, WHITE)
        screen.blit(instruction_text, (WIDTH // 2 - instruction_text.get_width() // 2, HEIGHT // 3))

    # Bilgisayarın seçim yapması
    def get_computer_choice():
        return random.choice(choices)

    # Kazananı belirleme
    def determine_winner(user_choice, computer_choice):
        if user_choice == computer_choice:
            return "Beraberlik!"
        elif (user_choice == 'S' and computer_choice == 'A') or \
             (user_choice == 'D' and computer_choice == 'S') or \
             (user_choice == 'A' and computer_choice == 'D'):
            return "Kazandınız!"
        else:
            return "Bilgisayar kazandı!"

    # Ana oyun döngüsü
    def play_game():
        global user_choice, computer_choice, result  # Bu değişkenlerin global olarak kullanılacağını belirtiriz

        running = True
        while running:
            screen.fill(BLACK)

            # Oyun başlıkları
            title_text = font.render("Taş, Kağıt, Makas", True, WHITE)
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 20))

            # Talimatları çiz
            draw_instructions()

            # Sonuç metnini çiz
            if user_choice is not None and computer_choice is not None:
                result_text = font.render(f"Sonuç: {result}", True, WHITE)
                screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, HEIGHT // 2))

            # Kullanıcı seçimleri
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Klavye tuşlarına basma
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:  # Taş
                        user_choice = "S"
                    elif event.key == pygame.K_d:  # Kağıt
                        user_choice = "D"
                    elif event.key == pygame.K_a:  # Makas
                        user_choice = "A"

                    if user_choice:
                        computer_choice = get_computer_choice()
                        result = determine_winner(user_choice, computer_choice)

            pygame.display.flip()

    # Oyun başlat
    play_game()

    # Pygame'i kapat
    pygame.quit()

