import pygame
import random
import neat
import os
import math
import pickle

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

STAT_FONT = pygame.font.SysFont("comicsans", 30)

dis_dim = 300
dis_width = dis_dim
dis_height = dis_dim

dis = pygame.display.set_mode((dis_width, dis_height))
clock = pygame.time.Clock()

block_size = 10
snake_speed = 20
clock_true = True
init_max_moves = 2*dis_dim-2
gen = 0


class Snake:
    def __init__(self, length, snake_block, snake_list, x1, y1, x1_change, y1_change, food):
        self.snake_block = snake_block
        self.snake_list = snake_list
        self.x1 = x1
        self.y1 = y1
        self.x1_change = x1_change
        self.y1_change = y1_change
        self.snake_Head = []
        self.length = length
        self.origDist = math.sqrt(math.pow((food.x - self.x1), 2) + math.pow((food.y - self.y1), 2))
        self.num_moves = 0

    def didMoveTowardsFood(self, food):
        boolean = False
        newDist = math.sqrt(math.pow((food.x - self.x1), 2) + math.pow((food.y - self.y1), 2))
        if newDist <= self.origDist:
            boolean = True
        self.origDist = newDist
        return boolean

    def getDistFromFood(self, food):
        return math.sqrt(math.pow((food.x - self.x1), 2) + math.pow((food.y - self.y1), 2))

    # def getDistFromCenter(self):
    #     return math.sqrt(math.pow((dis_width/2 - self.x1), 2) + math.pow((dis_height/2 - self.y1), 2))

    def didCollideWithEdge(self):
        return self.x1 >= dis_width or self.x1 < 0 or self.y1 >= dis_height or self.y1 < 0

    def didCollideWithSelf(self):
        for x in self.snake_list[:-1]:
            if x == self.snake_Head:
                return True
        return False

    def didCollideWithFood(self, food):
        return self.x1 == food.x and self.y1 == food.y

    def distStraightToWall(self):
        if self.x1_change < 0:
            return math.sqrt(math.pow((0 - self.x1), 2))
        elif self.x1_change > 0:
            return math.sqrt(math.pow((dis_width - self.x1 - block_size), 2))
        elif self.y1_change < 0:
            return math.sqrt(math.pow((0 - self.y1), 2))
        elif self.y1_change > 0:
            return math.sqrt(math.pow((dis_height - self.y1 - block_size), 2))
        else:
            # print("This brokeSW")
            return -1

    def distRightToWall(self):
        if self.x1_change < 0:
            return math.sqrt(math.pow((0 - self.y1), 2))
        elif self.x1_change > 0:
            return math.sqrt(math.pow((dis_height - self.y1 - block_size), 2))
        elif self.y1_change < 0:
            return math.sqrt(math.pow((dis_width - self.x1 - block_size), 2))
        elif self.y1_change > 0:
            return math.sqrt(math.pow((0 - self.x1), 2))
        else:
            # print("This brokeRW")
            return -1

    def distLeftToWall(self):
        if self.x1_change < 0:
            return math.sqrt(math.pow((dis_height - self.y1 - block_size), 2))
        elif self.x1_change > 0:
            return math.sqrt(math.pow((0 - self.y1), 2))
        elif self.y1_change < 0:
            return math.sqrt(math.pow((0 - self.x1), 2))
        elif self.y1_change > 0:
            return math.sqrt(math.pow((dis_width - self.x1 - block_size), 2))
        else:
            # print("This brokeLW")
            return -1

    def distStraightToFood(self, food):
        #if not fixed edit the value to be like toWall (add the block_size)
        # if not (self.x1 == food.x or self.y1 == food.y):
        #     return -1
        if self.x1_change < 0 and food.x < self.x1 and self.y1 == food.y:
            return self.getDistFromFood(food)
        elif self.x1_change > 0 and food.x > self.x1 and self.y1 == food.y:
            return self.getDistFromFood(food)
        elif self.y1_change < 0 and food.y < self.y1 and self.x1 == food.x:
            return self.getDistFromFood(food)
        elif self.y1_change < 0 and food.y > self.y1 and self.x1 == food.x:
            return self.getDistFromFood(food)
        else:
            # print("this brokeSF")
            return -1

    def distRightToFood(self, food):
        # if not (self.x1 == food.x or self.y1 == food.y):
        #     return -1
        if self.x1_change < 0 and food.y < self.y1 and self.x1 == food.x:
            return self.getDistFromFood(food)
        elif self.x1_change > 0 and food.y > self.y1 and self.x1 == food.x:
            return self.getDistFromFood(food)
        elif self.y1_change < 0 and food.x > self.x1 and self.y1 == food.y:
            return self.getDistFromFood(food)
        elif self.y1_change > 0 and food.x < self.x1 and self.y1 == food.y:
            return self.getDistFromFood(food)
        else:
            # print("this brokeRF")
            return -1

    def distLeftToFood(self, food):
        # if not (self.x1 == food.x or self.y1 == food.y):
        #     return -1
        if self.x1_change < 0 and food.y > self.y1 and self.x1 == food.x:
            return self.getDistFromFood(food)
        elif self.x1_change > 0 and food.y < self.y1 and self.x1 == food.x:
            return self.getDistFromFood(food)
        elif self.y1_change < 0 and food.x < self.x1 and self.y1 == food.y:
            return self.getDistFromFood(food)
        elif self.y1_change > 0 and food.x > self.x1 and self.y1 == food.y:
            return self.getDistFromFood(food)
        else:
            # print("this brokeLF")
            return -1

    def distStraightToSelf(self):
        if self.length < 4:
            return -1
        else:
            self.x1 = int(self.x1)
            self.x1_change = int(self.x1_change)
            self.y1 = int(self.y1)
            self.y1_change = int(self.y1_change)
            if self.x1_change < 0:
                for i in range(self.x1 + self.x1_change, 0, self.x1_change):
                    if (i, self.y1) in self.snake_list:
                        return math.sqrt(math.pow((i - self.x1), 2))
            elif self.x1_change > 0:
                for i in range(self.x1 + self.x1_change, dis_width, self.x1_change):
                    if (i, self.y1) in self.snake_list:
                        return math.sqrt(math.pow((i - self.x1), 2))
            elif self.y1_change < 0:
                for i in range(self.y1 + self.y1_change, 0, self.y1_change):
                    if (self.x1, i) in self.snake_list:
                        return math.sqrt(math.pow((i - self.y1), 2))
            elif self.y1_change > 0:
                for i in range(self.y1 + self.y1_change, dis_height, self.y1_change):
                    if (self.x1, i) in self.snake_list:
                        return math.sqrt(math.pow((i - self.y1), 2))
            # print("this brokeS")
            return 0

    def distRightToSelf(self):
        if self.length < 4:
            return -1
        else:
            self.x1 = int(self.x1)
            self.x1_change = int(self.x1_change)
            self.y1 = int(self.y1)
            self.y1_change = int(self.y1_change)
            if self.x1_change < 0:
                for i in range(self.y1 - block_size, 0, -block_size):
                    if (self.x1, i) in self.snake_list:
                        return math.sqrt(math.pow((i - self.y1), 2))
            elif self.x1_change > 0:
                for i in range(self.y1 + block_size, dis_height, block_size):
                    if (self.x1, i) in self.snake_list:
                        return math.sqrt(math.pow((i - self.y1), 2))
            elif self.y1_change < 0:
                for i in range(self.x1 + block_size, dis_width, block_size):
                    if (i, self.y1) in self.snake_list:
                        return math.sqrt(math.pow((i - self.x1), 2))
            elif self.y1_change > 0:
                for i in range(self.x1 - block_size, 0, -block_size):
                    if (i, self.y1) in self.snake_list:
                        return math.sqrt(math.pow((i - self.x1), 2))
            # print("this brokeS")
            return 0

    def distLeftToSelf(self):
        if self.length < 4:
            return -1
        else:
            self.x1 = int(self.x1)
            self.x1_change = int(self.x1_change)
            self.y1 = int(self.y1)
            self.y1_change = int(self.y1_change)
            if self.x1_change > 0:
                for i in range(self.y1 - block_size, 0, -block_size):
                    if (self.x1, i) in self.snake_list:
                        return math.sqrt(math.pow((i - self.y1), 2))
            elif self.x1_change < 0:
                for i in range(self.y1 + block_size, dis_height, block_size):
                    if (self.x1, i) in self.snake_list:
                        return math.sqrt(math.pow((i - self.y1), 2))
            elif self.y1_change > 0:
                for i in range(self.x1 + block_size, dis_width, block_size):
                    if (i, self.y1) in self.snake_list:
                        return math.sqrt(math.pow((i - self.x1), 2))
            elif self.y1_change < 0:
                for i in range(self.x1 - block_size, 0, -block_size):
                    if (i, self.y1) in self.snake_list:
                        return math.sqrt(math.pow((i - self.x1), 2))
            # print("this brokeS")
            return 0

    def move(self, dir):
        #0 == straight, 1 == left, 2 == right
        if dir == 1:
            if self.x1_change < 0 and self.y1_change == 0:
                self.x1_change = 0
                self.y1_change = block_size
            elif self.x1_change > 0 and self.y1_change == 0:
                self.x1_change = 0
                self.y1_change = -block_size
            elif self.y1_change < 0 and self.x1_change == 0:
                self.x1_change = -block_size
                self.y1_change = 0
            elif self.y1_change > 0 and self.x1_change == 0:
                self.x1_change = block_size
                self.y1_change = 0
            else:
                print("this broke")
        if dir == 2:
            if self.x1_change < 0 and self.y1_change == 0:
                self.x1_change = 0
                self.y1_change = -block_size
            elif self.x1_change > 0 and self.y1_change == 0:
                self.x1_change = 0
                self.y1_change = block_size
            elif self.y1_change < 0 and self.x1_change == 0:
                self.x1_change = block_size
                self.y1_change = 0
            elif self.y1_change > 0 and self.x1_change == 0:
                self.x1_change = -block_size
                self.y1_change = 0
            else:
                print("this broke")

        self.x1 += self.x1_change
        self.y1 += self.y1_change
        self.snake_Head = [self.x1, self.y1]
        self.snake_list.append(self.snake_Head)
        if len(self.snake_list) > self.length:
            del self.snake_list[0]
        self.num_moves += 1

    def draw(self, color):
        for x in self.snake_list:
            pygame.draw.rect(dis, color, [x[0], x[1], self.snake_block, self.snake_block])


class Food:
    def __init__(self, posx, posy):
        self.x = posx
        self.y = posy

    def draw(self):
        pygame.draw.rect(dis, green, [self.x, self.y, block_size, block_size])

    def newPos(self):
        self.x = round(random.randrange(10, dis_width - 2 * block_size) / 10.0) * 10.0
        self.y = round(random.randrange(10, dis_width - 2 * block_size) / 10.0) * 10.0


def getInitStart(length):
    if length <= 1:
        return []
    else:
        pos = []
        for i in range(length-1,-1,-1):
            pos.append((dis_width / 2, (dis_height / 2) + block_size*i))
        return pos


def main(genomes, config):
    global gen
    nets = []
    ge = []

    snakes = []
    foods = []

    global clock_true

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        food = Food(round(random.randrange(10, dis_width - 2 * block_size) / 10.0) * 10.0,
                    round(random.randrange(10, dis_height - 2 * block_size) / 10.0) * 10.0)
        snakes.append(Snake(5, block_size, getInitStart(5), dis_width / 2, dis_height / 2, 0, -block_size, food))
        foods.append(food)
        g.fitness = 0
        ge.append(g)

    running = True
    while running:
        dis.fill(blue)
        if clock_true:
            clock.tick(snake_speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    clock_true = True
                if event.key == pygame.K_f:
                    clock_true = False

        if len(snakes) == 0:
            running = False
            break

        top3 = []
        for snake in snakes:
            top3.append(snake.length)
        while len(top3) > 3:
            top3.remove(min(top3))

        #check output, food eaten and draw stuff and fitness
        for x, food in enumerate(foods):
            snake = snakes[x]
            output = nets[x].activate((snake.distStraightToWall(), snake.distLeftToWall(), snake.distRightToWall(),
                                      snake.distStraightToFood(food), snake.distLeftToFood(food), snake.distRightToFood(food),
                                      snake.distStraightToSelf(), snake.distLeftToSelf(), snake.distRightToSelf()))
            # print(output)
            dir = output.index(max(output))
            snake.move(dir)
            if snake.length in top3:
                if snake.length == max(top3):
                    snake.draw(pygame.Color("red"))
                else:
                    snake.draw(pygame.Color("black"))
                food.draw()
            if not snake.didMoveTowardsFood(food):
                ge[x].fitness -= 1.5
            else:
                ge[x].fitness += 1
            if snake.didCollideWithFood(food):
                ge[x].fitness += 10
                food.newPos()
                snake.length += 1
                snake.num_moves -= 2*dis_dim-2
            snake.num_moves += 1
            if snake.didCollideWithEdge():
                foods.pop(x)
                nets.pop(x)
                ge.pop(x)
                snakes.pop(x)
            if snake.didCollideWithSelf():
                foods.pop(x)
                ge[x].fitness -= 5
                nets.pop(x)
                ge.pop(x)
                snakes.pop(x)
            if snake.num_moves >= init_max_moves:
                foods.pop(x)
                ge[x].fitness -= 10
                nets.pop(x)
                ge.pop(x)
                snakes.pop(x)

        text = STAT_FONT.render("# alive: " + str(len(snakes)), 1, (255, 255, 255))
        dis.blit(text, (dis_width - 10 - text.get_width(), 10))
        text = STAT_FONT.render("Gen: " + str(gen), 1, (255, 255, 255))
        dis.blit(text, (dis_width - 10 - text.get_width(), 30))
        if len(snakes) > 0:
            lengths = []
            for snake in snakes:
                lengths.append(snake.length)
            text = STAT_FONT.render("Longest Snake: " + str(max(lengths)), 1, (255, 255, 255))
            dis.blit(text, (dis_width - 10 - text.get_width(), 50))
        pygame.display.update()
    gen += 1


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 20)
    with open("bestmodel.pickle", "wb") as f:
        pickle.dump(winner, f)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "conf-feedforward2.txt")
    run(config_path)
