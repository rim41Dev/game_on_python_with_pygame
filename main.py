import pygame
from random import choice, randint

# import time as t

pygame.init()
BLACK = (255, 255, 255)
W = 900
H = 800
RED = (255, 0, 0)
screen = pygame.display.set_mode((H, W))
# print(screen.get_rect())
FPS = 300
bg = pygame.image.load("bg.png").convert()
coin = pygame.image.load("coin.png").convert()
car = pygame.image.load("car.jpg").convert()
knife = pygame.image.load("knife.jpg").convert()
car.set_colorkey(BLACK)
coin.set_colorkey(BLACK)
knife.set_colorkey(BLACK)
coin = pygame.transform.scale(coin, (300, 300))
bg = pygame.transform.scale(bg, (H, W))
car = pygame.transform.scale(car, (200, 400))
# knife = pygame.transform.scale(knife, (200, 400))
d = pygame.display
d.set_caption('Need For Speed 2')
clock = pygame.time.Clock()
speed = 1
all_sprites = pygame.sprite.Group()


class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = car
        self.rect = self.image.get_rect()
        self.rect.center = (H // 2, 530)

    def move(self, mot):
        if mot == 'l':
            self.rect.x -= speed * 3
        if mot == 'r':
            self.rect.x += speed * 3


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = coin
        self.rect = self.image.get_rect()
        self.rect.center = (-200, -200)

    def gen(self):
        self.rect.center = (randint(100, W - 100), -50)

    def update(self):
        self.rect.y += speed
        if self.rect.y >= H + 200:
            self.gen()


class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = knife
        self.rect = self.image.get_rect()
        self.rect.center = (-200, -200)
        self.radius = 50
        pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

    def gen(self):
        self.rect.center = (randint(150, W - 150), -150)

    def update(self):
        self.rect.y += speed
        if self.rect.y >= H + 300:
            self.gen()


class White(pygame.sprite.Sprite):
    def __init__(self, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 60))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect()
        self.radius = 50
        self.rect.center = (H // 2, y)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)

    def gen(self):
        self.rect.center = (H // 2, -15)

    def update(self):
        self.rect.y += speed
        if self.rect.y >= H + 180:
            self.gen()


def main():
    global speed
    f = pygame.font.SysFont('arial', 36)
    mot = ''
    score = 0
    run = True
    all_sprites = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    rocks = pygame.sprite.Group()
    player = Car()
    prise = Coin()
    rock = Rock()
    l_whites = [White(i * 90) for i in range(11)]
    for x in l_whites:
        all_sprites.add(x)
    all_sprites.add(rock)
    rocks.add(rock)
    coins.add(prise)
    all_sprites.add(player)
    all_sprites.add(prise)
    prise.gen()
    rock.gen()
    text2 = f.render("Ты проиграл:(", False, (0, 0, 0))
    isFast = False
    gamemode = 0
    while run:
        all_sprites.update()
        isHitsDie = pygame.sprite.spritecollide(player, rocks, False, pygame.sprite.collide_circle_ratio(0.91))
        isHitsPrise = pygame.sprite.spritecollide(player, coins, False, pygame.sprite.collide_rect_ratio(0.65))
        if isHitsDie:
            gamemode = 1
        if isHitsPrise:
            score += 1
            prise.gen()
            print(score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    mot = 'r'

                if event.key == pygame.K_LEFT:
                    mot = 'l'

                if event.key == pygame.K_SPACE:
                    if gamemode == 1:
                        main()
                    elif gamemode == 0:
                        isFast = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    isFast = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    mot = ''
        if gamemode == 0:
            if not isFast:
                speed = 1
            if isFast:
                speed += 0.01
            # screen.blit(bg, (0, 0))
            screen.fill((0, 0, 0))
            for x in l_whites:
                x.update()
            prise.update()
            rock.update()

            player.move(mot)
            all_sprites.draw(screen)
        if gamemode == 1:
            speed = 1
            screen.fill((255, 255, 255))
            screen.blit(text2, (W // 2, H // 2))
        d.update()
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
