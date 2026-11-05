# models/map.py
from typing import List, Dict
from models.room import Room

class Map:
    def __init__(self):
        self.grid: List[List[Room]] = []
        self.player_x: int = 0
        self.player_y: int = 4  # 左下をスタート位置とする (y=4, x=0)

    def generate_grid(self) -> None:
        """
        【担当：リーダー】
        5x5の部屋配列を生成する。
        1. ボス(1), 戦闘(5), 育成(5), イベント(5), ランダム(8) のリストを作りシャッフルする。
        2. 5x5の二次元配列(grid)に配置していく。[4][0]（左下）は "start" に上書き固定。
        3. 【詰み防止処理】スタート地点の隣接マス（[3][0]と[4][1]）を確認する。
           もし両方が "battle" になっていたら、片方を他のマス（安全な部屋）と入れ替える。
        """
        pass

    def get_adjacent_rooms(self) -> Dict[str, Room]:
        """
        【担当：リーダー】
        現在地(player_x, player_y)の上下左右にある部屋を取得し、辞書で返す。
        - 画面端（壁）の場合は除外する。
        - 戻り値の例: {"up": Roomオブジェクト, "right": Roomオブジェクト}
        """
        pass

    def move_player(self, direction: str) -> Room:
        """
        【担当：リーダー】
        指定された方向("up", "down", "left", "right")へ player_x, player_y を更新する。
        移動先の Room オブジェクトを return する。
        """
        pass