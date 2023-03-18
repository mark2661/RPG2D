import heapq
import math
import sys
from typing import TYPE_CHECKING, Tuple, List, Dict, Set, Optional


if TYPE_CHECKING:
    import pygame
    from tile import Tile
    from level import Level


def heuristic(a: "Tile", b: "Tile") -> float:
    # get centre coords for the pygame.Rect objects of each tile
    a: Tuple[float, float] = a.rect.center
    b: Tuple[float, float] = b.rect.center
    # Manhattan distance between the centre points of the pygame.Rect objects of each tile
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


# def a_star(grid: List["Tile"], start: "Tile", end: "Tile", level: "Level") -> Optional[List["Tile"]]:
#     heap_entry_count: int = 0  # variable to keep track of the order of objects entered into the heap
#     open_list: heapq = [(0, heap_entry_count, start)]
#     g_scores: Dict[Tile, float] = {tile: sys.maxsize for tile in grid}
#     # set g score of first tile to zero
#     g_scores[start] = 0
#     f_scores: Dict[Tile, float] = {tile: sys.maxsize for tile in grid}
#     f_scores[start] = heuristic(start, end)
#     closed_list: Set = set()
#
#     # keep track of preceding path
#     parents: Dict[Tile, Optional[Tile]] = {start: None}
#
#     while open_list:
#         f: float
#         current: Tile
#         f, _, current = heapq.heappop(open_list)
#
#         # if the end tile is being process stop the algorithm and return the best path
#         if current == end:
#             path: List[Tile] = []
#             while current:
#                 path.append(current)
#                 current = parents[current]
#             return path[::-1]  # reverse path so tiles are ordered from start -> end
#
#         # process neighbours of current vertex
#         for neighbour in level.get_pathable_neighbours(current):
#             # if the neighbour has not been seen before
#             if all(neighbour not in group for group in [open_list, closed_list]):
#                 g_neighbour: float = g_scores[current] + 1
#                 g_scores[neighbour] = g_neighbour
#                 f_neighbour: float = heuristic(neighbour, end) + g_neighbour
#
#                 if f_neighbour < f_scores[neighbour]:
#                     f_scores[neighbour] = f_neighbour
#                     parents[neighbour] = current
#                     heapq.heappush(open_list, (f_neighbour, heap_entry_count, neighbour))
#                     heap_entry_count += 1
#
#         # finished processing current vertex. Add to closed list
#         closed_list.add(current)
#
#     return None

def a_star(start: "Tile", end: "Tile", level: "Level") -> Optional[List["Tile"]]:
    """
    Implementation of A* pathfinding algorithm (https://www.redblobgames.com/pathfinding/a-star/implementation.html).
    Returns a list of pathable connected tiles between the start and end tile arguments (from start -> end).
    Returns None if no path is found
    """
    heap_entry_count: int = 0  # variable to keep track of the order of objects entered into the heap
    open_list: heapq = [(0, heap_entry_count, start)]
    g_scores: Dict[Tile, float] = dict()
    # set g score of first tile to zero
    g_scores[start] = 0
    closed_list: Set = set()

    # keep track of preceding path
    parents: Dict[Tile, Optional[Tile]] = {start: None}

    while open_list:
        current: Tile
        _, __, current = heapq.heappop(open_list)

        # if the end tile is being processed stop the algorithm and return the best path
        if current == end:
            path: List[Tile] = []
            while current:
                path.append(current)
                current = parents[current]
            return path[::-1]  # reverse path so tiles are ordered from start -> end

        # process neighbours of current vertex
        for neighbour in level.get_pathable_neighbours(current):
            g_neighbour: float = g_scores[current] + 1
            if neighbour not in g_scores or g_neighbour < g_scores[neighbour]:
                g_scores[neighbour] = g_neighbour
                f_neighbour: float = heuristic(neighbour, end) + g_neighbour
                heapq.heappush(open_list, (f_neighbour, heap_entry_count, neighbour))
                heap_entry_count += 1
                parents[neighbour] = current

        # finished processing current vertex. Add to closed list
        closed_list.add(current)

    return None
