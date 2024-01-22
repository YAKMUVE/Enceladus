import random


class Maze:  # класс лабиринта
    def __init__(self, size) -> None:
        self.size = size
        self.generate_new()

    def link(self, cell, links):  # проверка связей
        if self.vis[cell[0]][cell[1]]:
            return True
        self.vis[cell[0]][cell[1]] = True
        for l in links[cell[0]][cell[1]]:
            self.link(l, links)

    def link_checker(self, cells, links):  # создание и проверка связей
        x1, y1, x2, y2 = cells
        self.vis = []
        for i in range(self.size[0]):
            self.vis.append([])
            for j in range(self.size[1]):
                self.vis[i].append(False)

        self.link((x1, y1), links)

        if self.vis[x2][y2]:
            return True
        return False

    def generate_new(self):  # построение связей
        todo = []  # класс лабиринта
        doors = []  # проходы
        links = []  # связки путей
        for i in range(self.size[0]):
            links.append([])
            for j in range(self.size[1]):
                links[i].append([])
                todo.append((i, j))

        while len(todo) > 0:
            x, y = random.choice(todo)
            w = []
            if x - 1 >= 0:
                if not (x - 1, y, x, y) in doors:
                    w.append((x - 1, y, x, y))
            if x + 1 < self.size[0]:
                if not (x, y, x + 1, y) in doors:
                    w.append((x, y, x + 1, y))
            if y - 1 >= 0:
                if not (x, y - 1, x, y) in doors:
                    w.append((x, y - 1, x, y))
            if y + 1 < self.size[1]:
                if not (x, y, x, y + 1) in doors:
                    w.append((x, y, x, y + 1))

            random.shuffle(w)

            n_linked = 0
            for p in w:
                if not self.link_checker(p, links):
                    n_linked += 1
                    if n_linked == 1:
                        x1, y1, x2, y2 = p
                        doors.append(p)
                        links[x1][y1].append([x2, y2])
                        links[x2][y2].append([x1, y1])

            if n_linked <= 1:
                todo.remove((x, y))
        self.doors = doors
