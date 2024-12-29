import pygame
import random

# Ekran boyutları
SCREEN = WIDTH, HEIGHT = (480, 320)
FPS = 60

class Ground():
    def __init__(self):
        self.image = pygame.image.load('Assets/ground.png')
        self.rect = self.image.get_rect()

        self.width = self.image.get_width()
        self.x1 = 0
        self.x2 = self.width
        self.y = HEIGHT - 50  # Toprak yüksekliği

    def update(self, speed):
        self.x1 -= speed
        self.x2 -= speed

        if self.x1 <= -self.width:
            self.x1 = self.width

        if self.x2 <= -self.width:
            self.x2 = self.width

    def draw(self, win):
        win.blit(self.image, (self.x1, self.y))
        win.blit(self.image, (self.x2, self.y))

class Dino():
    def __init__(self, x, y):
        self.x, self.base = x, HEIGHT - 50  # Yeni taban yüksekliği

        self.run_list = []
        self.duck_list = []

        for i in range(1, 4):
            img = pygame.image.load(f'Assets/Dino/{i}.png')
            img = pygame.transform.scale(img, (52, 58))
            self.run_list.append(img)

        for i in range(4, 6):
            img = pygame.image.load(f'Assets/Dino/{i}.png')
            img = pygame.transform.scale(img, (70, 38))
            self.duck_list.append(img)

        self.dead_image = pygame.image.load(f'Assets/Dino/8.png')
        self.dead_image = pygame.transform.scale(self.dead_image, (52, 58))

        self.reset()

        self.vel = 0
        self.gravity = 1
        self.jumpHeight = 15
        self.isJumping = False

    def reset(self):
        self.index = 0
        self.image = self.run_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.bottom = self.base

        self.alive = True
        self.counter = 0

    def update(self, jump, duck):
        if self.alive:
            if not self.isJumping and jump:
                self.vel = -self.jumpHeight
                self.isJumping = True

            self.vel += self.gravity
            if self.vel >= self.jumpHeight:
                self.vel = self.jumpHeight

            self.rect.y += self.vel
            if self.rect.bottom > self.base:
                self.rect.bottom = self.base
                self.isJumping = False

            if duck:
                self.counter += 1
                if self.counter >= 6:
                    self.index = (self.index + 1) % len(self.duck_list)
                    self.image = self.duck_list[self.index]
                    self.rect = self.image.get_rect()
                    self.rect.x = self.x
                    self.rect.bottom = self.base
                    self.counter = 0

            elif self.isJumping:
                self.index = 0
                self.counter = 0
                self.image = self.run_list[self.index]
            else:
                self.counter += 1
                if self.counter >= 4:
                    self.index = (self.index + 1) % len(self.run_list)
                    self.image = self.run_list[self.index]
                    self.rect = self.image.get_rect()
                    self.rect.x = self.x
                    self.rect.bottom = self.base
                    self.counter = 0

            self.mask = pygame.mask.from_surface(self.image)

        else:
            self.image = self.dead_image

    def draw(self, win):
        win.blit(self.image, self.rect)

class Cactus(pygame.sprite.Sprite):
    def __init__(self, type):
        super(Cactus, self).__init__()

        self.image_list = []
        for i in range(5):
            scale = 0.5  # Daha küçük ekran için ölçek
            img = pygame.image.load(f'Assets/Cactus/{i+1}.png')
            w, h = img.get_size()
            img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
            self.image_list.append(img)

        self.image = self.image_list[type - 1]
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + 10
        self.rect.bottom = HEIGHT - 50  # Toprağa hizalı

    def update(self, speed, dino):
        if dino.alive:
            self.rect.x -= speed
            if self.rect.right <= 0:
                self.kill()

            self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win):
        win.blit(self.image, self.rect)

class Game():
    def __init__(self):
        pygame.init()
        self.win = pygame.display.set_mode(SCREEN)
        pygame.display.set_caption("Dino Run")
        self.clock = pygame.time.Clock()

        self.ground = Ground()
        self.dino = Dino(50, HEIGHT - 50)

        self.cactus_group = pygame.sprite.Group()
        self.spawn_timer = 0

        self.speed = 5

    def run(self):
        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            jump = keys[pygame.K_SPACE]
            duck = keys[pygame.K_DOWN]

            self.dino.update(jump, duck)

            self.spawn_timer += 1
            if self.spawn_timer >= 90:
                cactus = Cactus(random.randint(1, 5))
                self.cactus_group.add(cactus)
                self.spawn_timer = 0

            self.cactus_group.update(self.speed, self.dino)

            self.ground.update(self.speed)

            self.draw()

        pygame.quit()

    def draw(self):
        self.win.fill((255, 255, 255))
        self.ground.draw(self.win)
        self.dino.draw(self.win)
        self.cactus_group.draw(self.win)
        pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()
