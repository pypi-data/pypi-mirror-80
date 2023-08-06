from coverage_strategies.src.Entities import Strategy, Slot, Board, Agent
from coverage_strategies.src.SpanningTreeCoverage import is_slot_shallow_obstacle


def get_graph_from_board(b:Board):
    g = Graph()

    for cell_row in b.Slots:
        for cell in cell_row:
            if g.get_vertex(cell) is None:
                g.add_vertex(cell)
            for n in [cell.go_north(), cell.go_south(), cell.go_east(), cell.go_west()]:
                if 0 <= n.row < b.Rows and 0 <= n.col < b.Cols:
                    g.add_edge(cell, n, 1 if not (is_slot_shallow_obstacle(cell, b.Obstacles) or is_slot_shallow_obstacle(n,b.Obstacles)) else sys.maxsize)
    return g

def get_interception_point(steps_o, InitPosX, InitPosY, agentO:Agent):
    ip_x = -1
    ip_y = -1

    steps_counter = 0
    g = get_graph_from_board(agentO.gameBoard)
    start = Slot(InitPosX, InitPosY)
    path_to = []
    for step in steps_o:
        steps_counter += 1

        # computing the distance should be done using dijkstra, since now we allow obstacles
        # create graph from Board (with obstacles)

        dijkstra(g, g.get_vertex(start), g.get_vertex(step))

        target = g.get_vertex(step)
        path = [target.get_id()]
        shortest(target, path)
        # print('The shortest path : %s' % (path[::-1]))

        distance_from_i_r = len(path[::-1])
        if steps_counter > distance_from_i_r:
            ip_x, ip_y = step.row, step.col
            path_to = path[::-1]
            break

    assert (ip_x != -1 and ip_y != -1)

    return Slot(ip_x, ip_y), len(path_to), path_to


class InterceptThenCopy_Strategy(Strategy):
    def get_steps(self, agent_r, board_size=50, agent_o=None):
        # steps_o = StrategyGenerator.get_strategy_from_enum(agent_o.StrategyEnum).get_steps(agent_o, board_size,
        #                                                                                    board_size)
        steps_o = agent_o.steps

        # Find interception point
        (interceptionPoint_R_O, distance, path_to_interception_point) = get_interception_point(steps_o, agent_r.InitPosX, agent_r.InitPosY, agent_o)
        steps_r = run_agent_over_board_interception_strategy(steps_o, path_to_interception_point)
        return steps_r


def run_agent_over_board_interception_strategy(steps_o, path_to):
    steps = []
    steps.extend(path_to)
    steps.extend(steps_o[(steps_o.index(path_to[-1])+1):])

    return steps


# --------------------------------------
import sys
from functools import total_ordering

@total_ordering
class Vertex:
    def __init__(self, node):
        self.id = node
        self.adjacent = {}
        # Set distance to infinity for all nodes
        self.distance = sys.maxsize
        # Mark all nodes unvisited
        self.visited = False
        # Predecessor
        self.previous = None

    def add_neighbor(self, neighbor, weight=0):
        self.adjacent[neighbor] = weight

    def get_connections(self):
        return self.adjacent.keys()

    def get_id(self):
        return self.id

    def get_weight(self, neighbor):
        return self.adjacent[neighbor]

    def set_distance(self, dist):
        self.distance = dist

    def get_distance(self):
        return self.distance

    def set_previous(self, prev):
        self.previous = prev

    def set_visited(self):
        self.visited = True

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.distance == other.distance
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            return self.distance < other.distance

    def __hash__(self):
        return id(self)

    def __str__(self):
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])


class Graph:
    def __init__(self):
        self.vert_dict = {}
        self.num_vertices = 0

    def __iter__(self):
        return iter(self.vert_dict.values())

    def add_vertex(self, node):
        self.num_vertices = self.num_vertices + 1
        new_vertex = Vertex(node)
        self.vert_dict[node] = new_vertex
        return new_vertex

    def get_vertex(self, n):
        if n in self.vert_dict:
            return self.vert_dict[n]
        else:
            return None

    def add_edge(self, frm, to, cost=0):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def get_vertices(self):
        return self.vert_dict.keys()

    def set_previous(self, current):
        self.previous = current

    def get_previous(self, current):
        return self.previous


def shortest(v, path):
    ''' make shortest path from v.previous'''
    if v.previous:
        path.append(v.previous.get_id())
        shortest(v.previous, path)
    return


import heapq


def dijkstra(aGraph, start, target):
    # print('''Dijkstra's shortest path''')
    # Set the distance for the start node to zero
    start.set_distance(0)

    # Put tuple pair into the priority queue
    unvisited_queue = [(v.get_distance(), v) for v in aGraph]
    heapq.heapify(unvisited_queue)

    while len(unvisited_queue):
        # Pops a vertex with the smallest distance
        uv = heapq.heappop(unvisited_queue)
        current = uv[1]
        current.set_visited()

        # for next in v.adjacent:
        for next in current.adjacent:
            # if visited, skip
            if next.visited:
                continue
            new_dist = current.get_distance() + current.get_weight(next)

            if new_dist < next.get_distance():
                next.set_distance(new_dist)
                next.set_previous(current)
                # print('updated : current = %s next = %s new_dist = %s' \
                #       % (current.get_id(), next.get_id(), next.get_distance()))
            else:
                pass
                # print('not updated : current = %s next = %s new_dist = %s' \
                #       % (current.get_id(), next.get_id(), next.get_distance()))

        # Rebuild heap
        # 1. Pop every item
        while len(unvisited_queue):
            heapq.heappop(unvisited_queue)
        # 2. Put all vertices not visited into the queue
        unvisited_queue = [(v.get_distance(), v) for v in aGraph if not v.visited]
        heapq.heapify(unvisited_queue)

# A working example of Graph and dijkstra
# if __name__ == '__main__':
#
#     g = Graph()
#
#     g.add_vertex('a')
#     g.add_vertex('b')
#     g.add_vertex('c')
#     g.add_vertex('d')
#     g.add_vertex('e')
#     g.add_vertex('f')
#
#     g.add_edge('a', 'b', 7)
#     g.add_edge('a', 'c', 9)
#     g.add_edge('a', 'f', 14)
#     g.add_edge('b', 'c', 10)
#     g.add_edge('b', 'd', 15)
#     g.add_edge('c', 'd', 11)
#     g.add_edge('c', 'f', 2)
#     g.add_edge('d', 'e', 6)
#     g.add_edge('e', 'f', 9)
#
#     print('Graph data:')
#     for v in g:
#         for w in v.get_connections():
#             vid = v.get_id()
#             wid = w.get_id()
#             print('( %s , %s, %3d)' % (vid, wid, v.get_weight(w)))
#
#     dijkstra(g, g.get_vertex('a'), g.get_vertex('e'))
#
#     target = g.get_vertex('e')
#     path = [target.get_id()]
#     shortest(target, path)
#     print('The shortest path : %s' % (path[::-1]))
