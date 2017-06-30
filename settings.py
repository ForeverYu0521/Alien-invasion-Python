#-*-coding:utf-8-*-
class Settings():

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (0, 0, 230)

        self.ship_speed_factor = 0.5
        self.ship_limit = 1
        
        #外星人设置
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 50
        #fleet_direction为1表示向右移，-1表示向左移
        self.fleet_direction = 1

        #加快游戏节奏设置
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

        #子弹属性设置
        self.bullet_speed_factor = 1
        self.bullet_width = 1200
        self.bullet_height = 15
        self.bullet_color = 230, 0, 0
        self.bullets_allowed = 5

    def initialize_dynamic_settings(self):
        #初始化随游戏进行而变化的设置
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        #fleet_direction为1表示向右，为-1表示向左
        self.fleet_direction = 1

    def increase_speed(self):
        #提高速度设置
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
