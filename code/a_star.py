import heapq
import math
import sys
from typing import TYPE_CHECKING, Tuple, List, Dict, Set, Optional
from level import Level


if TYPE_CHECKING:
    import pygame
    from tile import Tile


def heuristic(a: Tile, b: Tile) -> float:
    # get centre coords for the pygame.Rect objects of each tile
    a: Tuple[float, float] = a.rect.center
    b: Tuple[float, float] = b.rect.center
    # Manhattan distance between the centre points of the pygame.Rect objects of each tile
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def a_star(grid: List[Tile], start: Tile, end: Tile, level: Level) -> Optional[List[Tile]]:
    heap_entry_count: int = 0  # variable to keep track of the order of objects entered into the heap
    heap: heapq = [(0, heap_entry_count, start)]
    g_scores: Dict[Tile, float] = {tile: sys.maxsize for tile in grid}
    # set g score of first tile to zero
    g_scores[start] = 0
    f_scores: Dict[Tile, float] = {tile: sys.maxsize for tile in grid}
    f_scores[start] = heuristic(start, end)
    open_list: Set = set([start])
    closed_list: Set = set()

    # keep track of preceding path
    parents: Dict[Tile, Optional[Tile]] = {start: None}

    while heap:
        f: float
        current: Tile
        f, _, current = heapq.heappop(heap)

        # if the end tile is being process stop the algorithm and return the best path
        if current == end:
            path: List[Tile] = []
            while current:
                path.append(current)
                current = parents[current]
            return path

        # process neighbours of current vertex
        for neighbour in level.get_pathable_neighbours(current):
            if all(neighbour not in group for group in [open_list, closed_list]):
                open_list.add(neighbour)

            g_neighbour: float = g_scores[current] + 1
            f_neighbour: float = heuristic(neighbour, end) + g_neighbour

            if f_neighbour < f_scores[neighbour]:
                f_scores[neighbour] = f_neighbour
                parents[neighbour] = current
                heapq.heappush(heap, (f_neighbour, heap_entry_count, neighbour))
                heap_entry_count += 1

        # finished processing current vertex remove from open list and add to closed list
        closed_list.add(open_list.remove(current))

    return None
