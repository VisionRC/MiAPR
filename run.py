import gym
from gym import wrappers, logger
import random
from heapq import *
import math
import numpy as np
from scipy import ndimage

class Agent(object):
    # [y, x]
    map_path = [([0] * 160) for i in range(210)]
    path = []
    # [y, x]
    map = []
    # (x, y)
    spaceShip_pos = ()
    # (x, y)
    target = ()
    ch_target = 0
    commands = []

    def __init__(self, action_space):
        self.action_space = action_space

    def Make_Map(self, ob):
        self.map = []
        for y in range(210):
            row = []
            for x in range(160):
                if ob[y][x][0] > 0 \
                        or ob[y][x][1] > 0 \
                        or ob[y][x][2] > 0:
                    row.append(1)
                else:
                    row.append(0)
            self.map.append(row)

        _mapp = self.map
        map_new = self.map

        for k in range(15):
            temp_map = [([0] * 160) for i in range(210)]
            for x in range(160):
                for y in range(210):
                    if map_new[y][x] == 1:
                        if 0 <= x - 1 <= 159 and x + 1 <= 159 and \
                                0 <= y - 1 <= 209 and y + 1 <= 209:
                            temp_map[y - 1][x - 1] = 1
                            temp_map[y - 1][x] = 1
                            temp_map[y - 1][x + 1] = 1
                            temp_map[y][x - 1] = 1
                            temp_map[y][x] = 1
                            temp_map[y][x + 1] = 1
                            temp_map[y + 1][x - 1] = 1
                            temp_map[y + 1][x] = 1
                            temp_map[y + 1][x + 1] = 1
            map_new = temp_map
        self.map = map_new

        # f = open("map.txt", "w")
        # for y in range(210):
        #     for x in range(160):
        #         f.write(str(_mapp[y][x]))
        #     f.write("\r")
        #
        # f.close()

    def Find_SpaceShip(self, ob):
        localisation = (80, 106)
        for x in range(160):
            for y in range(210):
                if ob[y][x][0] == 240 \
                        and ob[y][x][1] == 128 \
                        and ob[y][x][2] == 128:
                    localisation = (x, y)
                    break
        self.spaceShip_pos = localisation

    def Create_Target(self):
        x = random.randrange(60, 100, 1)
        y = random.randrange(80, 130, 1)

        map_new = self.map

        for k in range(20):
            temp_map = [([0] * 160) for i in range(210)]
            for x in range(160):
                for y in range(210):
                    if map_new[y][x] == 1:
                        if 0 <= x - 1 <= 159 and x + 1 <= 159 and \
                                0 <= y - 1 <= 209 and y + 1 <= 209:
                            temp_map[y - 1][x - 1] = 1
                            temp_map[y - 1][x] = 1
                            temp_map[y - 1][x + 1] = 1
                            temp_map[y][x - 1] = 1
                            temp_map[y][x] = 1
                            temp_map[y][x + 1] = 1
                            temp_map[y + 1][x - 1] = 1
                            temp_map[y + 1][x] = 1
                            temp_map[y + 1][x + 1] = 1
            map_new = temp_map
        _map = np.array(map_new)
        table = np.argwhere(_map == 0)
        random_num = random.choice(table)
        (x, y) = random_num
        # print(random_num)
        # f = open("d1.txt", "w")
        #
        # for y in range(210):
        #     f.write(str(map_new[y]))
        #     f.write("\r")
        #
        # f.close()

        # while self.map[y][x] == 1:
        #     x = random.randrange(60, 100, 1)
        #     y = random.randrange(80, 130, 1)

        self.target = (x, y)

        # if self.spaceShip_pos == (80, 106):
        #     # Brak statku
        #     x = random.randrange(60, 100, 1)
        #     y = random.randrange(80, 130, 1)
        #     self.target = (x, y)
        # else:
        #     (a, b) = self.spaceShip_pos
        #     if 0 <= a - 25 <= 159 and a + 25 <= 159 and \
        #             0 <= b - 25 <= 209 and b + 25 <= 209:
        #         square = np.array(self.map)
        #         square = square[a - 25:a + 25, b - 25:b + 25]
        #
        #         (x1, y1) = ndimage.measurements.center_of_mass(square, labels=None, index=0)
        #         x1 = x1.astype(int)
        #         y1 = y1.astype(int)
        #         if square[y1, x1] == 0:
        #             x = x1
        #             y = y1
        #             print(x, y)
        #             self.target = (x, y)
        #         else:
        #             while self.map[y1][x1] == 1:
        #                 x = random.randrange(60, 100, 1)
        #                 y = random.randrange(80, 130, 1)
        #                 print(x, y)
        #                 self.target = (x, y)

    def PlanedPath_Robot(self):

        (x, y) = self.spaceShip_pos
        self.path.append([x, y])

        for q in range(len(self.path)):
            (x1, y1) = self.path[q]
            self.map_path[y1][x1] = "@"

        # print(len(self.path))

        if self.ch_target%10 == 1:
            for i in range(len(self.commands)):
                if self.commands[i] == 2:
                    y = y + 1
                    self.map_path[y][x] = '#'
                if self.commands[i] == 6:
                    x = x + 1
                    self.map_path[y][x] = '#'
                if self.commands[i] == 7:
                    x = x - 1
                    self.map_path[y][x] = '#'
                if self.commands[i] == 12:
                    y = y + 1
                    x = x + 1
                    self.map_path[y][x] = '#'
                if self.commands[i] == 13:
                    y = y - 1
                    x = x - 1
                    self.map_path[y][x] = '#'

        f = open("path.txt", "w")
        for y in range(210):
            for x in range(160):
                f.write(str(self.map_path[y][x]))
            f.write("\r")
        f.close()

    def Astar(self):

        Directions = {
            # UP/FOWARD
            2: (0, 1),
            # RIGHT-SPIN???
            6: (1, 0),
            # LEFT-SPIN???
            7: (-1, 0),
            # RIGHT-DOWN?
            # 12: (1, 1),
            # LEFT - DOWN?
            # 13: (-1, -1)
        }
        Inverted = {v: k for k, v in Directions.items()}

        start = self.spaceShip_pos
        end = self.target
        neighbors = list(Directions.values())

        def h(a, b):
            return math.pow((b[0] - a[0]), 2) + math.pow((b[1] - a[1]), 2)

        close_set = set()
        came_from = {}
        gscore = {start: 0}
        fscore = {start: h(start, end)}
        oheap = []

        heappush(oheap, (fscore[start], start))

        while oheap:

            current = heappop(oheap)[1]

            if current == end:
                data = []
                while current in came_from:
                    before = came_from[current]
                    action = (current[0] - before[0], current[1] - before[1])
                    data.append(Inverted[action])
                    current = came_from[current]
                if data:
                    self.commands = data
                return data[0]

            close_set.add(current)
            for i, j in neighbors:
                neighbor = (current[0] + i, current[1] + j)
                tentative_g_score = gscore[current] + h(current, neighbor)
                if neighbor[0] < 0 or neighbor[0] >= 210:
                    continue
                if neighbor[1] < 0 or neighbor[1] >= 160:
                    continue
                if self.map[neighbor[0]][neighbor[1]] == 1:
                    continue
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + h(end, neighbor)
                    heappush(oheap, (fscore[neighbor], neighbor))
        return 0

def main():
    # Set Level 20
    logger.set_level(logger.INFO)
    # Set game environment
    env = gym.make('Asteroids-v0')
    # Output directory
    outdir = '/home/dc/Desktop/Asteroids/mp4'
    # Set monitor
    env = wrappers.Monitor(env, directory=outdir, force=True)

    # Random numbers generator
    env.seed(0)
    # Send valid actions
    agent = Agent(env.action_space)

    # Number of games
    episode_count = 1
    reward = 0
    # False for "game is not over yet"
    done = False

    for i in range(episode_count):
        # Returns initial observation
        ob = env.reset()
        while True:
            agent.Make_Map(ob)
            agent.Find_SpaceShip(ob)

            if agent.ch_target % 8 == 1 or agent.ch_target == 0:
                agent.Create_Target()

            action = agent.Astar()
            # agent.PlanedPath_Robot()

            # Take action
            ob, reward, done, info = env.step(6)
            agent.ch_target += 1
            # If no more lives left
            if done:
                break
    # Close the env and write monitor result info to disk
    env.close()

main()
