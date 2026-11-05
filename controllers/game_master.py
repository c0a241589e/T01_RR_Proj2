# controllers/game_master.py
from models.partner_monster import PartnerMonster
from models.enemy import Enemy
from models.map import Map
from models.room import Room
from models.event_manager import EventManager
from views.views import Views

class GameMaster:
    def __init__(self):
        self.current_turn: int = 1
        self.max_turn: int = 15
        self.player = PartnerMonster()
        self.map = Map()
        self.event_manager = EventManager()
        self.is_running = True

    def run(self) -> None:
        """
        【担当：リーダー】
        ゲームのメインループ。
        1. self.map.generate_grid() でマップ生成
        2. current_turn が max_turn になるまでループ
        3. process_room_select() で部屋を移動し、room_type に応じて各processメソッドへ分岐
        4. 15ターン経過でボス戦処理（Enemy.create_enemy(is_boss=True) を呼ぶ）
        """
        pass

    def process_room_select(self)-> Room:
        """
        【担当：リーダー】
        部屋選択の処理。
        1. self.map.get_adjacent_rooms() でヒントを取得
        2. Views.show_map() で表示し、Views.get_player_input() で入力を受ける
        3. self.map.move_player() で移動し、Roomを return する
        """
        pass

    def process_battle(self, enemy: Enemy) -> bool:
        """
        【担当：メンバーB】
        戦闘ループ。
        1. Views.show_battle_status() でお互いのステータス表示
        2. 素早さを比較し、高い方から攻撃処理 (calculate_dodgeで回避判定後、take_damage)
        3. 「逃げる」の場合は calculate_flee() で判定
        ※ どちらかのis_alive()がFalseになるか、逃走成功でループ終了
        """
        pass

    def calculate_dodge(self, attacker_speed: int, defender_speed: int) -> bool:
        """
        【担当：メンバーB】
        回避判定ロジック。
        defender_speed が上回っている場合のみ、差分に応じた確率で True を返す。
        """
        pass

    def calculate_flee(self, player_speed: int, enemy_speed: int) -> bool:
        """
        【担当：メンバーB】
        逃亡判定ロジック。
        基本成功率60% ＋ (player_speed - enemy_speed) × 5% で計算し、TrueかFalseを返す。
        """
        pass

    def process_training(self) -> None:
        """
        【担当：メンバーC】
        育成部屋の処理。
        4〜7ptを算出し、Views.show_training_options() を経由してプレイヤーに割り振らせる。
        """
        pass

    def process_event(self) -> None:
        """
        【担当：メンバーC】
        イベント部屋の処理。
        1. self.event_manager.get_random_event() でデータを取得
        2. Views.show_event_options() で表示し、入力を受ける
        3. process_event_result() を呼び出して結果を適用
        4. もし結果の action が "start_battle" なら、Enemyを生成して process_battle() を呼ぶ
        """
        pass

    def process_recovery(self) -> None:
        """
        【担当：メンバーC】
        クリア済み（回復）部屋の処理。player.heal() を呼び出して回復する。
        """
        pass