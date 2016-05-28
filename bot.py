from random import choice
from game import Game
from pathfinding import navigate_towards, shortest_path
import webbrowser


class Bot:
    def __init__(self):
        self.viewUrl = None

    def freemine(self, game, mines_locs):
        try:
            hero_id = game.hero.id
            untaken_mines = [loc for loc, hero in mines_locs.items() if hero != str(hero_id)]
            return sorted(untaken_mines, key=lambda l: len(shortest_path(game.board, game.hero.pos, l)))[0]
        except:
            return hero.pos

    def move(self, state):
        if not self.viewUrl:
            self.viewUrl = state['viewUrl']
            webbrowser.open(self.viewUrl,new=2)

        game = Game(state)
        dest = self.freemine(game, game.mines_locs)
        return navigate_towards(game.board, game.hero.pos, dest)
