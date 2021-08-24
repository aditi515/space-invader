import pygame
import random
import math
from pygame import mixer #for sounds

pygame.init()

#t  methods
width = 1400
height = 1500
screen = pygame.display.set_mode( (width,height), pygame.RESIZABLE) #width, height

pygame.display.set_caption("space invador")
icon = pygame.image.load('project (1).png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('backg.png').convert_alpha()
background = pygame.transform.scale(background, (width,height))

#background sound       .....music- for long audio, sound for short audio
#mixer.music.load("background music.mp3")
#mixer.music.play(-1)  #-1 for loop


# player
player_image = pygame.image.load('space_nani.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (150,150))
playerX = width/2
playerY = height/2
bulletX = 0
playerX_change = 0

def player(x,y):
    screen.blit(player_image,(x,y))
    
# enemy
enemy_image = [ ]
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemy_img = pygame.image.load('alien_nanu2.0.png').convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (100,100))
    enemy_image.append(enemy_img)
    enemyX.append(random.randint(-width/2,width/2)) #width
    enemyY.append(random.randint(-300,150)) #height
    enemyX_change.append(3)
    enemyY_change.append(20)

# bullet
# ready = u cant see on screen   -----  fire = moving
bullet_image = pygame.image.load('flame.png')
bulletX = 0
bulletY = 480 #same as of spaceship y/ height
bulletY_change = 10
bullet_state = "ready"

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

def show_score(x,y):
    score = font.render("Score : " + str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))
    
def enemy(x,y,i):
    screen.blit(enemy_image[i],(x,y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image,(x + 60, y + 60))   #half of image size

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2) )+ (math.pow(enemyY-bulletY,2)))
    if distance < 50:
        return True
    else:
        return False


#game loop
running = True

while running:
    #full screen with a background color
    screen.fill((25,10,100))
    
    screen.blit(background,(0,0))
    
    
    
    for event in pygame.event.get():
        # if crossed from top left quit game
        if event.type == pygame.QUIT:
            running = False
        
        # if keystroke is pressed check if right or left
        if event.type == pygame.KEYDOWN:   #KEYDOWN is pressing of key and KEYUP is realising of key
            if event.key == pygame.K_LEFT:
                playerX_change = - 5
    
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
                
            if event.key == pygame.K_UP:
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound("shooting.wav")
                    bullet_sound.play()
                    #get current x corrdinate
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
            
            
        if event.type == pygame.KEYUP:   #KEYDOWN is pressing of key and KEYUP is realising of key
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0
                
                
    #loacton of player
    playerX += playerX_change
    # checking of boundiers of spaceship
    if playerX <= 0:
        playerX = 0
    elif playerX >= width:
        playerX = width
    player(playerX, playerY)
    
    #bullet movement
    if bulletY <= 0:
        bulletY = 480  #height
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    
    
    
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= width-100:
            enemyX_change[i] = -3
            enemyY[i] += enemyY_change[i]
            
        enemy(enemyX[i], enemyY[i],i)
    
        #collision
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if collision:
            collision_sound = mixer.Sound("collision.wav")
            collision_sound.play()
            bulletY = width/2
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0,width)
            enemyY[i] = random.randint(10,50)

    show_score(textX,textY)

    pygame.display.update()

