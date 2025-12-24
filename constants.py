import pygame as pg

pg.init()

s_width, s_height = pg.display.get_desktop_sizes()[0]
screen = pg.display.set_mode((s_width, s_height))