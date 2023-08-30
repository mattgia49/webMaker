import pygame
import time


class Term:
    def __init__(self, i, x, y):
        self.id = i
        self.names = [""]
        self.lines = [""]
        self.color = (230, 230, 230)
        self.border = (0, 0, 0)
        self.nfont = pygame.font.SysFont('Verdana', 20)
        self.basenh = 25
        self.dfont = pygame.font.SysFont('Verdana', 12)
        self.basedh = 15
        self.dh = 0
        self.x = x
        self.y = y
        self.w = 200
        self.h = 80
        self.active = False
        self.edit_title = False
        self.edit_desc = False
        self.chars = "1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&*()QWERTYUIOPASDFGHJKLZXCVBNM .,;:[]{}?-_=+"

    def set_names(self, ns):
        self.names = ns

    def set_lines(self, ls):
        self.lines = ls

    def get_json(self):
        return {
            "id": self.id,
            "names": self.names,
            "desc": self.lines,
            "color": self.color,
            "x": self.x,
            "y": self.y
        }
    def display(self, w):

        self.h = (self.basenh * len(self.names)) + 30 + (self.basedh * len(self.lines))
        pygame.draw.rect(w, self.color, (self.x, self.y, self.w, self.h), 0, 10)
        pygame.draw.rect(w, self.border, (self.x, self.y, self.w, self.h), 3, 10)
        pygame.draw.line(w, (70, 70, 70), (self.x + 10, self.y + (self.basedh + 10) * len(self.names) + 10), (self.x + self.w - 11, self.y + (self.basedh + 10) * len(self.names) + 10), 2)

        nameh = 0
        for namei, n in enumerate(self.names):
            name = self.nfont.render(n, True, (0, 0, 0))
            namesize = name.get_size()
            nameh += namesize[1]
            w.blit(name, (self.x + self.w // 2 - namesize[0] // 2, self.y + 10 + (namei * namesize[1])))

        desch = 0
        for linei, line in enumerate(self.lines):
            desc = self.dfont.render(line, True, (0, 0, 0))
            descsize = desc.get_size()
            desch += descsize[1]
            w.blit(desc, (self.x + 10, self.y + (self.basenh * len(self.names)) + 15 + (linei * descsize[1])))

        if self.edit_title:
            if time.time() % 1 > 0.5:
                pygame.draw.line(w,
                                 (70, 70, 70),
                                 (self.x + self.w // 2 + namesize[0] // 2 + 2, self.y + 10 + (self.basenh * (len(self.names) - 1))),
                                 (self.x + self.w // 2 + namesize[0] // 2 + 2, self.y + 7 + + (self.basenh * (len(self.names)))),
                                 2)
        elif self.edit_desc:
            if time.time() % 1 > 0.5:
                pygame.draw.line(w,
                                 (70, 70, 70),
                                 (self.x + descsize[0] + 11,
                                  self.y + namesize[1] + 15 + (linei * descsize[1])),
                                 (self.x + descsize[0] + 11,
                                  self.y + namesize[1] + 15 + ((linei + 1) * descsize[1])),
                                 2)

    def check_sel(self, pos):
        if self.x < pos[0] < self.x + self.w and self.y < pos[1] < self.y + self.h:
            return self.id
        else:
            return -1

    def isId(self, check):
        return check == self.id

    def movePos(self, rel):
        self.x += rel[0]
        self.y += rel[1]

    def getcenter(self):
        return self.x + self.w//2, self.y + self.h//2

    def is_active(self):
        return self.active

    def toggle(self):
        if self.active:
            self.active = False
            self.border = (0, 0, 0)
            self.edit_title = False
            self.edit_desc = False
        else:
            self.active = True
            self.border = (100, 240, 100)

    def set_active(self):
        self.active = True
        self.border = (100, 240, 100)

    def set_not_active(self):
        self.active = False
        self.border = (0, 0, 0)
        self.edit_title = False
        self.edit_desc = False

    def get_id(self):
        return self.id

    def edit(self, pos):
        if pos[1] < self.y + self.h // 2:
            self.edit_title = True
            self.edit_desc = False
        else:
            self.edit_desc = True
            self.edit_title = False

    def stop_edit(self):
        self.edit_title = False
        self.edit_desc = False

    def del_char(self):
        if self.edit_title:
            print(len(self.names))

            if len(self.names[len(self.names) - 1]) == 0:
                print(len(self.names))
                if len(self.names) > 1:
                    self.names.pop()
            else:
                self.names[len(self.names) - 1] = self.names[len(self.names) - 1][:-1]
        else:
            if len(self.lines[len(self.lines) - 1]) == 0:
                if len(self.lines) > 1:
                    self.lines.pop()
            else:
                self.lines[len(self.lines) - 1] = self.lines[len(self.lines) - 1][:-1]

    def add_char(self, e):
        if e.dict['key'] != 8:
            c = e.dict['unicode']
            if c in self.chars:
                ind = -1
                if self.edit_title:
                    text = self.nfont.render(self.names[len(self.names) - 1], True, (0, 0, 0))
                    if text.get_size()[0] > self.w - 20:
                        for spacei, char in enumerate(self.names[len(self.names) - 1]):
                            if char == " ":
                                ind = spacei
                        if ind == -1:
                            self.names.append(c)
                        else:
                            self.names.append(self.names[len(self.names) - 1][ind + 1:] + c)
                            self.names[len(self.names) - 2] = self.names[len(self.names) - 2][:ind]

                    else:
                        self.names[len(self.names) - 1] += c
                else:
                    text = self.dfont.render(self.lines[len(self.lines) - 1], True, (0, 0, 0))
                    if text.get_size()[0] > self.w - 20:
                        for spacei, char in enumerate(self.lines[len(self.lines) - 1]):
                            if char == " ":
                                ind = spacei
                        if ind == -1:
                            self.lines.append(c)
                        else:
                            self.lines.append(self.lines[len(self.lines) - 1][ind + 1:] + c)
                            self.lines[len(self.lines) - 2] = self.lines[len(self.lines) - 2][:ind]

                    else:
                        self.lines[len(self.lines) - 1] += c

        else:
            if self.edit_title:
                self.del_char()
            else:
                self.del_char()

    def change_color(self, color):
        self.color = color
