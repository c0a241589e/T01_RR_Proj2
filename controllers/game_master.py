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

        self.map.generate_grid()

        while self.current_turn <= self.max_turn:
            Views.show_message(f"\n===== ターン {self.current_turn} / {self.max_turn} =====")
            room = self.process_room_select()

            # 部屋の種類に応じて処理を分岐
            if room.is_cleared:
                self.process_recovery()
            elif room.room_type == "boss":
                # ボス部屋に入ったらその場でボス戦 → 勝敗判定してゲーム終了
                Views.show_message("\n===== ボス部屋だ！ボスが現れた！ =====")
                boss = Enemy.create_enemy(self.current_turn, is_boss=True)
                self.judge_result(self.process_battle(boss))
                return
            elif room.room_type == "battle":
                self.process_battle(Enemy.create_enemy(self.current_turn))
            elif room.room_type == "training":
                self.process_training()
            elif room.room_type == "event":
                self.process_event()
            else:
                Views.show_message("何もない部屋だ。")
            room.is_cleared = True

            # 部屋の処理直後に生存チェック
            if not self.player.is_alive():
                self.judge_result(False)
                return

            self.current_turn += 1

        # 15ターン経過 → ボス戦
        Views.show_message("\n===== ボスが現れた！ =====")
        boss = Enemy.create_enemy(self.current_turn, is_boss=True)
        self.judge_result(self.process_battle(boss))

    def judge_result(self, boss_defeated: bool) -> None:
        """
        勝敗判定。
        - ボスを倒し、相棒が生きていれば勝利 (GAME CLEAR)
        - それ以外（相棒が力尽きた）は敗北 (GAME OVER)
        """
        self.is_running = False
        if boss_defeated and self.player.is_alive():
            Views.show_message("\n★★★ ボスを倒した！ GAME CLEAR ★★★")
        else:
            Views.show_message("\n相棒は力尽きた…… GAME OVER")

    def process_room_select(self)-> Room:
        """
        【担当：リーダー】
        部屋選択の処理。
        1. self.map.get_adjacent_rooms() でヒントを取得
        2. Views.show_map() で表示し、Views.get_player_input() で入力を受ける
        3. self.map.move_player() で移動し、Roomを return する
        """
        hints = self.map.get_adjacent_rooms()
        Views.show_map(self.map, hints)

        while True:
            direction = Views.get_player_input(
                f"どの方向へ進む？ {list(hints.keys())}"
            ).strip().lower()
            if direction in hints:
                return self.map.move_player(direction)
            Views.show_message("その方向には進めない！")

    def process_battle(self, enemy: Enemy) -> bool:
        """
        【担当：メンバーB】
        戦闘ループ。
        1. Views.show_battle_status() でお互いのステータス表示
        2. 素早さを比較し、高い方から攻撃処理 (calculate_dodgeで回避判定後、take_damage)
        3. 「逃げる」の場合は calculate_flee() で判定
        ※ どちらかのis_alive()がFalseになるか、逃走成功でループ終了
        """
        Views.show_message(f"{enemy.name} が現れた！")
        while True:
            Views.show_battle_status(self.player, enemy)
            select_action = Views.get_player_input("1:戦う　2:逃げる").strip()

            if select_action == "1":
                self.attack_round(enemy)
            elif select_action == "2":
                if enemy.is_boss:
                    Views.show_message("ボスからは逃げられない！")
                    continue
                Views.show_message("うまく逃げ切れた！")
                return False
            else:
                Views.show_message("1か2を入力してください。")
                continue

            # 勝敗判定
            if not self.player.is_alive():
                Views.show_message(f"{self.player.name} は倒れてしまった…")
                return False
            if not enemy.is_alive():
                Views.show_message(f"{enemy.name} を倒した！")
                return True

    def attack_round(self, enemy: Enemy) -> None:
        """
        1ターン分の攻撃処理。素早さが高い方から攻撃する（同値なら相棒が先攻）。
        先に攻撃した側が相手を倒したら、後攻の攻撃は行わない。
        """
        if self.player.speed >= enemy.speed:
            order = [(self.player, enemy), (enemy, self.player)]
        else:
            order = [(enemy, self.player), (self.player, enemy)]

        for attacker, defender in order:
            damage = max(1, attacker.attack - defender.defense)
            defender.take_damage(damage)
            Views.show_message(f"{attacker.name} の攻撃！ {defender.name} に {damage} のダメージ！")
            if not defender.is_alive():
                break

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
        Views.show_message("育成部屋に入った！攻撃が1上がった！")
        self.player.attack += 1

    def process_event(self) -> None:
        """
        【担当：メンバーC】
        イベント部屋の処理。
        1. self.event_manager.get_random_event() でデータを取得
        2. Views.show_event_options() で表示し、入力を受ける
        3. process_event_result() を呼び出して結果を適用
        4. もし結果の action が "start_battle" なら、Enemyを生成して process_battle() を呼ぶ
        """
        Views.show_message("イベントが発生した！しかし何も起きなかった！")

    def process_recovery(self) -> None:
        """
        【担当：メンバーC】
        クリア済み（回復）部屋の処理。player.heal() を呼び出して回復する。
        """
        Views.show_message("HPが回復した！")
        self.player.hp += 5
