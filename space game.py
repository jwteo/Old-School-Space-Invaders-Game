import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()
# Create the screen: Width x Height
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('background.png')

# background sound
mixer.music.load('background.wav')
mixer.music.play(-1) # play on loop, not just once

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('monster.png'))
    enemyX.append(random.randint(0, 735)) # We want out enemy to appear at random positions
    enemyY.append(random.randint(50, 150)) # We want out enemy to appear at random positions
    enemyX_change.append(3)
    enemyY_change.append(40)

# Bullet
# Ready State --> Can't see bullet on the screen
# Fire State --> bullet is currently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480 # shooting the bullet from the top of the spaceship
bulletX_change = 4
bulletY_change = 10
bullet_state = 'ready'

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 0
textY = 0

# Game Over Text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render('Score : ' + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render('GAME OVER', True, (0, 255, 0))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))  # .blit() means draw, (x, y) is the coordinate

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))  # .blit() means draw

def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x+16, y+10))
    # plus 16 and 10 so that bullet is being shot from the middle of the player

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX)**2 + (enemyY - bulletY)**2)
    if distance < 27:
        return True
    return False

# Create an infinite loop (game loop)--> all the things you want to display persistently on the screen,
# add inside the loop
running = True
while running:
    screen.fill((0, 0, 0)) # setting the color of the screen --> RGB, always first in while loop
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():  # loop through all the events in the game
        if event.type == pygame.QUIT:  # When the cloe button is pressed, program closes
            running = False
        # if keystroke is pressed check if its left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is 'ready':
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX # so that the bullet won't follow the spaceship's direction when it moves
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Checking of boundaries
    # Player movement
    playerX += playerX_change
    if playerX < 0:  # To prevent our spaceship from going beyond the screen
        playerX = 0
    elif playerX >= 736:  # To prevent our spaceship from going beyond the screen
        playerX = 736  # We are taking into account the width of our spaceship

    # Enemy movement
    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i]> 440: # when one of the enemies reaches the spaceship, game over
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3 # if the enemy hits the boundary, go back onto the main screen
            enemyY[i] += enemyY_change[i] # if the enemy hits the screen, move it upwards / closer to the player
        elif enemyX[i] >= 736:
            enemyX_change[i] = -3 # if the enemy hits the boundary, go back onto the main screen
            enemyY[i] += enemyY_change[i] # if the enemy hits the screen, move it upwards / closer to the player

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            # After collision, enemy will restart at a random position
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0: # 'Reload the bullet after first shot'
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change # so that the bullet will move upwards

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()  # Updating the screen