import re

TAVERN = 0
AIR = -1
WALL = -2
SPIKE = -3

PLAYER1 = 1
PLAYER2 = 2
PLAYER3 = 3
PLAYER4 = 4

AIM = {'North': (-1, 0),
       'East': (0, 1),
       'South': (1, 0),
       'West': (0, -1)}

class HeroTile:
    def __init__(self, id):
        self.id = id

class MineTile:
    def __init__(self, heroId = None):
        self.heroId = heroId

class Game:
    def __init__(self, state):
        self.state = state
        self.board = Board(state['game']['board'])
        self.heroes = [Hero(state['game']['heroes'][i]) for i in range(len(state['game']['heroes']))]
        self.hero = self.heroes[int(state['hero']['id']) - 1]
        self.mines_locs = {}
        self.heroes_locs = {}
        self.taverns_locs = set([])
        self.spikes_locs = set([])
        for row in range(len(self.board.tiles)):
            for col in range(len(self.board.tiles[row])):
                obj = self.board.tiles[row][col]
                if isinstance(obj, MineTile):
                    self.mines_locs[(row, col)] = obj.heroId
                elif isinstance(obj, HeroTile):
                    self.heroes_locs[(row, col)] = obj.id
                elif (obj == TAVERN):
                    self.taverns_locs.add((row, col))
                elif (obj == SPIKE):
                    self.spikes_locs.add((row, col))



class Board:
    def __parseTile(self, str):
        if (str == '  '):
            return AIR
        if (str == '##'):
            return WALL
        if (str == '[]'):
            return TAVERN
        if (str == '^^'):
            return SPIKE
        match = re.match('\$([-0-9])', str)
        if (match):
            return MineTile(match.group(1))
        match = re.match('\@([0-9])', str)
        if (match):
            return HeroTile(match.group(1))

    def __parseTiles(self, tiles):
        vector = [tiles[i:i+2] for i in range(0, len(tiles), 2)]
        matrix = [vector[i:i+self.size] for i in range(0, len(vector), self.size)]

        return [[self.__parseTile(x) for x in xs] for xs in matrix]

    def __init__(self, board):
        self.size = board['size']
        self.tiles = self.__parseTiles(board['tiles'])

    def passable(self, loc):
        'true if can walk through'
        row, col = loc
        pos = self.tiles[row][col]
        return (pos != WALL) and (pos != TAVERN) and not isinstance(pos, MineTile)

    def to(self, loc, direction):
        'calculate a new location given the direction'
        row, col = loc
        d_row, d_col = AIM[direction]
        n_row = row + d_row
        if (n_row < 0): n_row = 0
        if (n_row >= self.size): n_row = self.size - 1
        n_col = col + d_col
        if (n_col < 0): n_col = 0
        if (n_col >= self.size): n_col = self.size - 1

        return (n_row, n_col)



class Hero:
    def __init__(self, hero):
        self.id = hero['id']
        self.name = hero['name']
        self.pos = (int(hero['pos']['x']), int(hero['pos']['y']))
        self.life = hero['life']
        self.gold = hero['gold']
