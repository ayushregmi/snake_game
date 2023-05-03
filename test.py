import pygame
import random
import pandas as pd
from queue import PriorityQueue

SCREEN_DIMENSIONS = (800, 800)
FPS = 30
BACKGROUND_COLOR = (81, 81, 81)

SNAKE_SIZE = FOOD_SIZE = BOX_SIZE = 10
SNAKE_COLOR = (0, 255, 0)

FOOD_COLOR = (255, 0, 0)

NUMBER_OF_BOXES = int(SCREEN_DIMENSIONS[0] / BOX_SIZE)

class Player():
    def __init__(self, startPosition):
        self.size = 1
        self.head_position = startPosition
        self.direction = 0
        self.body = [BodyPart(startPosition)]
        self.speed = 1
    
    def move(self):
        
        if self.direction == 1:

            self.head_position = (self.head_position[0] - 1*self.speed, self.head_position[1])
            previousPosition = self.head_position

            for body in self.body:
                temp = body.position
                body.changePosition(previousPosition)
                previousPosition = temp
            
        if self.direction == 2:

            self.head_position = (self.head_position[0], self.head_position[1]-1*self.speed)
            previousPosition = self.head_position

            for body in self.body:
                temp = body.position
                body.changePosition(previousPosition)
                previousPosition = temp
            
        if self.direction == 3:

            self.head_position = (self.head_position[0]  +1*self.speed, self.head_position[1])
            previousPosition = self.head_position

            for body in self.body:
                temp = body.position
                body.changePosition(previousPosition)
                previousPosition = temp
            
        if self.direction == 4:

            self.head_position = (self.head_position[0], self.head_position[1]+1*self.speed)
            previousPosition = self.head_position

            for body in self.body:
                temp = body.position
                body.changePosition(previousPosition)
                previousPosition = temp
            
        pass
    
    def drawPlayer(self, screen):
        for body in self.body:
            body.draw(screen)
    
    def __eq__(self, food):
        if self.head_position == food.position:
            return True
        return False
    
    def addBodyPart(self):
        self.size += 1
        self.body.append(BodyPart(position=None))
    
    def checkCollision(self):
        
        collision = True
        
        if not (self.body[0] in self.body[3:]):
            collision = False
        
        if collision:
            self.direction = 0
            print("self colllision")
            return True
        
        if self.head_position[0] >= 0 and self.head_position[0] < NUMBER_OF_BOXES and self.head_position[1] >= 0 and self.head_position[1] < NUMBER_OF_BOXES:
            return False
        print("border collision")
        self.direction = 0
        return True
        
    

class BodyPart():
    def __init__(self, position: tuple):
        self.position = position
    
    def draw(self, screen):
        if self.position is None:
            return
        pygame.draw.rect(screen, BACKGROUND_COLOR, (self.position[0] * BOX_SIZE, self.position[1] * BOX_SIZE, SNAKE_SIZE, SNAKE_SIZE))
        pygame.draw.rect(screen, SNAKE_COLOR, (self.position[0] * BOX_SIZE + 2, self.position[1] * BOX_SIZE + 2, SNAKE_SIZE-2, SNAKE_SIZE-2))
    
    def changePosition(self, position):
        self.position = position
        
    def __eq__(self, value):
        
        if self.position == value.position:
            return 1
        return 0
    

class Food():
    
    def __init__(self):
        self.position = None
        pass
    
    def changePosition(self, position):
        self.position = position
        
    def drawFood(self, screen):
        if self.position is not None:
            pygame.draw.rect(screen, FOOD_COLOR, (self.position[0] * BOX_SIZE, self.position[1] * BOX_SIZE, FOOD_SIZE, FOOD_SIZE))
        
class Game():
    
    def path_to_food(self):
        pass
    
    def __init__(self, screenDimensions):
        self.screenDimensions = screenDimensions
        self.reset_game()
        self.screen = pygame.display.set_mode(self.screenDimensions)
        pygame.display.set_caption("Snake Game")
        self.background = (0, 0, 0)
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        self.enableKeyboard = True
        return
    
    def reset_game(self):
        self.player = Player((NUMBER_OF_BOXES/2,NUMBER_OF_BOXES/2))
        
        foodPosition = (random.randrange(0, NUMBER_OF_BOXES), random.randrange(0, NUMBER_OF_BOXES))
        self.food = Food()
        self.food.changePosition(foodPosition)  
        self.gameover = False  
        self.enableKeyboard = True
    
        while self.food in self.player.body: 
            foodPosition = (random.randrange(0, NUMBER_OF_BOXES), random.randrange(0, NUMBER_OF_BOXES))
            self.food.changePosition(foodPosition)



        self.score = 0
        
    def handleKeyboardInput(self):
        if self.enableKeyboard:
            prevDirection = self.player.direction
            keypressed = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                
                
                if event.type == pygame.KEYDOWN:
                    if self.gameover and event.key == pygame.K_r:
                        self.reset_game()
                    self.enableKeyboard = False
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.player.direction != 3:
                        self.player.direction = 1
                        keypressed = 1
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.player.direction != 1:
                        self.player.direction = 3
                        keypressed = 3
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.player.direction != 2:
                        self.player.direction = 4
                        keypressed = 4
                    elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.player.direction != 4:
                        self.player.direction = 2
                        keypressed = 2
                    
                # if self.player.direction > 0:
                #     self.generateTrainingData(prevDirection)
                    
                # if keypressed > 0:
                #     return
                        

            
    
    def eatFood(self):
        self.score += 1
            
        self.player.addBodyPart()
            
        foodPosition = (random.randrange(0, NUMBER_OF_BOXES), random.randrange(0, NUMBER_OF_BOXES))
        while self.food in self.player.body: 
            foodPosition = (random.randrange(0, NUMBER_OF_BOXES), random.randrange(0, NUMBER_OF_BOXES))
            self.food.changePosition(foodPosition)
    
    def updateScreen(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.player.drawPlayer(self.screen)
        self.food.drawFood(self.screen)
        pygame.display.update()
        self.enableKeyboard = True
    
    def generateTrainingData(self, prevDirection):
        
        df = pd.DataFrame(data=[self.player.head_position[0], self.player.head_position[1], self.player.size, self.food.position[0], self.food.position[1], prevDirection, self.player.direction], index=self.dataframe.columns).T
        self.dataframe = pd.concat([self.dataframe,df])
        print(f"{self.player.head_position}, {self.player.size}, {self.food.position}, {prevDirection}, {self.player.direction}")
    
    def start_game(self):
        self.run = True
        
        # try:
        #     self.dataframe = pd.read_csv("data.csv")["player_x", "player_y", "player_size", "food_position_x", "food_position_y", "previous_direction", "new_direction"]
        # except:
        #     self.dataframe = pd.DataFrame(columns=["player_x", "player_y", "player_size", "food_position_x", "food_position_y", "previous_direction", "new_direction"])
        while self.run:
            self.handleKeyboardInput()
            
            self.player.move()
            
            
            self.gameover = self.player.checkCollision()
            if self.gameover:
                # self.dataframe.to_csv("data.csv")
                print(f"final score: {self.score}")
                while self.gameover:
                    self.handleKeyboardInput()
                    pass
            
            if self.food == self.player.body[0]:
                self.eatFood()
            
            self.updateScreen()
            
            self.fpsClock.tick(FPS)
            
        
        
game = Game(SCREEN_DIMENSIONS)

game.start_game()

    