# models/map.py
from typing import List
from models.room import Room

class Map:
    def __init__(self):
        self.grid: List[List[Room]] = []
        self.player_x: int = 0
        self.player_y: int = 4 # 左下スタート (5x5の場合)

    def generate_grid(self) -> None:
        """
        【担当：メンバーA】
        5x5の部屋配列を生成する。
        - ボス1, 戦闘5, 育成5, イベント5, ランダム8 をシャッフルして配置
        - [0][4]（左下）は強制的にスタート部屋にする
        """
        pass

    def get_adjacent_rooms(self) -> dict:
        """
        【担当：メンバーA】
        現在地(player_x, player_y)の上下左右にある部屋のヒントを取得し、辞書で返す。
        （例: {"up": "モンスターの気配", "right": "壁"} など）
        """
        pass

    def move_player(self, direction: str) -> Room:
        """
        【担当：メンバーA】
        指定された方向へ player_x, player_y を更新し、移動先の Room オブジェクトを返す。
        """
        pass