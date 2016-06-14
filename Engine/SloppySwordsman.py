import pygame
import os
import pickle

#Initializing/Setup

pygame.init()
pygame.mixer.init()
display_width = 800
display_height = 600
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Hail Post ALPHA v1.0')
clock = pygame.time.Clock()

#Colors#

black = (0,0,0)
white = (255,255,255)
red = (222,41,16)
green = (0,255,0)
gold = (255, 222, 0)
UI =(149, 165, 166)
emerald =(39, 174, 96)
pomegranate =(192, 57, 43)
pom =(231, 76, 60)
em =(46, 204, 113)

#Images

char_width = 40
char_height = 54
lobbybackground = pygame.image.load(os.path.join("data", 'lobbybackground.png')).convert()
metal_inactive_texture = pygame.image.load(os.path.join("data", 'metal.png')).convert()
metal_active_texture = pygame.image.load(os.path.join("data", 'metal_dark.png')).convert()
still = pygame.image.load(os.path.join("data", 'back1.png')).convert()
pygame.mixer.music.load(os.path.join("data", 'lobby.mp3'))
pygame.mixer.music.play(-1)


# WALKING ANIMATION SHIT #

left_images = []
left_images.append( pygame.image.load(os.path.join("data", 'left1.png') ).convert())
left_images.append( pygame.image.load(os.path.join("data", 'left2.png') ).convert())
left_images.append( pygame.image.load(os.path.join("data", 'left3.png') ).convert())
right_images = []
right_images.append( pygame.image.load(os.path.join("data", 'right1.png') ))
right_images.append( pygame.image.load(os.path.join("data", 'right2.png') ))
right_images.append( pygame.image.load(os.path.join("data", 'right3.png') ))
forward_images = []
forward_images.append( pygame.image.load(os.path.join("data", 'forward1.png') ))
forward_images.append( pygame.image.load(os.path.join("data", 'forward2.png') ))
forward_images.append( pygame.image.load(os.path.join("data", 'forward3.png') ))
back_images = []
back_images.append( pygame.image.load(os.path.join("data",'back1.png') ))
back_images.append( pygame.image.load(os.path.join("data", 'back2.png') ))
back_images.append( pygame.image.load(os.path.join("data", 'back3.png') ))
left_current = 1
right_current = 0
forward_current = 0

back_current = 0
left_walking = True
left_walking_steps = 0
left_current = (left_current + 1) % len(left_images)
left_player = left_images[ left_current ]
right_walking = False
right_walking_steps = 0
right_current = (right_current + 1) % len(right_images)
right_player = right_images[ right_current ]
forward_walking = False
forward_walking_steps = 0
forward_current = (forward_current + 1) % len(forward_images)
forward_player = forward_images[ forward_current ]
back_walking = False
back_walking_steps = 0
back_current = (back_current + 1) % len(back_images)
back_player = back_images[ back_current ]

#MISC INIT STUFF#
rectposfile = {}

### SAVE FILE CREATION AND LOADING ###
try:

    with open('save.pkl','rb') as infile:
        saveread = pickle.load(infile)
    savereadis = True
    with open('player.pkl','rb') as infile:
        playerread = pickle.load(infile)
    with open('rectpos.pkl','rb') as infile:
        playerread = pickle.load(infile)

except:
    print "Creating Savefile...."
    savefile = ['Placeholder']
    playerfile = {"Place":"Holder"}
    rectposfile = {"Place":"Holder"}

    with open('save.pkl','wb') as outfile:
        pickle.dump(savefile,outfile)
    with open('save.pkl','rb') as infile:
        saveread = pickle.load(infile)

    with open('player.pkl','wb') as outfile:
        pickle.dump(playerfile,outfile)
    with open('player.pkl','rb') as infile:
        playerread = pickle.load(infile)

    with open('rectpos.pkl','wb') as outfile:
        pickle.dump(rectposfile,outfile)
    with open('rectpos.pkl','rb') as infile:
        rectposread = pickle.load(infile)
    print "Save Loaded."

    savefile = saveread
    playerfile = playerread
    rectposfile = rectposread

def text_objects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()
def message_display(text,y,font,size,color,x = None):

    largeText=pygame.font.Font(os.path.join("data", font),size)
    TextSurf, TextRect=text_objects(text, largeText, color)
    if x == None:
        TextRect.center=((display_width/2),(y))
    else:
        TextRect.center=((x),(y))
    gameDisplay.blit(TextSurf, TextRect)
def button(msg,b_x,b_y,w,h,inactive_texture,active_texture,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    cropped_inactive = pygame.transform.scale(inactive_texture,(w,h))
    cropped_active = pygame.transform.scale(active_texture,(w,h))
    if b_x+w > mouse[0] > b_x and b_y+h > mouse[1] > b_y:
        gameDisplay.blit(cropped_active,(b_x,b_y))

        if click[0] == 1 and action != None:
                action()
    else:
        gameDisplay.blit(cropped_inactive,(b_x,b_y))

    smallText = pygame.font.Font(os.path.join("data", "freesansbold.ttf"),20)
    textSurf, textRect = text_objects(msg, smallText,black)
    textRect.center = ( (b_x+(w/2)), (b_y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
def saverectpos():
    with open('rectpos.pkl','wb') as outfile:
        pickle.dump(rectposfile,outfile)
    with open('rectpos.pkl','rb') as infile:
        rectposread = pickle.load(infile)
def rect_store(rectname,recttotalx,recttotaly):
            global rectposfile
            rectnamex = rectname + 'x'
            rectnamey = rectname + 'y'
            try:
                rectposfile[rectnamex] = recttotalx
                rectposfile[rectnamey] = recttotaly
            except:
                for key,value in rectposfile.items():
                    rectposfile[rectnamex] = recttotalx
                    rectposfile[rectnamey] = recttotaly

            saverectpos()
def rect_read(rectname):
    with open('rectpos.pkl','rb') as infile:
        rectdict = pickle.load(infile)
        rectoutput = rectdict[rectname]
    return rectoutput
def save():


    with open('save.pkl','wb') as outfile:
        pickle.dump(savefile,outfile)
    print "Saved...."
    with open('save.pkl','rb') as infile:
        saveread = pickle.load(infile)
    print "savefile",savefile
    print "saveread"
    print saveread
def saveplayer():
    print playerfile
    with open('player.pkl','wb') as outfile:
        pickle.dump(playerfile,outfile)


    with open('player.pkl','rb') as infile:
        playerread = pickle.load(infile)
    print playerread
def game_loop():
    backgroundx = 0
    backgroundy = 0
    backgroundx_change = 0

    x = display_width/2 - (char_width/2)
    y = display_height/2 - (char_height/2)
    gameExit = False

    onGround = False
    x_change = 0
    y_change = 0
    timer = 0
    testrecttotalx = 0
    testrecttotaly = 0
    backgroundy_change = 0

    global left_walking
    global left_walking_steps
    global left_current
    global left_player

    global right_walking
    global right_walking_steps
    global right_current
    global right_player

    global forward_walking
    global forward_walking_steps
    global forward_current
    global forward_player

    global back_walking
    global back_walking_steps
    global back_current
    global back_player


    while not gameExit:

        onGround = False
        if y == display_height - char_height:
            onGround = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_0:
                    print "null"
                elif event.key == pygame.K_a:
                    #x_change = -8
                    backgroundx_change = 8
                    left_walking = True
                    left_walking_steps = 5
                if event.key == pygame.K_2:
                    print "null"
                elif event.key == pygame.K_d:
                    #x_change = 8
                    backgroundx_change = -8
                    right_walking = True
                    right_walking_steps = 5

                if event.key == pygame.K_0:
                    print "null"
                elif event.key == pygame.K_w:
                    #x_change = -8
                    backgroundy_change = 8
                    forward_walking = True
                    forward_walking_steps = 5
                if event.key == pygame.K_2:
                    print "null"
                elif event.key == pygame.K_s:
                    #x_change = 8
                    backgroundy_change = -8
                    back_walking = True
                    back_walking_steps = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    #x_change = 0
                    backgroundx_change = 0
                    left_current = 1
                    left_walking = False
                    right_walking = False
                if event.key == pygame.K_s or event.key == pygame.K_w:
                    backgroundy_change = 0
                    forward_walking = False
                    back_walking = False
                if event.key == pygame.K_SPACE:
                    y_change = 0
        if left_walking == True:
            if left_walking_steps > 0:
                left_current = (left_current + 1) % len(left_images)
                left_player = left_images[ left_current ]
                if left_current == 3:
                    left_current 
            else:
                left_walking = False
        if forward_walking == True:
        
            if forward_walking_steps > 0:
                forward_current = (forward_current + 1) % len(forward_images)
                forward_player = forward_images[ forward_current ]
            else:
                forward_walking = False
        if back_walking == True:
            if back_walking_steps > 0:
                back_current = (back_current + 1) % len(back_images)
                back_player = back_images[ back_current ]
                if back_current == 3:
                    back_current
            else:
                back_walking = False
        if right_walking == True:

            if right_walking_steps > 0:
                right_current = (right_current + 1) % len(right_images)
                right_player = right_images[ right_current ]
            else:
                right_walking = False
        left_walking == True
        gameDisplay.fill(black)

        backgroundx += backgroundx_change
        backgroundy += backgroundy_change

        gameDisplay.blit(lobbybackground,(backgroundx,backgroundy))
        if left_walking == True:
            gameDisplay.blit(left_player,(x,y))
        elif right_walking == True:
            gameDisplay.blit(right_player,(x,y))
        elif forward_walking == True:
            gameDisplay.blit(forward_player,(x,y))
        elif back_walking == True:
            gameDisplay.blit(back_player,(x,y))
        else:
            gameDisplay.blit(still,(x,y))


        xand = x + char_width
        careight = char_width/8
        mouse = pygame.mouse.get_pos()
        hitbox = pygame.Rect(x, y, char_width, char_height)
        leftRect = pygame.Rect(x, y, char_width/8 , char_height)
        rightRect = pygame.Rect(xand - careight, y, char_width/8 , char_height)

        pygame.draw.rect(gameDisplay, red,(x, y, careight , char_height))
        pygame.draw.rect(gameDisplay, gold,((xand - careight) - (char_width/8), y, char_width/8 , char_height))
        pygame.draw.rect(gameDisplay, black,(x + careight, y, char_width - careight - careight, char_height/8))
        pygame.draw.rect(gameDisplay, green,(x + careight, (y + char_height) - (char_height/8), char_width - careight - careight, char_height/8))
        button('Test',200,200,200,200,metal_inactive_texture,metal_active_texture)
        # RECTANGLE POSITION STORAGE #


        #testrect = pygame.Rect(245,500, 100, 100)
        testrecttotalx += backgroundx_change
        testrecttotaly += backgroundy_change
        rect_store('testrect',testrecttotalx,testrecttotaly)

        testrect = pygame.draw.rect(gameDisplay, white,(246 + rect_read('testrectx'),1700 + rect_read('testrecty'), 100, 100))
        clock.tick(15)
        pygame.display.update()


game_loop()

