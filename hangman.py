import pygame
import random

pygame.init()

width, height = 1100, 700
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game")

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 70, 70)
green = (50, 205, 50)
blue = (70, 130, 255)
lightBlue = (173, 216, 230)
gray = (211, 211, 211)
heartColor = (255, 0, 0)

letterFont = pygame.font.SysFont('comicsans', 40)
wordFont = pygame.font.SysFont('comicsans', 60)
titleFont = pygame.font.SysFont('comicsans', 100)

hearts = 6
radius = 30
gap = 20
letters = []
startX = round((width - (radius * 2 + gap) * 13) / 2)
startY = 450

background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (width, height))

def loadWords(filename):
    with open(filename, 'r') as file:
        return [line.strip().upper() for line in file]

words = loadWords("words.txt")
word = random.choice(words)
guessed = []

a = 65
for i in range(26):
    x = startX + gap * 2 + ((radius * 2 + gap) * (i % 13))
    y = startY + ((i // 13) * (gap + radius * 2))
    letters.append([x, y, chr(a + i), True])

def draw():
    screen.fill(white)
    screen.blit(background, (0, 0))
    displayWord = "".join([letter + " " if letter in guessed else "_ " for letter in word])
    wordText = wordFont.render(displayWord, 1, black)
    screen.blit(wordText, (width / 2 - wordText.get_width() / 2, 250))

    for i in range(hearts):
        color = heartColor if i >= hangmanStatus else white
        pygame.draw.circle(screen, color, (50 + i * 50, 50), 20)

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen, gray, (x, y), radius)
            pygame.draw.circle(screen, black, (x, y), radius, 2)
            letterText = letterFont.render(ltr, 1, black)
            screen.blit(letterText, (x - letterText.get_width() / 2, y - letterText.get_height() / 2))
        mouseX, mouseY = pygame.mouse.get_pos()
        if visible and (x - mouseX) ** 2 + (y - mouseY) ** 2 < radius ** 2:
            pygame.draw.circle(screen, (180, 180, 255), (x, y), radius)

    pygame.display.update()

def displayMessage(message, color):
    pygame.time.delay(500)
    screen.fill(white)
    screen.blit(background, (0, 0))
    messageText = wordFont.render(message, 1, color)
    screen.blit(messageText, (width / 2 - messageText.get_width() / 2, height / 2 - messageText.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(500)

clock = pygame.time.Clock()
fps = 60
hangmanStatus = 0
run = True

while run:
    clock.tick(fps)
    draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                if visible and (x - mouseX) ** 2 + (y - mouseY) ** 2 < radius ** 2:
                    letter[3] = False
                    guessed.append(ltr)
                    if ltr not in word:
                        hangmanStatus += 1

    won = all([letter in guessed for letter in word])
    if won:
        displayMessage("YOU WON!", green)
        break
    if hangmanStatus == hearts:
        displayMessage(f"YOU LOST!", red)
        displayMessage(f"WORD: {word}", red)
        pygame.time.delay(300)
        break

pygame.quit()
