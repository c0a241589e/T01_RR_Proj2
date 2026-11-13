# controllers/game_master.py
import random
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

        Views.show_game_rule()
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
        1. 戦闘ループ（Viewsから「1:戦う 2:逃げる」の入力を受ける）
        
        2. 「逃げる」選択時の処理：
           - 敵がボス (enemy.is_boss) の場合は「逃げられない！」と表示して失敗扱い。
           - ボス以外なら self.calculate_flee(...) を呼び、成功すればループを抜ける。
           
        3. 「戦う」選択・敵の攻撃処理：
           - プレイヤーの攻撃で敵にダメージを与える。
           - 敵の攻撃前には self.calculate_dodge(...) を呼び、False(回避失敗)の時だけプレイヤーにダメージを与える。
           - どちらかの is_alive() が False になったらループを抜ける。
           
        4. 戦闘ループ終了後の処理：
           - もし敵を倒した (enemy.is_alive() == False) なら、報酬割り振りを行う。
             distribution = Views.get_reward_distribution(enemy.reward_points)
             self.player.distribute_reward(distribution)
             
        5. 最後に return self.player.is_alive() を返す。
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
        防御側の素早さが高い場合、差分×5%などの確率を計算し、回避成功なら True を返す。
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
        1. 4〜7の乱数ポイントを生成する。
        2. choice = Views.get_training_choice(points, ...) を呼んで選ばれたステータスを取得。
        3. self.player.boost_single_stat(choice, points) を実行する。
        """
        points = random.randint(4, 7)
        choice = Views.get_training_choice(
            points,
            self.player.attack,
            self.player.defense,
            self.player.speed,
        )
        self.player.boost_single_stat(choice, points)
        stat_labels = {"attack": "攻撃", "defense": "防御", "speed": "素早さ"}
        Views.show_message(f"{stat_labels.get(choice, choice)}が {points} 上がった！")

    def process_event(self) -> None:
        """
        【担当：メンバーC】
        1. event_data = self.event_manager.get_random_event()
        2. Views.show_event_options() で表示し入力結果を受け取る。
        3. result = self.event_manager.process_event_result(...)
        4. result["action"] == "start_battle" ならボス以外の敵を生成して process_battle(enemy) に突入させる。
        """
        event_data = self.event_manager.get_random_event()
        Views.show_event_options(event_data)

        num_options = len(event_data.get("options", []))
        valid_choices = [str(i) for i in range(1, num_options + 1)] if num_options > 0 else ["1", "2"]

        while True:
            try:
                raw_input = Views.get_player_input(f"選択肢を選んでください ({'/'.join(valid_choices)})").strip()
                choice_num = int(raw_input)
                if str(choice_num) in valid_choices:
                    choice = str(choice_num)
                    break
                Views.show_message(f"{', '.join(valid_choices)} のいずれかを入力してください。")
            except ValueError:
                Views.show_message(f"無効な入力です。数字（{', '.join(valid_choices)}）を入力してください。")

        result = self.event_manager.process_event_result(event_data["id"], choice, self.player)
        Views.show_message(result["message"])

        if result.get("action") == "start_battle":
            enemy = Enemy.create_enemy(self.current_turn, is_boss=False)
            self.process_battle(enemy)

    def process_recovery(self) -> None:
        """
        【担当：メンバーC】
        クリア済み（回復）部屋の処理。player.heal() を呼び出して回復する。
        """
        self.player.heal(5)
        Views.show_message("探索済みの部屋で休憩した。HPが5回復した！")
