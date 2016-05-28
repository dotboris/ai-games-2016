from random import choice
from game import Game
from pathfinding import navigate_towards, shortest_path
import webbrowser


class Bot:
    def __init__(self):
        self.healing = False
        self.viewUrl = None

    def hero_distance(self, location):
        return len(shortest_path(self.game, self.game.hero.pos, location))

    def closest_enemy_mine(self, game):
        try:
            hero_id = game.hero.id
            mines_locs = game.mines_locs
            untaken_mines = [loc for loc, hero in mines_locs.items() if hero != str(hero_id)]
            return min(untaken_mines, key=self.hero_distance)
        except Exception as e:
            return game.hero.pos

    def closest_tavern(self):
        try:
            return min(self.game.taverns_locs, key=self.hero_distance)
        except:
            return self.game.hero.pos

    def move(self, state):
        if not self.viewUrl:
            self.viewUrl = state['viewUrl']
            webbrowser.open(self.viewUrl, new=2)

        game = Game(state)
        self.game = game

        if self.healing and self.game.hero.life >= 99:
            self.healing = False

        closest_tavern = self.closest_tavern()
        heal_treshold = self.hero_distance(closest_tavern) * 2 + 26
        if self.game.hero.life <= heal_treshold:
            self.healing = True

        dest = self.game.hero.pos
        if self.healing:
            dest = closest_tavern
        else:
            dest = self.closest_enemy_mine(game)

        if dest == self.game.hero.pos:
            return 'Stay'
        else:
            return navigate_towards(game, game.hero.pos, dest)
