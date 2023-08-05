from collections import deque
from typing import Any, Callable, Set, TypeVar

from graph.graph import Graph


T = TypeVar('T')

def dfs(graph: Graph, vertex: T, func: Callable[[Graph], Any], sort_key: Callable[[T], T]=lambda val: val):
    visited = set()
    _dfs(graph, vertex, visited, func, sort_key)

def _dfs(graph: Graph, vertex: T, visited: Set, func: Callable[[Graph], None], sort_key: Callable[[T], T]=lambda val: val):
    func(vertex)
    visited.add(vertex)
    for neighbor in sorted(graph[vertex], key=sort_key):
        if neighbor not in visited:
            _dfs(graph, neighbor, visited, func, sort_key)


def bfs(graph: Graph, vertex: T, func: Callable[[Graph], Any], sort_key: Callable[[T], T]=lambda val: val):
    queue = deque()
    queue.append(vertex)
    visited = set()
    visited.add(vertex)
    while len(queue) > 0:
        v = queue.popleft()
        func(v)
        for neighbor in sorted(graph[v], key=sort_key):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
