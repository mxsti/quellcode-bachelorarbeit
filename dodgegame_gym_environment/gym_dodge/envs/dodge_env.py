import gym
from gym import error, spaces, utils
from gym.utils import seeding
import pygame
import random
import numpy as np
import math

class Player(object):
    def __init__(self, x, y, width, height, speed):
        self.x = x
        self.y = y
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
        elif direction is 2:
            pass


class Barrier(object):
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


class DodgeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.counter = 0
        self.player = Player(250, 450, 50, 50, 30)
        self.curr_barrier = Barrier(random.randint(0, 400), 0, 150, 10, 20)
        self.max_barriery = 600
        self.action_space = spaces.Discrete(3)

        self.min_playerx = 60
        self.max_playerx = 440
        self.min_barrierx = 0
        self.max_barrierx = 400
        
        self.low = np.array([self.min_playerx, self.min_barrierx])
        self.high = np.array([self.max_playerx, self.max_barrierx])

        #observation space with position
        self.observation_space = spaces.Box(self.low, self.high, dtype=np.int16)

        #observation space with distance
        #self.observation_space = spaces.Box(low=0, high=500, shape=(1,), dtype=np.int16)

        #rendering stuff
        pygame.init()
        pygame.font.init()
        self.win = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("Dodge Game")
        self.myfont = pygame.font.SysFont('Arial', 24)

        self.reset()

    def step(self, action):
        #action can be 0 for moving left or 1 for moving right or 2 to keep position
        if action not in range(0,3):
            raise Exception(f"Invalid action: {action}")
        
        self.counter+=1
        #add new barrier periodically
        if self.counter % 30 == 0:
            self.curr_barrier = Barrier(random.randint(0, 400), 0, 150, 10, 20)
        #move player left or right or stay
        if (
            action == 0 and 
            self.player.x > self.min_playerx + self.player.width/2
        ):
            self.player.update_pos(0)
        
        if action == 1 and self.player.x < self.max_playerx - self.player.width/2:
            self.player.update_pos(1)

        if action == 2:
            self.player.update_pos(2)

        #move barrier down
        self.curr_barrier.update_pos()

        result, done = self.is_over()
        state = self.get_game_state()
        #reward = 1
        reward = self.get_reward(result)
        return state, reward, done, {}

    def reset(self):
        self.player = Player(250, 450, 50, 50, 30)
        self.curr_barrier = Barrier(random.randint(0, 400), 0, 150, 10, 20)
        self.counter = 0
        return np.array([self.player.x, 0])

    def render(self, mode='human', close='False'):
        #renders game state
        self.win.fill((0,0,0))
        text = self.myfont.render(f"Score: {self.counter}", True, (255, 255, 255))
        self.win.blit(text, (10, 10))
        self.player.draw(self.win)
        self.curr_barrier.draw(self.win)
        pygame.display.update()
    
    def get_game_state(self):
        #return np.array([self.get_distance()])
        player_pos = np.array(self.player.x)
        barrier_pos = np.array(self.curr_barrier.x)
        return np.array((player_pos, barrier_pos))

    def get_reward(self, result):
        #calculates reward for each action
        rewards = {
            "alive": 1,
            "win": 20,
            "dead": -20,
        }
        #check win or lose
        if len(result)>0:
            return rewards[result]
        return rewards["alive"]

    def check_collision(self):
        if self.curr_barrier.x - self.player.width/2 <= (self.player.x) <= self.curr_barrier.x + self.curr_barrier.width + self.player.width/2 and self.curr_barrier.y == 440:
            return True
        return False
    
    def get_distance(self):
        distance = math.sqrt(((self.player.x - self.curr_barrier.x) ** 2) + ((self.player.y - self.curr_barrier.y) ** 2))
        return int(distance)

    def is_over(self):
        if self.counter == 200:
            return "win", True
        if self.check_collision():
            return "dead", True
        return "", False