import pygame


class Navbar:
    def __init__(self, bg):
        self.x = 0
        self.y = 0
        self.w = 40
        self.h = 40
        self.bg = bg
        self.color = (60, 60, 60)
        self.isOpen = -1
        self.buffer = 60
        self.oH = 50
        self.font = pygame.font.SysFont('Verdana', 32)
        self.ofont = pygame.font.SysFont('Verdana', 24)

    def display(self, w, os):
        if self.isOpen == -1:
            pygame.draw.rect(w, self.bg, (0, 0, self.w, self.h))
            pygame.draw.line(w, self.color, (10, 10), (30, 10), 3)
            pygame.draw.line(w, self.color, (10, 16), (30, 16), 3)
            pygame.draw.line(w, self.color, (10, 22), (30, 22), 3)
        else:
            win_size = w.get_size()

            # Header
            pygame.draw.rect(w, (196, 89, 255), (5, 5, win_size[0]//4, 50), 0, 10)

            # X
            pygame.draw.line(w, (120, 33, 166), (win_size[0]//4 - self.w + 15, 15),
                             (win_size[0]//4 - self.w + 25, 25), 3)
            pygame.draw.line(w, (120, 33, 166), (win_size[0]//4 - self.w + 15, 25),
                             (win_size[0]//4 - self.w + 25, 15), 3)

            # Text
            text = self.font.render('Options', True, (120, 33, 166))
            w.blit(text, (20, 5))

            for i, o in enumerate(os):
                pygame.draw.rect(w, (224, 166, 255), (5, self.buffer + (self.oH + 3) * i, win_size[0]//4, self.oH), 0, 10)
                pygame.draw.rect(w, (196, 89, 255), (5, self.buffer + (self.oH + 3) * i, win_size[0]//4, self.oH), 3, 10)
                text = self.ofont.render(o, True, (120, 33, 166))

                w.blit(text, (win_size[0]//8 - text.get_size()[0]//2 + 5, self.buffer + 9 + (self.oH + 3) * i))

    def check_click(self, pos, w):
        if self.isOpen == -1:
            if self.x < pos[0] < self.x + self.w and self.y < pos[1] < self.y + self.h:
                return True
            else:
                return False
        else:
            win_size = w.get_size()
            if win_size[0]//4 - self.w < pos[0] < win_size[0]//4 and self.y < pos[1] < self.y + self.h:
                return True
            elif 5 < pos[0] < win_size[0]//4 and 5 < pos[1] < win_size[1] - 10:
                return "Check"
            else:
                return False

    def toggle(self):
        self.isOpen *= -1
