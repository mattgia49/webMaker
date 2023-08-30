import pygame
import time

from navbar import Navbar
from project import Project
from NewProj import NewProj
from term import Term
from loadFile import LoadFile

pygame.init()

win = pygame.display.set_mode((1000, 800))

crashed = False
clock = pygame.time.Clock()

backgroundColor = (180, 180, 180)

options = ["New Project", "Load Project", "Save Project"]

nb = Navbar(backgroundColor)
new_proj = NewProj(win.get_size()[0], win.get_size()[1], "Create")
load_proj = NewProj(win.get_size()[0], win.get_size()[1], "Load")
save_proj = NewProj(win.get_size()[0], win.get_size()[1], "Save")
curr_proj = None

editing = False
moving = False
drag_term = -1
up_term = -1
down_term = -1
connecting = False
curr_view = "main"

add_button_x = 0
add_button_y = 0
add_button_w = 0
add_button_h = 0

deleting = False
pos = 0
title_font = pygame.font.SysFont('Verdana', 24)

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if curr_proj is not None:
                if event.dict['button'] == 3:
                    moving = True
                    drag_term = curr_proj.check_terms_sel(pos)
                elif event.dict['button'] == 1:
                    down_term = curr_proj.check_terms_sel(pos)
                    if curr_proj.is_term_act(down_term):
                        connecting = True

        elif event.type == pygame.MOUSEMOTION:
            pos = event.dict['pos']
            if drag_term != -1:
                if not curr_proj.is_term_act(drag_term):
                    curr_proj.move_term(drag_term, event.dict['rel'])
            else:
                if curr_proj is not None and moving:
                    curr_proj.move_terms(event.dict['rel'])
        elif event.type == pygame.MOUSEBUTTONUP:
            if curr_view == "main":
                clicked = nb.check_click(pos, win)
                if clicked == "Check":
                    sel_proj = (pos[1] - 45) // 60
                    if sel_proj < len(options) and sel_proj != -1:
                        curr_view = options[sel_proj]
                else:
                    if clicked:
                        nb.toggle()
            elif curr_view == "New Project" or curr_view == "Load Project" or curr_view == "Save Project":
                if curr_view == "New Project":
                    curr_box = new_proj
                elif curr_view == "Load Project":
                    curr_box = load_proj
                else:
                    curr_box = save_proj

                clicked = curr_box.check_click(pos)
                if clicked == "Close":
                    curr_view = "main"
                elif clicked == "Name":
                    curr_box.activate_name()
                elif clicked == "Create":
                    if curr_view == "New Project":
                        new_name = curr_box.get_name()
                        curr_proj = Project(new_name)
                    elif curr_view == "Load Project":
                        curr_proj = LoadFile(curr_box.get_name() + ".json").get_loaded()
                    else:
                        curr_proj.save_to_file(curr_box.get_name())
                    curr_box.deactivate_name()
                    curr_view = "main"
                    nb.toggle()
                else:
                    new_proj.deactivate_name()


            if curr_proj is not None:
                up_term = curr_proj.check_terms_sel(pos)
                if event.dict['button'] == 3:
                    if up_term != -1 and curr_proj.is_term_act(up_term):
                        editing = True
                        curr_proj.edit_term(up_term, pos)
                elif add_button_x < pos[0] < add_button_x + add_button_w and add_button_y < pos[1] < add_button_y + add_button_h:
                    curr_proj.add_term(Term(curr_proj.get_new_term_id(), win.get_size()[0]//2 - 100, win.get_size()[1]//2 - 40))
                elif down_term == up_term and event.dict['button'] == 1:
                    curr_proj.toggle_term(up_term)
                    editing = False
                if connecting:
                    if down_term != up_term and up_term != -1:
                        curr_proj.create_connection(down_term, up_term)
                connecting = False

            up_term = -1
            down_term = -1
            drag_term = -1
            moving = False
        elif event.type == pygame.KEYDOWN:
            if editing:
                if event.dict["key"] == 8:
                    curr_proj.add_term_char(event)
                    deleting = True
                    start_del = time.time()
        elif event.type == pygame.KEYUP:
            deleting = False
            if curr_view == "New Project" or curr_view == "Load Project" or curr_view == "Save Project":
                if curr_view == "New Project":
                    curr_box = new_proj
                elif curr_view == "Load Project":
                    curr_box = load_proj
                else:
                    curr_box = save_proj

                curr_box.add_char(event)
            elif curr_view == "main":
                if curr_proj is not None:
                    if event.dict['key'] == 8 and not editing:
                        curr_proj.del_term()
                    if event.dict['key'] != 8 and editing:
                        curr_proj.add_term_char(event)

    win.fill(backgroundColor)
    nb.display(win, options)



    if deleting:
        if time.time() - start_del > .75:
            curr_proj.del_term_char()

    if connecting:
        pygame.draw.line(win, (0, 0, 0), (pos[0], pos[1]), curr_proj.get_term_by_id(down_term).getcenter(), 3)

    if curr_proj is not None:
        title = title_font.render(curr_proj.get_name(), True, (120, 33, 166))
        pygame.draw.rect(win, (224, 166, 255),
                         (10, win.get_size()[1] - 50, title.get_size()[0] + 20, title.get_size()[1] + 10), 0, 10)
        pygame.draw.rect(win, (196, 89, 255),
                         (10, win.get_size()[1] - 50, title.get_size()[0] + 20, title.get_size()[1] + 10), 3, 10)
        win.blit(title, (20, win.get_size()[1] - 45))

        pygame.draw.rect(win, (224, 166, 255), (
        40 + title.get_size()[0], win.get_size()[1] - 50, title.get_size()[1] + 10, title.get_size()[1] + 10), 0, 10)
        pygame.draw.rect(win, (196, 89, 255), (
        40 + title.get_size()[0], win.get_size()[1] - 50, title.get_size()[1] + 10, title.get_size()[1] + 10), 3, 10)
        add_button_x = 40 + title.get_size()[0]
        add_button_y = win.get_size()[1] - 50
        add_button_w = title.get_size()[1] + 10
        add_button_h = add_button_w

        pygame.draw.line(win, (120, 33, 166),
                         (add_button_x + add_button_w // 2, add_button_y + 11),
                         (add_button_x + add_button_w // 2, add_button_y + add_button_w - 11), 3)
        pygame.draw.line(win, (120, 33, 166),
                         (add_button_x + 11, add_button_y + add_button_h // 2),
                         (add_button_x + add_button_w - 11, add_button_y + add_button_h // 2), 3)
        curr_proj.show(win)

    if curr_view == "main":
        if curr_proj is not None:
            curr_proj.show(win)
    elif curr_view == "New Project":
        new_proj.show(win)
    elif curr_view == "Save Project":
        save_proj.show(win)
    elif curr_view == "Load Project":
        load_proj.show(win)

    pygame.display.update()
    clock.tick(60)
