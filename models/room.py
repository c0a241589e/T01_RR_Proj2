# models/room.py
class Room:
    def __init__(self, room_type: str):
        """
        【担当：リーダー】
        部屋の初期化を行う。
        - room_type には "start", "boss", "battle", "training", "event" のいずれかが入る。
        - is_cleared は初期状態では False とする。
        - room_type に応じて、プレイヤーに提示する hint_text を設定する。
          （例: "battle" なら "モンスターの獰猛な気配がする…" など）
        """
        self.room_type: str = room_type
        self.is_cleared: bool = False
        self.hint_text: str = ""
        
        if room_type == "start":
            self.hint_text = "見覚えのある場所だ。"
        elif room_type == "boss":
            self.hint_text = "圧倒的な威圧感が漂ってくる…！"
        elif room_type == "battle":
            self.hint_text = "モンスターの獰猛な気配がする…"
        elif room_type == "training":
            self.hint_text = "鍛錬に使えそうな道具の音が聞こえる。"
        elif room_type == "event":
            self.hint_text = "何やら不思議な気配がする…"