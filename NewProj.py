import pygame
import time


class NewProj:
    def __init__(self, screenw, screenh, button):
        self.screenw = screenw
        self.screenh = screenh
        self.w = screenw//6 * 2
        self.h = screenh//6 * 2
        self.y = screenh//6
        self.x = screenw//6 * 2
        self.name_font = pygame.font.SysFont('Verdana', 20)
        self.new_font = pygame.font.SysFont('Verdana', 24)

        self.chars = "1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&*()QWERTYUIOPASDFGHJKLZXCVBNM .,;:[]{}?-_=+"

        self.nameh = 40
        self.is_name_active = False
        self.button = button
        self.new_proj_name = ""

    def show(self, w):
        s = pygame.Surface((self.screenw, self.screenh))
        s.set_alpha(128)
        s.fill((0, 0, 0))
        w.blit(s, (0, 0))
        pygame.draw.rect(w, (224, 166, 255), (self.x, self.y, self.w, self.h), 0, 10)
        pygame.draw.rect(w, (196, 89, 255), (self.x, self.y, self.w, self.h), 3, 10)
        pygame.draw.line(w, (120, 33, 166), (self.x + self.w - 25, self.y + 10), (self.x + self.w - 10, self.y + 25), 3)
        pygame.draw.line(w, (120, 33, 166), (self.x + self.w - 25, self.y + 25), (self.x + self.w - 10, self.y + 10), 3)

        pygame.draw.rect(w, (230, 230, 230), (self.x + self.w//8, self.y + self.h//2, self.w//8 * 6, 40), 0, 10)
        pygame.draw.rect(w, (196, 89, 255), (self.x + self.w//8, self.y + self.h//2, self.w//8 * 6, 40), 3, 10)
        text = self.name_font.render(self.new_proj_name, True, (70, 70, 70))
        w.blit(text, (self.x + self.w // 8 + 10, self.y + self.h // 2 + self.nameh // 2 - text.get_size()[1] // 2))

        if self.is_name_active:

            if time.time() % 1 > 0.5:
                pygame.draw.line(w,
                                 (70, 70, 70),
                                 (self.x + self.w//8 + 12 + text.get_size()[0], self.y + self.h//2 + 10),
                                 (self.x + self.w//8 + 12 + text.get_size()[0], self.y + self.h//2 + text.get_size()[1] + 5),
                                 2)

        pygame.draw.rect(w, (230, 230, 230), (self.x + self.w // 10 * 3, self.y + self.h // 4 * 3, self.w // 10 * 4, 40), 0, 10)
        pygame.draw.rect(w, (196, 89, 255), (self.x + self.w // 10 * 3, self.y + self.h // 4 * 3, self.w // 10 * 4, 40), 3, 10)
        text = self.new_font.render(self.button, True, (120, 33, 166))

        w.blit(text, (self.x + self.w // 10 * 3 + self.w // 20 * 4 - text.get_size()[0]//2, self.y + self.h // 4 * 3 + 20 - text.get_size()[1]//2))

    def check_click(self, pos):
        if self.x + self.w - 25 < pos[0] < self.x + self.w - 10 and self.y + 10 < pos[1] < self.y + 25:
            self.is_name_active = False
            self.new_proj_name = ""
            return "Close"
        elif self.x + self.w//8 < pos[0] < self.x + self.w//8 * 7 and self.y + self.h//2 < pos[1] < self.y + self.h//2 + self.nameh:
            return "Name"
        elif self.x + self.w // 10 * 3 < pos[0] < self.x + self.w // 10 * 3 + self.w // 10 * 4 and self.y + self.h // 4 * 3 < pos[1] < self.y + self.h // 4 * 3 + 40:
            return "Create"
        else:
            return False

    def activate_name(self):
        self.is_name_active = True

    def deactivate_name(self):
        self.is_name_active = False

    def add_char(self, e):
        if self.is_name_active:
            if e.dict['unicode'] in self.chars:
                self.new_proj_name = self.new_proj_name + e.dict['unicode']
            elif e.dict['key'] == 8:
                self.new_proj_name = self.new_proj_name[:-1]

    def get_name(self):
        return self.new_proj_name
