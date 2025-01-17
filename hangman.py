import pygame
import random

width, height = 1100, 700
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 70, 70)
green = (50, 205, 50)
gray = (211, 211, 211)
heartColor = (255, 0, 0)
fps = 60
radius = 30
gap = 20
startX = (width - (radius * 2 + gap) * 13) // 2
startY = 450

pygame.init()
letterFont = pygame.font.SysFont('comicsans', 40)
wordFont = pygame.font.SysFont('comicsans', 60)
titleFont = pygame.font.SysFont('comicsans', 100)

background = pygame.image.load('background.jpg')
background = pygame.transform.scale(background, (width, height))
hintIcon = pygame.image.load('hint.png')  
hintIcon = pygame.transform.scale(hintIcon, (50, 50))

def loadWords(filename):
    try:
        with open(filename, 'r') as file:
            words = []
            for line in file:
                parts = line.strip().split(",")
                if len(parts) == 2 and parts[0].isalpha() and all('A' <= char <= 'Z' for char in parts[0].upper()):
                    words.append((parts[0].upper(), parts[1]))
                elif len(parts) == 1 and parts[0].isalpha():
                    words.append((parts[0].upper(), None)) 
        if not words:
            raise ValueError("Words file is empty or contains invalid entries.")
        return words
    except (FileNotFoundError, ValueError) as e:
        print(e)
        pygame.quit()
        exit()

def generateLetters(startX, startY, radius, gap):
    letters = []
    for i in range(26):
        x = startX + gap * 2 + ((radius * 2 + gap) * (i % 13))
        y = startY + ((i // 13) * (gap + radius * 2))
        letters.append([x, y, chr(65 + i), True])
    return letters

def isMouseOverCircle(mouseX, mouseY, x, y, radius):
    return (x - mouseX) ** 2 + (y - mouseY) ** 2 < radius ** 2

def drawHearts(screen, hearts, hangmanStatus):
    for i in range(hearts):
        color = heartColor if i >= hangmanStatus else white
        pygame.draw.circle(screen, color, (50 + i * 50, 50), 20)

def drawLetters(screen, letters):
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen, gray, (x, y), radius)
            pygame.draw.circle(screen, black, (x, y), radius, 2)
            letterText = letterFont.render(ltr, 1, black)
            screen.blit(letterText, (x - letterText.get_width() / 2, y - letterText.get_height() / 2))

def drawWord(screen, word, guessed):
    displayWord = "".join([letter + " " if letter in guessed else "_ " for letter in word])
    wordText = wordFont.render(displayWord, 1, black)
    screen.blit(wordText, (width / 2 - wordText.get_width() / 2, 250))

def displayMessage(screen, message, color):
    pygame.time.delay(500)
    screen.fill(white)
    screen.blit(background, (0, 0))
    messageText = wordFont.render(message, 1, color)
    screen.blit(messageText, (width / 2 - messageText.get_width() / 2, height / 2 - messageText.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(2000)

def drawHint(screen, hint):
    hintText = letterFont.render(f"Hint: {hint}", 1, red)
    screen.blit(hintText, (width / 2 - hintText.get_width() / 2, height - 100))

def drawHintIcon(screen, x, y):
    screen.blit(hintIcon, (x, y))

def playGame():
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Hangman Game")
    hearts = 6
    hangmanStatus = 0
    guessed = []
    hintUsed = False

    words = loadWords("words.txt")
    word, hint = random.choice(words)
    letters = generateLetters(startX, startY, radius, gap)
    clock = pygame.time.Clock()
    run = True

    hintX, hintY = width - 100, height - 100 

    while run:
        clock.tick(fps)
        screen.fill(white)
        screen.blit(background, (0, 0))
        drawWord(screen, word, guessed)
        drawLetters(screen, letters)
        drawHearts(screen, hearts, hangmanStatus)
        if hint and not hintUsed:  
            drawHintIcon(screen, hintX, hintY)
        if hintUsed and hint:
            drawHint(screen, hint)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible and isMouseOverCircle(mouseX, mouseY, x, y, radius):
                        letter[3] = False
                        guessed.append(ltr)
                        if ltr not in word:
                            hangmanStatus += 1
                if hint and not hintUsed and hintX <= mouseX <= hintX + 50 and hintY <= mouseY <= hintY + 50:
                    hintUsed = True

        won = all([letter in guessed for letter in word])
        if won:
            displayMessage(screen, "YOU WON!", green)
            break
        if hangmanStatus == hearts:
            displayMessage(screen, f"YOU LOST!", red)
            displayMessage(screen, f"WORD: {word}", red)
            break

    pygame.quit()

if __name__ == "__main__":
    playGame()
