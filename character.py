

class Character:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.unit_img = None
        self.atk_img = None
        self.atk_spd = 0
        self.mov_spd = 1

