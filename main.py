import pygame
import random
import math

# setup game display
pygame.init()
WIDTH, HEIGHT = 800, 500
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman!!!")

# game buttons
RADIUS = 20
GAP = 15
letters = []
startX = round((WIDTH - (RADIUS*2 + GAP)*13) / 2)
startY = 400
A = 65
for i in range(26):
    x = startX + GAP*2 + (RADIUS*2 + GAP)*(i % 13)
    y = startY + (i // 13)*(GAP + RADIUS*2)
    letters.append([x, y, chr(A + i), True])

# continue buttons
continue_RADIUS = 45
continue_GAP = 30
startX = round((WIDTH - (continue_RADIUS*2 + continue_GAP)*2) / 2)
continue_messages = ["YES", "NO"]
options = []

# letter fonts
sysFont = pygame.font.get_default_font()
LETTER_FONT = pygame.font.SysFont(sysFont, 35)
WORD_FONT = pygame.font.SysFont(sysFont, 50)
TITLE_FONT = pygame.font.SysFont(sysFont, 70)

# load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
hangman_status = 0
words = ["NHAN", "HANDSOME", "FACK", "SHIT"]
word = random.choice(words)
guessed = []

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)


# game processing
def draw():
    window.fill(WHITE)
    # draw title
    text = TITLE_FONT.render("HANGMAN GAME", 1, BLACK)
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, BLACK)
    window.blit(text, (400, 200))

    # draw buttons
    for letter in letters:
        # the coordinate of each button and the character to draw
        x, y, char, visible = letter
        if visible:
            pygame.draw.circle(window, BLACK, (x, y), RADIUS, 3)
            text = LETTER_FONT.render(char, 1, BLACK)
            window.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    # draw hangman
    window.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message, game_status):
    pygame.time.delay(1000)
    window.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    posY = HEIGHT/3 - text.get_height()/2
    window.blit(text, (WIDTH/2 - text.get_width()/2, posY))
    if not game_status:
        text = WORD_FONT.render("The right word is : " + word, 1, RED)
        posY += text.get_height() + 2
        window.blit(text, (WIDTH/2 - text.get_width()/2, posY))

    text = WORD_FONT.render("Do you want to continue?", 1, BLACK)
    posY += text.get_height() + 2
    window.blit(text, (WIDTH / 2 - text.get_width() / 2, posY))
    posY += continue_RADIUS*2 + 2
    for i in range(2):
        x = startX + continue_GAP * 2 + (continue_RADIUS * 2 + continue_GAP) * (i % 2)
        y = posY
        pygame.draw.circle(window, BLACK, (x, int(y)), continue_RADIUS, 4)
        text = WORD_FONT.render(continue_messages[i], 1, BLUE)
        window.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

        options.append([x, y, continue_messages[i]])

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                for option in options:
                    x, y, message = option
                    distance = math.sqrt((x - mouseX)**2 + (y - mouseY)**2)
                    if distance < continue_RADIUS:  # check if click right in the circle
                        if message == "YES":
                            return True
                        else:
                            return False


def reset():
    global hangman_status
    global word
    guessed.clear()
    hangman_status = 0
    word = random.choice(words)
    for letter in letters:
        letter[3] = True


def main():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, char, visible = letter
                    if visible:
                        # if button is still visible check if it is clicked or not
                        distance = math.sqrt((x - mouseX)**2 + (y - mouseY)**2)
                        if distance < RADIUS:  # check if click right in the circle
                            letter[3] = False
                            guessed.append(char)
                            if char not in word:
                                hangman_status += 1

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        if won:
            if display_message("You WON!", True):
                reset()
            else:
                break

        if hangman_status == 6:
            if display_message("You LOST!", False):
                reset()
            else:
                break


main()

pygame.quit()
