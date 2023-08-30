import pygame


class LoadView:
    def __init__(self):
        self.screenw = screenw
        self.screenh = screenh
        self.w = screenw // 6 * 2
        self.h = screenh // 6 * 2
        self.y = screenh // 6
        self.x = screenw // 6 * 2
        self.name_font = pygame.font.SysFont('Verdana', 20)
        self.new_font = pygame.font.SysFont('Verdana', 24)

        self.chars = "1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&*()QWERTYUIOPASDFGHJKLZXCVBNM .,;:[]{}?-_=+"

        self.nameh = 40
        self.is_name_active = False

        self.new_proj_name = ""