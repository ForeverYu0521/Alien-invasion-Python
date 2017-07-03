#-*-coding:utf-8-*-
import sys
import random

from time import sleep
import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets):

    if event.key == pygame.K_q:
        sys.exit()

    elif event.key == pygame.K_RIGHT:
        ship.moving_right = True

    elif event.key == pygame.K_LEFT:
        ship.moving_left = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    
    #当p按下时，游戏开始
    elif event.key == pygame.K_p and not stats.game_active:
        Play_game(ai_settings, screen, stats, sb, ship, aliens, bullets)


def fire_bullet(ai_settings, screen, ship, bullets):

    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):

    if event.key == pygame.K_RIGHT:
        ship.moving_right = False

    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
                    aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, 
        aliens, bullets, mouse_x, mouse_y):
    #玩家单击play按钮时开始新游戏
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)

    if button_clicked and not stats.game_active:
        #重置游戏设置
        Play_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
        
def Play_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
        ai_settings.initialize_dynamic_settings()

        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #隐藏光标
        pygame.mouse.set_visible(False)

        #重置游戏统计信息
        stats.reset_stats()
        stats.game_active = True

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并让飞船居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button, ItemBullet):

    screen.fill(ai_settings.bg_color)

    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    
    aliens.draw(screen)

    ItemBullet.blitme()

    nums_bullets(ai_settings, screen, bullets)

    sb.show_score()

    sb.prep_ships()

    if not stats.game_active:
        play_button.draw_button()

    pygame.display.flip()

def get_number_rows(ai_settings, ship_height, alien_height):
    #计算屏幕可容纳多少行外星人
    available_space_y = (ai_settings.screen_height - (3 * alien_height)
                          - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def get_number_aliens_x(ai_settings, alien_width):
    
    #计算每行容纳多少外星人
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = 2 * alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = 2 * alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    #创建外星人群
    #创建一个外星人，并计算一行可容纳多少个外星人
    #外星人间距为外星人宽度
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, 
            alien.rect.height * 3)

    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #创建一个外星人并将其加入当前行
            create_alien(ai_settings, screen, aliens, alien_number, 
                    row_number)

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, 
        bullets):
    #更新子弹的位置，并删除已经消失的子弹
    bullets.update()
        
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
   #检查是否诞生了最高分
   if stats.score > stats.high_score:
       stats.high_score = stats.score
       sb.prep_high_score()

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):

    #记录碰撞发生前的外星人数目
    pre_numbers = len(aliens)

    #检查子弹是否击中了外星人，如果是，就删除相应的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True) 
    
    if collisions:
        scores = ai_settings.alien_points * (pre_numbers - len(aliens))
        stats.score += scores
        sb.prep_score()
        
        #检查最高分
        check_high_score(stats, sb)

    if len(aliens) == 0: 
        bullets.empty()
        ai_settings.increase_speed()

        #提高等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)
def nums_bullets(ai_settings, screen, bullets):
    #显示剩余子弹的数目
    nums = ai_settings.bullets_allowed - len(bullets)    
    my_font = pygame.font.SysFont("arial", 32)
    nums_bullets_surface = my_font.render(str(nums), True, (0, 0, 0), 
            ai_settings.bg_color)
    nums_bullets_rect = nums_bullets_surface.get_rect()
    nums_bullets_rect.top = 60
    screen.blit(nums_bullets_surface,nums_bullets_rect)

def check_fleet_edges(ai_settings, aliens):
    #有外星人到达边缘时采取相应措施
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    #将整群外星人下移，并改变方向
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    #响应被外星人撞到的飞船
    #将ships_left减一
    if stats.ships_left > 0:
        stats.ships_left -= 1

        #更新记分牌
        sb.prep_ships()

        #清空外星人和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人，并将飞船放在屏幕低端中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        #暂停
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, stats, screen, sb, ship ,aliens, bullets):
    #检查是否有外星人到达屏幕低端
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            #像飞船被撞到一样处理
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    
    #更新外星人群中所有外星人的位置
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #检测外星人和飞船之间的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings, stats, screen, sb, ship, aliens, bullets)

def update_itembullet(ai_settings, screen, ship, ItemBullet, aliens):
    if not ItemBullet.bullet_flag:
        number = random.randint(0, ai_settings.ItemBullteDropFre)
        if number == 1:
            ItemBullet.rect.x = random.randint(0,120) * 10 
            ItemBullet.bullet_flag = True

    screen_rect = screen.get_rect()
    if ItemBullet.recty >= screen_rect.bottom:
        Item_Init(ItemBullet)
    if pygame.sprite.collide_rect(ItemBullet, ship):
        bullets_change(ai_settings)
        Item_Init(ItemBullet)
    ItemBullet.draw()
    
def Item_Init(ItemBullet):
    #物品碰撞和消失时
    ItemBullet.bullet_flag = False
    ItemBullet.recty = float(-1 * ItemBullet.rect.height)
    ItemBullet.rect.y = -1 * ItemBullet.rect.height

def bullets_change(ai_settings):
   #增加子弹的宽度
    ai_settings.bullet_width += ai_settings.bullet_increase
