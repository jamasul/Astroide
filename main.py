import pygame
import random
import numpy
import math
import time

class AstroideGame:
    def __init__(self):

        # initialize pygame
        pygame.init()

        # create the screen
        self.screen = pygame.display.set_mode((800, 600))
        self.score = 0
        self.life = 3
        self.gameOver = False
        self.font = pygame.font.Font(None, 36)
        self.FIRE = False
        self.weaponSpeed = 0.5
        self.firstY = 1.5
        self.myfont = pygame.font.SysFont("monospace", 16)
        self.WHITE = (255,255,255)
        # Caption and icon
        pygame.display.set_caption("Spaceship")
        self.icon = pygame.image.load('Images\\game_icons\\spaceship.png')
        pygame.display.set_icon(self.icon)

        # Player
        self.playerImg = pygame.image.load('Images\\game_icons\\spaceship.png')
        self.projectileImg = pygame.image.load('Images\\game_icons\\projectile.png')
        self.playerPosX = 380
        self.playerPosY = 260

        self.projectileX = self.playerPosX
        self.projectileY = self.playerPosY + 0.5 # shooted from front of ship
        self.shootSound = pygame.mixer.Sound('Sound\\shoot.wav')
        self.enemyKilledSound = pygame.mixer.Sound('Sound\\explosion.wav')
        self.themeSong = pygame.mixer.Sound('Sound\\spaceinvaders.mpeg')
        self.bonusSound = pygame.mixer.Sound('Sound\\bonus.wav')

        self.projectileY_changed = 0
        self.playerX_changed = 0
        self.playerY_changed = 0
        self.speed = 0.4

        # Enemy & Fruits/atroide/diamonds
        self.enemyImg = pygame.image.load('Images\\game_icons\\invader.png')
        self.enemy2Img = pygame.image.load('Images\\game_icons\\invader.png')

        self.fruitImg = pygame.image.load('Images\\game_icons\\diamond.png')
        self.fruit2Img = pygame.image.load('Images\\game_icons\\astroide.png')


        self.enemyPositions = []
        self.fruitPositions = []
        self.numFruits = 10

    def initialize(self):
        for i in range(self.numFruits):
            numbersX = list(range(0, 360)) + list(range(390, 800))
            enemyX = random.choice(numbersX)
            numbersY = list(range(0, 240)) + list(range(280, 600))
            enemyY = random.choice(numbersY)
            self.enemyPositions.append((enemyX, enemyY))

        # Fruits
        for i in range(10):
            fruitX = random.randint(0, 800)
            fruitY = random.randint(0, 600)
            self.fruitPositions.append((fruitX, fruitY))
        pygame.mixer.Sound.stop(self.themeSong)
        pygame.mixer.Sound.play(self.themeSong)

    def reset(self):
        self.player(self.playerPosX, self.playerPosY)
        global score, life, enemyPositions, fruitPositions

        self.life = 3
        self.enemyPositions = []
        self.fruitPositions = []
        self.initialize()

    def player(self, x, y):
        self.screen.blit(self.playerImg, (x, y))

    def enemies(self, pos):
        global enemyPositions
        for i in range(0, len(pos)):
            #if i <= 5:
            x = pos[i][0]
            y = pos[i][1]

            if x >= 750:
                while x > 100:
                    x-=1.4
                    self.screen.blit(self.enemyImg, (x, y))
            else:
                x += 0.1

            self.enemyPositions[i] = (x,y)
            self.screen.blit(self.enemyImg, (x, y))

        if len(self.enemyPositions) == 0:
            self.reset()


    def fruits(self, pos):
        for i in range(len(pos)):
            if i <= 5:
                self.screen.blit(self.fruitImg, (pos[i][0], pos[i][1]))
            else:
                self.screen.blit(self.fruit2Img, (pos[i][0], pos[i][1]))


    def currentPos(self):

        return (round(self.playerPosX), round(self.playerPosY))

    def projectilePos(self):

        return (round(self.projectileX), round(self.projectileY))


    def checkEnemyCollision(self):
        # check enemy collision
        global life, speed, gameOver
        for x in self.enemyPositions:

            distance = math.sqrt(math.pow(numpy.subtract(self.currentPos()[0], x[0]), 2) + math.pow(
                numpy.subtract(self.currentPos()[1], x[1]), 2))

            if distance < 30:
                time.sleep(0.5)
                self.life -= 1
                self.speed = 0.3
            if self.life == 0:
                self.score = 0
                self.gameOver = True

                print("game over!")
                pygame.mixer.Sound.play(self.enemyKilledSound)
                self.reset()


    def checkFruitCollision(self):
        global score, life
        global fruitPositions, playerX_changed, playerY_changed, speed

        for x in self.fruitPositions:
            distance = math.sqrt(math.pow(numpy.subtract(self.currentPos()[0], x[0]), 2) + math.pow(
                numpy.subtract(self.currentPos()[1], x[1]), 2))


            if distance < 30:
                pygame.mixer.Sound.play(self.bonusSound)
                self.fruitPositions.remove((x[0], x[1]))
                self.score += 1
                self.speed += 0.01
                if (len(self.fruitPositions) <= 5 or len(self.fruitPositions) == 0):
                    self.life +=1
                if self.score == self.numFruits:
                    self.reset()

    def fireWeapon(self, x, y):

        global FIRE, weaponSpeed, firstY, projectileX, projectileY
        self.firstY = 1.0

        if self.firstY == 1.0:
            self.firstY = y + self.weaponSpeed

        else:
            self.firstY = 0
        self.weaponSpeed += 3.0

        if self.firstY >= 600.0:
            self.FIRE = False
            self.weaponSpeed = 0.5
            self.firstY = 1.5
        if self.FIRE:
            self.screen.blit(self.projectileImg, (x, self.firstY))
        self.projectileX = x
        self.projectileY = self.firstY

    def projectileEnemyCollide(self):
        for x in self.enemyPositions:
            distance = math.sqrt(math.pow(numpy.subtract(self.projectilePos()[0], x[0]), 2) + math.pow(
                numpy.subtract(self.projectilePos()[1], x[1]), 2))

            if distance < 30:
                pygame.mixer.Sound.play(self.enemyKilledSound)
                time.sleep(0.2)
                self.enemyPositions.remove((x[0], x[1]))

    # Game loop
    def saveGameScore(self):
        pass


    def gameEnd(self):
        global gameOver, running
        if self.gameOver:
            text = self.font.render("Game Over", True, self.WHITE)
            text_rect = text.get_rect()
            text_x = self.screen.get_width() / 2 - text_rect.width / 2
            text_y = self.screen.get_height() / 2 - text_rect.height / 2
            self.screen.blit(text, [text_x, text_y])


    def gameLoop(self):
        running = True
        self.reset()
        while running:
            self.screen.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pygame.mixer.music.stop()
                        pygame.mixer.Sound.play(self.shootSound)
                        self.FIRE = True
                        self.fireWeapon(self.playerPosX, self.playerPosY)

                # check keystroke right or left
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.playerY_changed = 0
                        self.playerX_changed = -self.speed #-0.3

                    if event.key == pygame.K_RIGHT:
                        self.playerY_changed = 0
                        self.playerX_changed = self.speed #0.3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.playerX_changed = -self.speed #-0.3
                    if event.key == pygame.K_RIGHT:
                        self.playerX_changed = self.speed #0.3

                # check keystroke up or down
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.playerX_changed = 0
                        self.playerY_changed = -self.speed #-0.3
                    if event.key == pygame.K_DOWN:
                        self.playerX_changed = 0
                        self.playerY_changed = self.speed #0.3
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.playerX_changed = 0
                        self.playerY_changed = -self.speed #-0.3

                    if event.key == pygame.K_DOWN:
                        self.playerX_changed = 0
                        self.playerY_changed = self.speed #0.3


            self.scoretext = self.myfont.render("Score {0}".format(self.score), 1, (255, 255, 255))
            self.lifetext = self.myfont.render("Life {0}".format(self.life), 1, (255, 255, 255))
            self.screen.blit(self.scoretext, (5, 10))

            self.screen.blit(self.lifetext, (5, 30))
            self.playerPosX += self.playerX_changed
            self.playerPosY += self.playerY_changed

            if self.playerPosX <= 0:
                self.playerPosX = 768
            elif self.playerPosX >= 768:
                self.playerPosX = 0

            if self.playerPosY <= 0:
                self.playerPosY = 568
            elif self.playerPosY >= 568:
                self.playerPosY = 0

            self.player(self.playerPosX, self.playerPosY)
            if self.FIRE:
                self.fireWeapon(self.playerPosX, self.playerPosY)
            self.enemies(self.enemyPositions)
            self.fruits(self.fruitPositions)
            self.checkEnemyCollision()
            self.checkFruitCollision()
            self.projectileEnemyCollide()
            self.gameEnd()
            pygame.display.update()

if __name__=="__main__":
    ast = AstroideGame()
    ast.gameLoop()