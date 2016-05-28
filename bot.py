from random import choice
from game import Game
from pathfinding import navigate_towards, shortest_path


class Bot:
    def move(self, state):
        game = Game(state)
        # TODO implement SkyNet here
        # Pathfinding example:
        # dir = navigate_towards(game.board, game.hero.pos, (0, 0))
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        return choice(dirs)
