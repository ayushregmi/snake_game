import pygame
import random
from queue import PriorityQueue, Queue

SCREEN_DIMENSIONS = (400, 400)
FPS = 30
BACKGROUND_COLOR = (81, 81, 81)

SNAKE_SIZE = FOOD_SIZE = BOX_SIZE = 20
SNAKE_COLOR = (0, 255, 0)

FOOD_COLOR = (255, 0, 0)

NUMBER_OF_BOXES = int(SCREEN_DIMENSIONS[0] / BOX_SIZE)

DIRECTIONS_X = [-1, 0, 1, 0]
DIRECTIONS_Y = [0, -1, 0, 1]


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
        self.body.append(BodyPart(position=self.body[-1].position))
    
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


class Node():
    def __init__(self, i, j):
        self.start_node = False
        self.end_node = False
        self.obstacle = False
        self.i = i
        self.j = j
        self.cost = 0
        self.distanceToEnd = None
        self.path = False
        self.parent = None
    
    def __lt__(self, node):
        return False
    def calculate_distance(self, node):
        return (abs(self.i - node.i) + abs(self.j - node.j))
        # return ((self.i - node.i) ** 2 + (self.j - node.j) ** 2) ** (1/2)
    
    def setParent(self, parent):
        self.parent = parent
    
    def hasParent(self):
        return self.parent
    
    def setPath(self):
        self.path = True
    
    def setCost(self, cost):
        self.cost = cost + 1
    
    def setDistance(self, endNode):
        self.distanceToEnd = self.calculate_distance(endNode)
    
    def setStart(self):
        self.start_node = True
        self.obstacle = False
        self.end_node = False
        
    def setEnd(self):
        self.start_node = False
        self.obstacle = False
        self.end_node = True
    
    def setObstacle(self):
        if not self.start_node and not self.end_node:
            self.obstacle = True
    
    def neighboursIndex(self):
        neighbours = []
        
        for x, y in zip(DIRECTIONS_X, DIRECTIONS_Y):
            temp_i = self.i + x
            temp_j = self.j + y
            
            if not (temp_i >= NUMBER_OF_BOXES or temp_i < 0 or temp_j >= NUMBER_OF_BOXES or temp_j < 0):
                neighbours.append((temp_i, temp_j))
        
        return neighbours

    



class Game():

    
    def __init__(self, screenDimensions):
        self.screenDimensions = screenDimensions
        self.reset_game()
        pygame.font.init()
        self.screen = pygame.display.set_mode(self.screenDimensions)
        pygame.display.set_caption("Snake Game")
        self.background = (0, 0, 0)
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        self.enableKeyboard = True

        return

    def display_score(self):
        
        
        font = pygame.font.Font(size=50)
        text = font.render(f"Score: {self.score}", True, (200,200,200))
        
        self.screen.blit(text, (10,10))
        return
        
    def path_to_food(self):
        node_list = []

        for i in range(NUMBER_OF_BOXES):
            for j in range(NUMBER_OF_BOXES):
                node_list.append(Node(j, i))
        
        endIndex = self.player.head_position[0] + self.player.head_position[1] * NUMBER_OF_BOXES
        endNode = node_list[endIndex]
        endNode.setEnd()
        
        
        startIndex = self.food.position[0] + self.food.position[1] * NUMBER_OF_BOXES
        startNode = node_list[startIndex]
        startNode.setStart()
        count = 0
        for part_index, part in enumerate(self.player.body[1:]):
            i = part.position[0]
            j = part.position[1]
            
            index = i + j * NUMBER_OF_BOXES            
            
            if (len(self.player.body) - part_index - 2) < (abs(self.player.head_position[0] - part.position[0]) + abs(self.player.head_position[1] - part.position[1])):
                continue
            
            node_list[index].setObstacle()
            count += 1
            
        print("obstacle count: ", count, f"snake size: {self.player.size}")
        open_list = []
        close_list = []
        
        current_node = startNode
        
        pq = PriorityQueue()
        pq.put((0, startNode))
        while(current_node != endNode):
            
            if pq.qsize() == 0:
                print("food unreachable")
                self.updateScreen()
                return Queue()
            
            total_cost, current_node = pq.get()
            
            close_list.append(current_node)
            
            neighbours = current_node.neighboursIndex()
            
            for i, j in neighbours:
                index = i + j * NUMBER_OF_BOXES
                
                # print(index, i ,j)
                if node_list[index] in close_list or node_list[index] in open_list or node_list[index].obstacle:
                    continue
                
                node_list[index].setParent(current_node)
                node_list[index].setCost(current_node.cost)
                node_list[index].setDistance(endNode)
                pq.put(((node_list[index].cost + node_list[index].distanceToEnd * 100), node_list[index]))
                open_list.append(node_list[index])
            
        
        node = endNode
        pathCoords = Queue()
        
        while node.parent != None:
            # print("path : ", node.i, node.j)
            pathCoords.put((node.i, node.j))
            node = node.parent
        
        pathCoords.put((startNode.i, startNode.j))
        
        return pathCoords
    
    def reset_game(self):
        self.player = Player((int(NUMBER_OF_BOXES/2),int(NUMBER_OF_BOXES/2)))
        
        foodPosition = (random.randrange(0, NUMBER_OF_BOXES), random.randrange(0, NUMBER_OF_BOXES))
        self.food = Food()
        self.food.changePosition(foodPosition)    
    
        while self.food in self.player.body: 
            foodPosition = (random.randrange(0, NUMBER_OF_BOXES), random.randrange(0, NUMBER_OF_BOXES))
            self.food.changePosition(foodPosition)

        self.steps = self.path_to_food()

        self.score = 0
        
    def handleKeyboardInput(self):
        if self.enableKeyboard:
            prevDirection = self.player.direction
            keypressed = 0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                
                # if event.type == pygame.KEYDOWN:
                #     self.enableKeyboard = False
                #     if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and self.player.direction != 3:
                #         self.player.direction = 1
                #         keypressed = 1
                #     elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and self.player.direction != 1:
                #         self.player.direction = 3
                #         keypressed = 3
                #     elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and self.player.direction != 2:
                #         self.player.direction = 4
                #         keypressed = 4
                #     elif (event.key == pygame.K_UP or event.key == pygame.K_w) and self.player.direction != 4:
                #         self.player.direction = 2
                #         keypressed = 2
                    
                # if self.player.direction > 0:
                #     self.generateTrainingData(prevDirection)
                    
                # if keypressed > 0:
                #     return
        
        if self.steps.qsize() != 0:
            next_position = self.steps.get()
            
            
            diff_x = self.player.head_position[0] - next_position[0]
            diff_y = self.player.head_position[1] - next_position[1]
            # print("direction : ", diff_x, diff_y)
            
            if diff_x == -1:
                self.player.direction = 3
            if diff_x == 1:
                self.player.direction = 1
            if diff_y == 1:
                self.player.direction = 2
            if diff_y == -1:
                self.player.direction = 4

            
    
    def eatFood(self):
        self.score += 1
        
        # print("food_eaten")
            
        self.player.addBodyPart()
            
        foodPosition = (random.randrange(0, NUMBER_OF_BOXES), random.randrange(0, NUMBER_OF_BOXES))
        while self.food in self.player.body: 
            foodPosition = (random.randrange(0, NUMBER_OF_BOXES), random.randrange(0, NUMBER_OF_BOXES))
            self.food.changePosition(foodPosition)
        
        self.steps = self.path_to_food()
        
    
    def updateScreen(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.display_score()
        self.player.drawPlayer(self.screen)
        self.food.drawFood(self.screen)
        pygame.display.update()
        self.enableKeyboard = True
    
    
    def start_game(self):
        self.run = True
        
        while self.run:
            # print("Hello")
            self.handleKeyboardInput()
            
            self.player.move()
            
            
            if self.player.checkCollision():
                print(f"final score: {self.score}")
                # while self.run:
                #     self.handleKeyboardInput()
                #     pass
                self.reset_game()
            if self.food == self.player.body[0]:
                self.player.direction = 0
                self.eatFood()
            
            # print("Head Position : ", self.player.head_position)
            
            self.updateScreen()
            
            self.fpsClock.tick(FPS)
            
        
        
game = Game(SCREEN_DIMENSIONS)

game.start_game()



# node_list = []

# for i in range(NUMBER_OF_BOXES):
#     for j in range(NUMBER_OF_BOXES):
#         node_list.append(Node(j, i))
        
# start_x, start_y = 10, 10
# start_node_index = start_x + start_y * NUMBER_OF_BOXES
# startNode = node_list[start_node_index]
# startNode.setStart()

# end_x, end_y = 20, 20
# end_node_index = end_x + end_y * NUMBER_OF_BOXES
# endNode = node_list[end_node_index]
# endNode.setEnd()

# def findPathSteps(self, start_pos, end_pos):
    
    
    
#     open_list = []
#     close_list = []
    
#     current_node = startNode
    
#     while(current_node != endNode):
        
#         close_list.append(current_node)
        
#         pq = PriorityQueue()
#         neighbours = current_node.neighboursIndex()
        
#         for i, j in neighbours:
#             index = i + j * NUMBER_OF_BOXES
            
#             if node_list[index] in close_list or node_list[index] in open_list:
#                 continue
            
#             node_list[index].setParent(current_node)
#             node_list[index].setCost(current_node.cost)
#             node_list[index].setDistance(endNode)
#             pq.put(((node_list[index].cost + node_list[index].distanceToEnd), node_list[index]))
#             open_list.append(node_list[index])
        
#         total_cost, current_node = pq.get()
#         print(current_node)
# findPath()
