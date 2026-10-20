# controllers/game_master.py
from models.partner_monster import PartnerMonster
from models.map import Map
from views.views import Views

class GameMaster:
    def __init__(self):
        self.current_turn: int = 1
        self.max_turn: int = 15
        self.player = PartnerMonster()
        self.map = Map()
        self.is_running = True

    def run(self) -> None:
        """
        【担当：メンバーA】
        ゲームのメインループ。
        1. マップを生成 (self.map.generate_grid)
        2. current_turn が max_turn になるまでループ
        3. ループ内で self.process_room_select() を呼び出し、部屋のタイプごとに分岐
        4. 15ターン終わったら強制ボス戦処理へ
        """
        pass

    def process_battle(self, enemy) -> bool:
        """
        【担当：メンバーB】
        戦闘ループの処理。
        1. Viewsを使ってお互いのステータスを表示
        2. 「戦う」「逃げる」の入力を受け取る
        3. 素早さ(speed)を比較し、先攻後攻を判定
        4. calculate_dodge() を使って回避判定
        5. ダメージを take_damage() で反映し、Viewsで表示
        ※ 逃走成功、またはどちらかが倒れたらループを抜ける
        """
        pass

    def calculate_dodge(self, attacker_speed: int, defender_speed: int) -> bool:
        """
        【担当：メンバーB】
        回避判定ロジック。
        defender_speed が上回っている場合、差分に基づいた確率で True(回避)を返す。
        """
        pass

    def process_training(self) -> None:
        """
        【担当：メンバーC】
        育成部屋の処理。
        1. 4〜7の乱数を生成 (獲得ポイント)
        2. Viewsを呼んでポイントを表示
        3. プレイヤーに「どのステータスにいくつ振るか」を入力させる
        4. self.player.boost_stats() を呼び出して反映する
        """
        pass