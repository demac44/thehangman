import pygame
import math
import random


pygame.init()

# SCREEN

WIDTH, HEIGHT = 1200, 600

win = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("TheHangman")

icon = pygame.image.load('assets/images/icon.ico')
pygame.display.set_icon(icon)

#IMAGES 

images = []

for i in range(7):
    image = pygame.image.load("assets/images/hangman"+ str(i)+ ".png")
    images.append(image)


hangman_status = 0

word = "HANGMAN"

def random_word(filename, k):
    sample = []
    with open(filename, 'rt') as f:
        linecount = sum(1 for line in f)
        f.seek(0)
        
        random_linenos = sorted(random.sample(range(linecount), k), reverse = True)
        lineno = random_linenos.pop()
        for n, line in enumerate(f):
            if n == lineno:
                sample.append(line.rstrip())
                if len(random_linenos) > 0:
                    lineno = random_linenos.pop()
                else:
                    break
    return sample



#COLORS

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (47,47,47)
GREEN = (45, 249, 4)
RED = (236, 37, 37)

# FONTS

LETTER_FONT = pygame.font.SysFont('mspgothic', 30)
WORD_FONT = pygame.font.SysFont('mspgothic', 60)
END_BTN_FONT = pygame.font.SysFont('mspgothic', 50)
SMALL_FONT = pygame.font.SysFont("mspgothic", 16)

# LETTER BUTTONS

RADIUS = 30
GAP = 20

letters = []
guessed = []

def draw_letters():
    
    startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
    starty = 450
    A = 65

    for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A+i), True])


draw_letters()

# START SCREEN

START_BTN_W = 400
START_BTN_H = 100


def draw_start_screen():

    made_by = SMALL_FONT.render("Made by Demir Umejr", 1, WHITE)
    win.blit(made_by, (WIDTH - made_by.get_width()- 20, HEIGHT-made_by.get_height()-10 ))

    img = pygame.image.load('assets/images/logo.png')

    win.blit(img, (WIDTH/2 - img.get_width()/2, 100))

    pygame.draw.rect(win, GRAY, (WIDTH / 2 - (START_BTN_W / 2), HEIGHT / 2 + START_BTN_H, START_BTN_W, START_BTN_H))


    start_btn_text = END_BTN_FONT.render("START", 1, WHITE)        
    start_btn_text2 = END_BTN_FONT.render("START", 1, BLACK)        
    win.blit(start_btn_text2, (WIDTH / 2 - (start_btn_text2.get_width() / 2) + 5, HEIGHT / 2 + START_BTN_H + start_btn_text2.get_height()/2 + 5))
    win.blit(start_btn_text, (WIDTH / 2 - (start_btn_text.get_width() / 2), HEIGHT / 2 + START_BTN_H + start_btn_text.get_height()/2))

    pygame.display.update()


# END SCREEN

streak = 0


END_GAME_BTN_W = WIDTH / 4
END_GAME_BTN_H = HEIGHT / 5


def draw_end_screen(won):
    global streak

    if won:
        end_text = WORD_FONT.render("CORRECT!", 1, WHITE) 
        tick_or_x_img = pygame.image.load("assets/images/tick.png")
    else: 
        end_text = WORD_FONT.render("WRONG!", 1, WHITE) 
        tick_or_x_img = pygame.image.load("assets/images/x.png")
        
    win.blit(tick_or_x_img, (WIDTH / 2 - 150, HEIGHT / 4-20))
               
    win.blit(end_text, (WIDTH / 2 - (end_text.get_width() / 2) + 40, HEIGHT / 4))


    show_word = LETTER_FONT.render("The word was "+word, 1, WHITE)
    win.blit(show_word, (WIDTH / 2 - (show_word.get_width() / 2), HEIGHT / 4+100))

    show_streak = LETTER_FONT.render("STREAK "+str(streak), 1, WHITE)
    win.blit(show_streak, (65, 25))

    streak_img = pygame.image.load('assets/images/flame.png')
    win.blit(streak_img, (20, 15))


    #new game
    pygame.draw.rect(win, WHITE, rect=((WIDTH / 2) / 4, HEIGHT - END_GAME_BTN_H - 100, END_GAME_BTN_W, END_GAME_BTN_H), border_radius=20)
    pygame.draw.rect(win, GRAY, rect=((WIDTH / 2) / 4 + 5, HEIGHT - END_GAME_BTN_H - 100 + 5, END_GAME_BTN_W - 10, END_GAME_BTN_H - 10), border_radius=20)
    
    #quit game
    pygame.draw.rect(win, WHITE, rect=(WIDTH/2 + ((WIDTH / 2) / 4), HEIGHT - END_GAME_BTN_H - 100, END_GAME_BTN_W, END_GAME_BTN_H), border_radius=20)
    pygame.draw.rect(win, GRAY, rect=(WIDTH/2 + ((WIDTH / 2) / 4) + 5, HEIGHT - END_GAME_BTN_H - 100 + 5, END_GAME_BTN_W - 10, END_GAME_BTN_H - 10), border_radius=20)

    if won:
        reset_game_text = END_BTN_FONT.render("CONTINUE", 1, WHITE)    
    else:
        reset_game_text = END_BTN_FONT.render("NEW GAME", 1, WHITE)        

    win.blit(reset_game_text, ((WIDTH / 2) / 4 + reset_game_text.get_width()/4, HEIGHT - 100 - END_GAME_BTN_H/2 - reset_game_text.get_height()/2))
    
    quit_game_text = END_BTN_FONT.render("QUIT", 1, WHITE)        
    win.blit(quit_game_text, (WIDTH/2 + (WIDTH / 2) / 4 + quit_game_text.get_width(), HEIGHT - 100 - END_GAME_BTN_H/2 - reset_game_text.get_height()/2))


    pygame.display.update()


def reset_game():
    global started
    global game_ended
    global hangman_status
    global guessed
    global letters
    global word


    started = True
    game_ended = False
    hangman_status = 0
    guessed = []
    letters = []
    word = random_word("assets/words.txt", 1)[0].upper()
    draw()
    draw_letters()
    pygame.display.update()


def hint_letter():
    for ltr in word:
        if ltr not in guessed:
            for l in letters:
                if ltr == l[2]:
                    l[3] = False
            return ltr
    return False



# GAME SCREEN

GUESSED_LTRS_GAP = 30

def draw():
    # draw word

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    

    text = WORD_FONT.render(display_word, 1, WHITE)
    win.blit(text, (400, 200))

    h = LETTER_FONT.render("HINT", 1, WHITE)
    win.blit(h, (WIDTH-h.get_width()-20, 20))

    # SHOW GUESSED LETTERS
    for i in range(len(guessed)):
        if guessed[i] in word:
            g = LETTER_FONT.render(guessed[i], 1, GREEN)
        else:
            g = LETTER_FONT.render(guessed[i], 1, RED)
        win.blit(g, (i*GUESSED_LTRS_GAP+10, 15))


    # draw circles for letters
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, WHITE, (x,y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, WHITE)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
        
    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


# GAME LOOP

started = False
game_ended = False

FPS = 60

clock = pygame.time.Clock()

run = True


while run:
    clock.tick(FPS)

    win.fill(GRAY)


    if started and not game_ended:
        draw()
    elif not started and not game_ended:
        draw_start_screen()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:

            m_x, m_y = pygame.mouse.get_pos()
            
            if started and not game_ended:
                # hint letter
                if m_x >=WIDTH-100 and m_y <= 50:
                    hint_ltr = hint_letter()
                    guessed.append(hint_ltr)

            
                
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
                

            elif not started and not game_ended:
                # start button
                if m_x >= WIDTH / 2 - (START_BTN_W / 2) and m_x <= (WIDTH / 2 - (START_BTN_W / 2)) + START_BTN_W and m_y >= HEIGHT / 2 + START_BTN_H and m_y <= HEIGHT / 2 + START_BTN_H*2:
                    word = random_word("assets/words.txt", 1)[0].upper()
                    started = True
                    draw()
            
            elif started and game_ended:
                # continue button
                if m_x >= (WIDTH / 2) / 4 and m_x <= (WIDTH / 2) / 4*3 and m_y >= HEIGHT - END_GAME_BTN_H - 100 and m_y <= HEIGHT-100:
                    reset_game()
                # quit button
                elif m_x >= WIDTH/2 + ((WIDTH / 2) / 4) and m_x <= WIDTH/2 + ((WIDTH / 2) / 4)*3 and m_y >= HEIGHT - END_GAME_BTN_H - 100 and m_y <= HEIGHT-100:
                    run = False

    
    won = True
    for letter in word:
        if letter not in guessed:
            won = False
            break
    


    
    if won:
        if not game_ended:
            streak+=1
        game_ended = True
        draw_end_screen(won)

    if hangman_status == 6:
        streak = 0
        game_ended = True
        draw_end_screen(won = False)




pygame.quit()

