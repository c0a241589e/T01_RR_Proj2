# models/map.py
import random
from typing import List, Dict
from models.room import Room

class Map:
    # 方向 -> (dx, dy)。grid[y][x] で、y が小さいほど上
    DIRECTIONS = {"up": (0, -1), "down": (0, 1), "left": (-1, 0), "right": (1, 0)}

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
           - "boss" があれば、他のマス（安全な部屋）と入れ替える。
           - 両方が "battle" なら、片方を他のマス（安全な部屋）と入れ替える（戦闘は1つまで）。
        """
        # 1. 部屋タイプのリストを作る（スタート以外の24部屋）
        normal_types = ["battle", "training", "event"]
        room_types = ["boss"]
        for room_type in normal_types:
            room_types += [room_type] * 5          # 各タイプ最低5部屋
        room_types += [random.choice(normal_types) for _ in range(8)]  # 残り8部屋はランダム
        random.shuffle(room_types)

        # 2. 5x5に配置（左下 [4][0] はスタート固定）
        self.grid = []
        index = 0
        for y in range(5):
            row: List[Room] = []
            for x in range(5):
                if (y, x) == (4, 0):
                    row.append(Room("start"))
                else:
                    row.append(Room(room_types[index]))
                    index += 1
            self.grid.append(row)

        # 3. 詰み防止：スタート隣接マスの制限
        #    - ボス部屋は置かない
        #    - 戦闘部屋は1つまで
        start_neighbors = [(3, 0), (4, 1)]
        safe_cells = [
            (y, x)
            for y in range(5) for x in range(5)
            if (y, x) not in start_neighbors
            and self.grid[y][x].room_type in ("training", "event")
        ]

        def swap_with_safe(y: int, x: int) -> None:
            sy, sx = safe_cells.pop(random.randrange(len(safe_cells)))
            self.grid[y][x], self.grid[sy][sx] = self.grid[sy][sx], self.grid[y][x]

        battle_count = 0
        for y, x in start_neighbors:
            room_type = self.grid[y][x].room_type
            if room_type == "boss":
                swap_with_safe(y, x)
            elif room_type == "battle":
                battle_count += 1
                if battle_count > 1:
                    swap_with_safe(y, x)

        # プレイヤー位置もスタートにリセット
        self.player_x, self.player_y = 0, 4

    def get_adjacent_rooms(self) -> Dict[str, Room]:
        """
        【担当：リーダー】
        現在地(player_x, player_y)の上下左右にある部屋を取得し、辞書で返す。
        - 画面端（壁）の場合は除外する。
        - 戻り値の例: {"up": Roomオブジェクト, "right": Roomオブジェクト}
        """
        adjacent: Dict[str, Room] = {}
        for direction, (dx, dy) in self.DIRECTIONS.items():
            nx, ny = self.player_x + dx, self.player_y + dy
            if 0 <= nx < 5 and 0 <= ny < 5:
                adjacent[direction] = self.grid[ny][nx]
        return adjacent

    def move_player(self, direction: str) -> Room:
        """
        【担当：リーダー】
        指定された方向("up", "down", "left", "right")へ player_x, player_y を更新する。
        移動先の Room オブジェクトを return する。
        """
        dx, dy = self.DIRECTIONS[direction]
        # 壁の外には出ないように 0〜4 に収める
        self.player_x = min(max(self.player_x + dx, 0), 4)
        self.player_y = min(max(self.player_y + dy, 0), 4)
        return self.grid[self.player_y][self.player_x]
