from game import AIM


def navigate_towards(board, source, destination):
    """
    Finds the shortest path from 'source' to 'destination' and returns the
    direction to take a single step towards that path.

    :param source:      source location (row, column) (e.g. location of your
                        hero)
    :param destination: destination location (row, column) (e.g. location of a
                        mine)
    :returns:           direction (string) to take to follow the optimal path
    """
    path = shortest_path(board, source, destination)
    target = path[0] if path else source
    return _direction_towards(source, target)


def shortest_path(board, source, destination):
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
            predecessors[v] = u

            nodes.add(v)

    return _build_path(destination, predecessors)


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
