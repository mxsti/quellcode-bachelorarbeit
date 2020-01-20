import pygame
import random
import math

pygame.init()
pygame.font.init()

win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Dodge Game")
clock = pygame.time.Clock()
myfont = pygame.font.SysFont('Arial', 24)
counter = 0
#barrier_list = []

class player(object):
    def __init__(self, x, width, height, speed):
        self.x = x
        self.y = 450
        self.width = width
        self.height = height
        self.speed = speed
    
    def draw(self, win):
        pygame.draw.polygon(win, (0, 255, 0), [(self.x - self.width/2, self.y + self.height/2), (self.x + self.height/2, self.y + self.height/2), (self.x, self.y - self.height/2)])

    def update_pos(self, direction):
        if direction is 0:
            self.x -= self.speed
        elif direction is 1:
            self.x += self.speed


class barrier(object):
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))
    
    def update_pos(self):
        self.y += self.speed

def check_collision(player, barrier):
    if barrier.x - player.width/2 <= (player.x) <= barrier.x + barrier.width + player.width/2 and barrier.y == 440:
        return True
    return False

def get_distance(player, barrier):
    distance = math.sqrt(((player.x - barrier.x) ** 2) + ((player.y - barrier.y) ** 2))
    return int(distance)

# game loop
p = player(random.randint(0, 400), 50, 50, 30)
curr_barrier = barrier(random.randint(0, 400), 0, 150, 10, 20)
run = True
while run:
    clock.tick(10)
    counter += 1

    if counter == 200:
        run = False

    if counter % 30 == 0:
        curr_barrier = barrier(random.randint(0, 400), 0, 150, 10, 20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and p.x > 60 + p.width/2:
        p.update_pos(0)

    if keys[pygame.K_RIGHT] and p.x < 440 - p.width/2:
        p.update_pos(1)

    win.fill((0,0,0))

    # draw stuff
    text = myfont.render(f"Score: {counter}", True, (255, 255, 255))
    win.blit(text, (10, 10))
    p.draw(win)
    curr_barrier.update_pos()
    curr_barrier.draw(win)

    if check_collision(p, curr_barrier):
        run = False

    pygame.display.update()