import pygame as pg
import background
import menu, constants as con
import player as p

def main():
    pg.init()
    bt_new_game = menu.Button('Nowa Gra', 0, action=None)
    bt_read_game = menu.Button('Wczytaj Grę', 1, action=None)
    bt_exit = menu.Button('Wyjdź z gry', 2, lambda: pg.event.post(pg.event.Event(pg.QUIT)))
    bts = [bt_new_game, bt_read_game, bt_exit]
    box = menu.Box(len(bts))
    bg = background.Background(con.s_width, con.s_height)
    all_sprites = pg.sprite.Group((bg))
    dt = 0
    player = p.Player()
    clock = pg.time.Clock()
    run = True
    while run:
        frame_rate = 1000 / clock.tick(60)
        dt = frame_rate / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        con.screen.fill((0, 255, 0))
        all_sprites.draw(con.screen)
        box.draw(con.screen)
        for bt in bts:
            bt.handle_event(event)
            bt.draw(con.screen)
        pg.display.flip()
    pg.quit()

if __name__ == '__main__': main()