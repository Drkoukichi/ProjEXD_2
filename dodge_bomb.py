import os
import sys
import pygame as pg
import random
import time

WIDTH, HEIGHT = 1600, 900
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def change_rotation():
    """
    概要：キャラクターの向きを押したキーによって変更する
    引数：なし
    戻り値：なし
    """
    key_lst = pg.key.get_pressed()
    if key_lst[pg.K_UP]:
        pass

bomsize = 10

def change_bom_size(tmr:int,bom:pg.Surface):
    """
    概要: 爆弾のサイズを変更する
    引数: tmr: 経過時間  bom: 爆弾の画像
    戻り値: なし
    """

    #
    #global bomsize
    #if tmr % 10 == 0:
    #    bom_img = bom
    #    bomsize += 10
    #    bom_img = pg.Surface((100, 100))
    #    bom_img.set_colorkey((0, 0, 0))
    #    pg.draw.circle(bom_img, (255, 0, 0), (50, 50), bomsize)
    #print(bom_img)
    #return bom_img
    return 0

def trans_chara(button:str, chara:pg.Surface):
    """
    概要: キャラクターの向きを変更する
    引数: button: 押されたキー, chara: キャラクターの画像
    戻り値: キャラクターの画像
    """
    return 0


def homing_bom(pos:tuple, bom_pos:tuple):
    """
    概要: 定期的に爆弾がキャラクターに向かって移動する
    引数: キャラクターの位置、爆弾の位置
    返り値: 爆弾のdx,dy
    """
    # 二点の座標の差を求める
    dx = pos[0] - bom_pos[0]
    dy = pos[1] - bom_pos[1]
    # 二点間の距離を求める
    diff = (dx**2 + dy**2)**0.5

    if diff <= 300 :
        return [0,0]

    x = dx / diff * 5
    y = dy / diff * 5
    return [x, y]

def gameover(screen:pg.Surface):
    """
    概要: ゲームオーバー画面を表示する
    引数: なし
    戻り値: なし
    """
    # 画面を黒くする
    screen.fill((0, 0, 0))
    # フォントの設定
    font = pg.font.Font(None, 100)
    # テキストの描画
    text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(text, [WIDTH/2-150, HEIGHT/2])
    # ゲームオーバーの両方にキャラクターを追加
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    screen.blit(kk_img, kk_rct)
    kk_rct.center = 700, 400
    screen.blit(kk_img, kk_rct)

    # 画面を更新して5秒待つ
    pg.display.update()
    time.sleep(5)

def check_wall_collision(pos:tuple):
    """
    概要: 画面端に到達したかどうかを判定する
    引数: pos: 対象の位置
    戻り値: 対象が左右で到達していたら1, 上下で到達していたら2, それ以外は0
    """
    x, y = pos
    """
    if x < 0 or x > 1500 :
        return 1
    elif y < 0 or y > 750 :
        return 2
    else:
        return 0
    """
    
    if x < 0 or x > WIDTH :
        return 1
    elif y < 0 or y > HEIGHT :
        return 2
    else:
        return 0
    
def colision_check(rect1:pg.Rect, rect2:pg.Rect):
    """
    概要: 2つの矩形が重なっているかどうかを判定する
    引数: rect1, rect2
    戻り値: 重なっていたらTrue, それ以外はFalse
    """
    #return rect1.colliderect(rect2)
    diff = ((rect1.x - rect2.x)**2 + (rect1.y - rect2.y)**2)**0.5
    #print (diff)
    if diff < 50:
        return True
    else:
        return False


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
    #print(type(bom_rect))

    # ゲームオーバーのフラグ
    gameover_f = False

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
        #print(kk_rct.topleft)

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

        # キャラクターが画面端に到達したかどうかを判定
        colision = check_wall_collision(kk_rct.topleft)
        if colision == 1 or colision == 2:
            move_rev = [-10 * sum_mv[0], -5 * sum_mv[1]]
            kk_rct.move_ip(move_rev)
            continue

        # 爆弾が画面端に到達したかどうかを判定
        colision = check_wall_collision(bom_rect.topleft)
        if colision == 1:
            bom_vx *= -1
        elif colision == 2:
            bom_vy *= -1

        # キャラクターの移動
        kk_rct.move_ip(sum_mv)
        # 爆弾の移動
        bom_rect.move_ip(bom_vx, bom_vy)
        screen.blit(kk_img, kk_rct)
        # 爆弾とキャラクターが重なっているかどうかを判定
        if colision_check(kk_rct, bom_rect):
            print("Game Over")
            #gameoverフラグを立てる
            break

        # 5フレームに1回爆弾の向きを変える
        
        if tmr % 10 == 0:
            new_move = homing_bom(kk_rct.topleft, bom_rect.topleft)
            if new_move != [0, 0]:
                bom_vx = new_move[0]
                bom_vy = new_move[1]

        # 爆弾のサイズを変更
        #bom_img = change_bom_size(tmr, bom_img)
        
        pg.display.update()
        tmr += 1
        clock.tick(50)

    gameover(screen)




if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
