# add library
import math
import pygame
from pygame import mixer
import random

# int
pygame.init()

# background
background = pygame.image.load('background space.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("space invador")
icon = pygame.image.load('spaceshipicon.png')
pygame.display.set_icon(icon)

# player
playerimg = pygame.image.load('player.png')
playerX = 355
playerY = 420
playerX_change = 0

# alien
alienimg = []
alienX = []
alienY = []
alienX_change = []
alienY_change = []
num_of_aliens = 5
for i in range(num_of_aliens):
    alienimg.append(pygame.image.load('alien.png'))
    alienX.append(random.randint(0, 800))
    alienY.append(random.randint(50, 150))
    alienX_change.append(1)
    alienY_change.append(40)

# bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 10
bullet_state = "ready"

score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over txt
over_font = pygame.font.Font('freesansbold.ttf', 43)


def show_score(x, y):
    score = font.render("score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_txt = over_font.render("GAME OVER   YOUR SCORE IS: " + str(score_value), True, (255, 0, 0))
    screen.blit(over_txt, (55, 250))


def player(x, y):
    screen.blit(playerimg, (x, y))


def alien(x, y, i):
    screen.blit(alienimg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y - 40))


def isCollision(alienX, alienY, bulletX, bulletY):
    distance = math.sqrt(math.pow(alienX - bulletX, 2)) + (math.pow(alienY - bulletY, 2))
    if distance < 27:
        return True
    else:
        return False


# screen
screen = pygame.display.set_mode((800, 600))
running = True
while running:

    screen.fill((192, 192, 192))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -4
            if event.key == pygame.K_RIGHT:
                playerX_change = 4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or pygame.K_LEFT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    for i in range(num_of_aliens):

        if alienY[i] > 440:
            for j in range(num_of_aliens):
                alienY[j] = 2000
            game_over_text()
            break

        alienX[i] += alienX_change[i]
        if alienX[i] <= 0:
            alienX_change[i] = 1
            alienY[i] += alienY_change[i]
        elif alienX[i] >= 736:
            alienX_change[i] = -1
            alienY[i] += alienY_change[i]

        collision = isCollision(alienX[i], alienY[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            alienX[i] = random.randint(0, 735)
            alienY[i] = random.randint(50, 150)
        alien(alienX[i], alienY[i], i)

    # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
