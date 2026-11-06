# views/views.py
from typing import Dict, Any

class Views:
    @staticmethod
    def show_message(text: str) -> None:
        """ 汎用的なメッセージ表示 """
        print(text)

    @staticmethod
    def get_player_input(prompt: str) -> str:
        """ 汎用的な入力受け付け """
        return input(f"{prompt} > ")

    @staticmethod
    def show_map(map_data, hints: dict) -> None:
        """
        【担当：リーダー】
        5x5のマップの現在地と、上下左右のヒントを表示する。
        - P : 現在地 / ? : 不明（隣接していないマスは探索済みでも ?）
        - 隣接マスのみ中身を表示 (x:探索済み B:戦闘 E:イベント T:育成 G:ボス)
        - hints は {"up": Room, ...} の形（Map.get_adjacent_rooms() の戻り値）
        """
        direction_labels = {"up": "上", "down": "下", "left": "左", "right": "右"}
        type_marks = {"battle": "B", "event": "E", "training": "T", "boss": "G"}
        hint_rooms = [id(room) for room in hints.values()]

        # --- マップ描画 ---
        print("+---" * len(map_data.grid) + "+")
        for y, row in enumerate(map_data.grid):
            cells = []
            for x, room in enumerate(row):
                if x == map_data.player_x and y == map_data.player_y:
                    mark = "P"
                elif id(room) in hint_rooms:
                    # 隣接マスだけ中身が分かる（探索済みなら x、それ以外は部屋の種類）
                    if room.is_cleared or room.room_type == "start":
                        mark = "x"
                    else:
                        mark = type_marks.get(room.room_type, "?")
                else:
                    # 隣接していないマスは探索済みでも分からない
                    mark = "?"
                cells.append(f" {mark} ")
            print("|" + "|".join(cells) + "|")
            print("+---" * len(row) + "+")
        print("P:現在地  x:探索済み  ?:不明")
        print("B:戦闘  E:イベント  T:育成  G:ボス")

        # --- 上下左右のヒント表示 ---
        print("\n[周囲の気配]")
        for direction, room in hints.items():
            label = direction_labels.get(direction, direction)
            if room.is_cleared:
                text = "探索済みの部屋だ。少し休めそうだ。"
            else:
                text = room.hint_text or "何の気配も感じない…"
            print(f"  {label}({direction}): {text}")

    @staticmethod
    def show_battle_status(monster, enemy) -> None:
        """
        【担当：メンバーB】
        プレイヤーと敵の現在のHP・ステータスを比較できるように表示する。
        """
        pass

    @staticmethod
    def show_training_options(points: int) -> None:
        """
        【担当：メンバーC】
        「〇〇pt獲得！」と現在のステータスを表示し、割り振りを促す。
        """
        pass

    @staticmethod
    def show_event_options(event_data: Dict[str, Any]) -> None:
        """
        【担当：メンバーC】
        イベントのテキストと選択肢を表示する。
        """
        pass