import os
import sys
import pygame as pg
import random

WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    # 背景画像の読み込み
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    # キャラクターの読み込み
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    # 爆弾となる赤色の円を描画
    bom_img = pg.Surface((100, 100))
    bom_img.set_colorkey((0, 0, 0))
    pg.draw.circle(bom_img, (255, 0, 0), (50, 50), 10)
    bom_rect = bom_img.get_rect()
    bom_rect.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    bom_vx = 5
    bom_vy = 5

    clock = pg.time.Clock()
    tmr = 0

    # キー入力による移動量
    movekey:dict ={ 
        "pg.K_UP": (0,-5),
        "pg.K_DOWN": (0,+5),
        "pg.K_LEFT": (-5,0),
        "pg.K_RIGHT": (+5,0)
    }

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 
        # 爆弾の描画
        screen.blit(bom_img, bom_rect)

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        #print(movekey.items())
        for k ,v in movekey.items():
            if key_lst[eval(k)]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]

        kk_rct.move_ip(sum_mv)
        # 爆弾の移動
        bom_rect.move_ip(bom_vx, bom_vy)
        screen.blit(kk_img, kk_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
