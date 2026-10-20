# models/room.py
class Room:
    def __init__(self, room_type: str):
        """
        【担当：メンバーA】
        部屋の初期化を行う。
        - room_type には "start", "boss", "battle", "training", "event", "random" のいずれかが入る想定。
        - is_cleared は初期状態では False とする。
        - room_type に応じて、プレイヤーに提示する hint_text を設定する。
          （例: "battle" なら "モンスターの獰猛な気配がする…" など）
        """
        self.room_type: str = room_type
        self.is_cleared: bool = False
        self.hint_text: str = ""
        
        # メンバーAがここに hint_text を設定するif文などを書く
        pass