import random
import pygame
from pygame import mixer
import math
#initialization of pygame
pygame.init()
#creating game window
screen=pygame.display.set_mode((800,600))
#background
background=pygame.image.load('background.jpg')
#background music
mixer.music.load('game_music.mp3')
mixer.music.play(-1)

#title and icon
pygame.display.set_caption("Space Invaders")
icon=pygame.image.load('startup.png')
pygame.display.set_icon(icon)

#player

playerimg=pygame.image.load('001-space-invaders.png')
playerx=350
playery=480
playerx_change=0
#enemy
enemyimg=[]
enemyx=[]
enemyy=[]
enemyx_change=[]
enemyy_change=[]
num_of_enemies=6
for i in range (num_of_enemies):

    enemyimg.append(pygame.image.load('enemy.png'))
    enemyx.append(random.randint(0,756 ))
    enemyy.append(random.randint(50,150))
    enemyx_change.append(0.3)
    enemyy_change.append(40)
#bullet
#ready=you cant see bullet on screen
#fire=bullet is moving
bulletimg=pygame.image.load('bullet.png')
bulletx=0
bullety=480
bulletx_change=0
bullety_change=2
bullet_state="ready"
#score=0
score_value=0
font=pygame.font.Font('freesansbold.ttf',32)
textx=10
texty=10

over_font=pygame.font.Font('freesansbold.ttf',64)
def show_score(x,y):
    score=font.render("Score:"+str(score_value),True,(255,255,255))
    screen.blit(score, (x, y))
def game_over_text():
    over_text=over_font.render("Game Over",True,(255,255,255))
    screen.blit(over_text,(200,250))
def player(x,y):
    screen.blit(playerimg,(x,y))
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))
def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletimg,(x+16,y+10))
def iscollision(enemyx,enemyy,bulletx,bullety):
    distance=math.sqrt(math.pow(enemyx-bulletx,2)+(math.pow(enemyy-bullety,2)))#finding distance by distance formula
    if distance<27:
        return True
    else:
        return False

#game loop
running=True
while running:
    # red,green,blue
    screen.fill((0, 0, 0))
    #background image
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type==pygame.QUIT:#by pressing cross- loop terminates
            running=False

        #key strokes is pressed check left or right movement of rocket
        if event.type==pygame.KEYDOWN:#press key on keybord

            if event.key==pygame.K_LEFT:#pressing left arrow key
                playerx_change=-0.9
            if event.key==pygame.K_RIGHT:#pressing right arrow key
                playerx_change=0.9
            if event.key==pygame.K_SPACE:#pressing space bar key
                if bullet_state is "ready":
                    bullet_sound=mixer.Sound('bullet_fire.mp3')
                    bullet_sound.play()
                    bulletx=playerx
                    fire_bullet(bulletx,bullety)
        if event.type==pygame.KEYUP:#releasing pressed key
            if event.key == pygame.K_LEFT or event.key==pygame.K_RIGHT:
                playerx_change=0#after releasing left or right arrow key movement will stop of spaceship
            #checking boundries of spaceship
    playerx +=playerx_change
    if playerx<=0:
        playerx=0
    elif playerx>=736:#800-64 ;64 is size of rocket
        playerx=736
    #enemy movement
    for i in range(num_of_enemies):
#game over
        if enemyy[i] > 440:
            for j in range(num_of_enemies):
                enemyy[j] = 20000
            game_over_text()
            pygame.mixer.music.stop()
            game_over_music = mixer.Sound('game_over.mp3')
            game_over_music.play(4)

            break
            pygame.mixer.music.stop()
        enemyx[i] += enemyx_change[i]


        if  enemyx[i] <= 0:
            enemyx_change[i]=0.7
            enemyy[i]+=enemyy_change[i]
        elif enemyx[i] >= 736:  # 800-64 ;64 is size of rocket
            enemyx_change[i]=-0.7
            enemyy[i]+=enemyy_change[i]

            # collision
        collision = iscollision(enemyx[i], enemyy[i], bulletx, bullety)
        if collision:
            explosion_bullet_sound = mixer.Sound('bullet_hit.mp3')
            explosion_bullet_sound.play()
            bullety = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyx[i] = random.randint(0, 756)
            enemyy[i] = random.randint(50, 150)
        enemy(enemyx[i],enemyy[i],i)
    #bullet movement
    if bullety<=0:
        bullety=480
        bullet_state="ready"


    if bullet_state is "fire":
        fire_bullet(bulletx,bullety)
        bullety-=bullety_change

    player(playerx,playery)
    show_score(textx,texty)
    pygame.display.update()