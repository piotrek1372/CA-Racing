import pygame as pg
import background
from menu import *
from constants import *
import player as p
from load_data import Data

def main():
    pg.init()
    data_loader = Data()
    game_db = data_loader.load_saves_template('game_data.json')
    player_save = data_loader.load_saves_template('player_state.json')
    if game_db and player_save:
        print("Dane wczytane poprawnie!")
    bt_new_game = Button('Nowa Gra', 0, action=None)
    bt_read_game = Button('Wczytaj Grę', 1, action=None)
    bt_exit = Button('Wyjdź z gry', 2, lambda: pg.event.post(pg.event.Event(pg.QUIT)))
    bts = [bt_new_game, bt_read_game, bt_exit]
    box = Box(len(bts))
    bg = background.Background(SCREEN_WIDTH, SCREEN_HEIGHT)
    all_sprites = pg.sprite.Group((bg))
    dt = 0
    clock = pg.time.Clock()
    run = True
    while run:
        dt = clock.tick(FPS) / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        SCREEN.fill((0, 255, 0))
        all_sprites.draw(SCREEN)
        box.draw(SCREEN)
        for bt in bts:
            bt.handle_event(event)
            bt.draw(SCREEN)
        pg.display.flip()
    pg.quit()

if __name__ == '__main__': main()