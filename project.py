import pygame
import json


class Project:
    def __init__(self, name):
        self.name = name
        self.terms = []
        self.connections = []
        self.navH = 50
        self.font = pygame.font.SysFont('Verdana', 24)
        self.desc_font = pygame.font.SysFont('Verdana', 20)
        self.buffer = 60
        self.term_id = 0

    def get_term_amt(self):
        return len(self.terms)

    def save_to_file(self, file_name):
        term_maps = []
        for t in self.terms:
            term_maps.append(t.get_json())

        connection_lists = []
        for c in self.connections:
            connection_lists.append([c[0].get_id(), c[1].get_id()])

        file_contents = {
            "name": self.name,
            "terms": term_maps,
            "connections": connection_lists,
            "term id": self.term_id
        }

        with open(file_name + ".json", "w") as outfile:
            outfile.write(json.dumps(file_contents, indent=2))

    def set_term_id(self, ti):
        self.term_id = ti

    def get_name(self):
        return self.name

    def add_term(self, t):
        self.terms.append(t)

    def show(self, w):
        for c in self.connections:
            pygame.draw.line(w, (0, 0, 0), c[0].getcenter(), c[1].getcenter(), 3)
        for t in self.terms:
            t.display(w)

    def check_terms_sel(self, pos):
        sel_id = -1
        for t in self.terms:
            curr_id = t.check_sel(pos)
            if curr_id > sel_id:
                sel_id = curr_id

        return sel_id

    def move_term(self, i, rel):
        for t in self.terms:
            if t.isId(i):
                t.movePos(rel)

    def move_terms(self, rel):
        for t in self.terms:
            t.movePos(rel)

    def __str__(self):
        return self.name

    def toggle_term(self, i):
        for t in self.terms:
            if t.isId(i):
                t.toggle()
            else:
                t.set_not_active()

    def is_term_act(self, i):
        for t in self.terms:
            if t.isId(i):
                return t.is_active()

    def create_connection(self, t1, t2):
        for t in self.terms:
            if t.isId(t1):
                t1 = t
            if t.isId(t2):
                t2 = t

        self.connections.append([t1, t2])

    def del_term(self):
        for it, t in enumerate(self.terms):
            if t.is_active():
                self.terms.pop(it)
                for ic, c in enumerate(self.connections):
                    if t.get_id() == c[0].get_id() or t.get_id() == c[1].get_id():
                        self.connections.pop(ic)

    def get_new_term_id(self):
        self.term_id += 1
        return self.term_id

    def edit_term(self, i, pos):
        for t in self.terms:
            if t.isId(i):
                t.edit(pos)

    def add_term_char(self, c):
        for t in self.terms:
            if t.is_active():
                t.add_char(c)

    def del_term_char(self):
        for t in self.terms:
            if t.is_active():
                t.del_char()

    def get_term_by_id(self, i):
        for t in self.terms:
            if t.get_id() == i:
                return t
