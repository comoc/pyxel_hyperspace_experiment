import pyxel
import math
import random

class App:
    def __init__(self):
        pyxel.init(160, 120)
        self.stars = []
        self.speed = 0
        self.max_speed = 15
        self.acceleration = 0.2
        
        # 初期の星を生成
        for _ in range(100):
            angle = random.uniform(0, math.pi * 2)
            distance = random.uniform(10, 200)
            speed = random.uniform(0.5, 2.0)
            self.stars.append({
                "angle": angle,
                "distance": distance,
                "speed": speed,
                "color": random.randint(1, 15)
            })
        
        pyxel.run(self.update, self.draw)

    def update(self):
        # 徐々に加速
        if pyxel.btn(pyxel.KEY_SPACE):
            self.speed = min(self.speed + self.acceleration, self.max_speed)
        else:
            self.speed = max(self.speed - self.acceleration, 0)

        # 星を更新
        for star in self.stars:
            # 距離を増加（ワープ効果）
            star["distance"] += self.speed * star["speed"]
            
            # 画面外に出た星を手前に戻す
            if star["distance"] > 200:
                star["distance"] = 10
                star["angle"] = random.uniform(0, math.pi * 2)
                star["speed"] = random.uniform(0.5, 2.0)
                star["color"] = random.randint(1, 15)

        # [Q]キーで終了
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        
        center_x = pyxel.width / 2
        center_y = pyxel.height / 2
        
        # 星を描画
        for star in self.stars:
            # 現在の位置を計算
            x = center_x + math.cos(star["angle"]) * star["distance"]
            y = center_y + math.sin(star["angle"]) * star["distance"]
            
            # 前の位置を計算（軌跡用）
            prev_x = center_x + math.cos(star["angle"]) * (star["distance"] - self.speed * star["speed"] * 2)
            prev_y = center_y + math.sin(star["angle"]) * (star["distance"] - self.speed * star["speed"] * 2)
            
            # 画面内の場合のみ描画
            if (0 <= x < pyxel.width and 0 <= y < pyxel.height and
                0 <= prev_x < pyxel.width and 0 <= prev_y < pyxel.height):
                
                # 距離に応じて色を変化
                color = min(15, max(1, star["color"] + int(self.speed)))
                
                # 軌跡を描画（ワープ時のみ）
                if self.speed > 5:
                    pyxel.line(x, y, prev_x, prev_y, color)
                else:
                    pyxel.pset(x, y, color)
        
        # スピードメーター
        meter_width = 40
        pyxel.rect(10, 10, meter_width, 5, 1)
        speed_width = int((self.speed / self.max_speed) * meter_width)
        if speed_width > 0:
            pyxel.rect(10, 10, speed_width, 5, 8)
        
        # 操作説明
        if self.speed < 1:
            pyxel.text(center_x - 30, center_y + 40, "PRESS SPACE", 7)

App()
