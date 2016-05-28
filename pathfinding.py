from game import AIM, SPIKE, HeroTile


def navigate_towards(game, source, destination):
    """
    Finds the shortest path from 'source' to 'destination' and returns the
    direction to take a single step towards that path.

    :param source:      source location (row, column) (e.g. location of your
                        hero)
    :param destination: destination location (row, column) (e.g. location of a
                        mine)
    :returns:           direction (string) to take to follow the optimal path
    """
    path = shortest_path(game, source, destination)
    target = path[0] if path else source
    return _direction_towards(source, target)


def shortest_path(game, source, destination):
    """
    Finds the shortest path from 'source' to 'destination' and returns the
    sequence of locations to follow to take the optimal path (excluding
    'source', including 'destination').

    :param source:      source location (row, column) (e.g. location of your
                        hero)
    :param destination: destination location (row, column) (e.g. location of a
                        mine)
    :returns:           list of locations to go to in order to reach the
                        destination
    """
    others_pos = [hero.pos for hero in game.heroes if hero.id != game.hero.id]
    #danger_zones = [adj for other in others_pos for adj in _neighbors(game, other)]

    health_percent = game.hero.life / 100
    if health_percent > 1 or health_percent < 0: print('what!')

    board = game.board
    nodes = set([source])
    distances = {source: 0}
    predecessors = {}

    while nodes:
        u = min(nodes, key=lambda n: distances[n])
        nodes.remove(u)

        neighbor_tiles = [board.to(u, direction) for direction in AIM.keys()]

        if destination in neighbor_tiles:
            predecessors[destination] = u
            break

        neighbors = [tile for tile in neighbor_tiles
                     if (tile != u and board.passable(tile) and
                         tile not in distances)]

        for v in neighbors:
            distances[v] = distances[u] + 1

            tile = board.tiles[v[0]][v[1]]
            if tile == SPIKE:
                distances[v] += abs(10 * (1 - health_percent))

            for o in others_pos:
                if (approx_distance(game.hero.pos, o) <= 2) and (v in _neighbors(game, o)) and (health_percent <= 0.5):
                    distances[v] += 2

            predecessors[v] = u

            nodes.add(v)

    return _build_path(destination, predecessors)


def approx_distance(a, b):
    return abs((a[0] - b[0]) + (a[1] - b[1]))


def _neighbors(game, pos):
    return set([game.board.to(pos, 'North'), game.board.to(pos, 'East'), game.board.to(pos, 'South'), game.board.to(pos, 'West')])

def _build_path(destination, predecessors):
    path = []
    n = destination

    while n in predecessors:
        path.append(n)
        n = predecessors[n]

    path.reverse()

    return path


def _direction_towards(source, destination):
    src_row, src_col = source
    dst_row, dst_col = destination

    if src_row > dst_row: return 'North'
    if src_row < dst_row: return 'South'
    if src_col > dst_col: return 'West'
    if src_col < dst_col: return 'East'
    return 'Stay'
