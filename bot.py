from random import choice
from game import Game
from pathfinding import navigate_towards, shortest_path
import webbrowser


class Bot:
    def __init__(self):
        self.viewUrl = None
        
    def freemine(self, game, mines_locs):
        untaken_mines = [loc for loc, hero in mines_locs.items() if hero == '-']
        return sorted(untaken_mines, key=lambda l: len(shortest_path(game.board, game.hero.pos, l)))[0]

    def move(self, state):
        if not self.viewUrl:
            self.viewUrl = state['viewUrl']
            webbrowser.open(self.viewUrl,new=2)

        game = Game(state)
        # TODO implement SkyNet here
        # Pathfinding example:
        # dir = navigate_towards(game.board, game.hero.pos, (0, 0))
        dirs = ['Stay', 'North', 'South', 'East', 'West']
        dest = self.freemine(game, game.mines_locs)
        print('dest is ' +  repr(dest))
        return navigate_towards(game.board, game.hero.pos, dest)
