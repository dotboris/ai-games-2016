from random import choice
from game import Game
from pathfinding import navigate_towards, shortest_path
import webbrowser


class Bot:
    def __init__(self):
        self.healing = False
        self.viewUrl = None

    def hero_distance(self, location):
        return len(shortest_path(self.game.board, self.game.hero.pos, location))

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
            return game.hero.pos

    def best_target_loc(self):
        # target player neirby with lower lifei
        def target_player(p):
            return p.life > self.game.hero.life and len(shortest_path(self.game.board, self.game.hero.pos, p.pos)) <= 2
        targets = filter(lambda p: not target_player(p), self.game.enemies)
        return max(targets, key=lambda t: t.mines)

    def move(self, state):
        if not self.viewUrl:
            self.viewUrl = state['viewUrl']
            webbrowser.open(self.viewUrl, new=2)

        game = Game(state)
        self.game = game
        
        if self.healing and self.game.hero.life >= 99:
            self.healing = False

        if self.game.hero.life <= 35:
            self.healing = True

        dest = self.game.hero.pos
        if self.healing:
            dest = self.closest_tavern()
        else:
            dest = self.closest_enemy_mine(game)

        target = self.best_target_loc()
        if target is not None:
            dest = target.pos 

        if dest == self.game.hero.pos:
            return 'Stay'
        else:
            return navigate_towards(game.board, game.hero.pos, dest)
