# views/views.py
from typing import Dict, Any
import sys
import unicodedata

# 絵文字を表示できるよう、出力を UTF-8 にする（Windows の cp932 環境対策）
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def _map_cell(mark: str) -> str:
    """マス1つ分の文字列を作る。全角/絵文字(幅2)・半角(幅1)どちらでも幅4に揃える"""
    width = sum(2 if unicodedata.east_asian_width(c) in ("W", "F") else 1 for c in mark)
    return " " + mark + " " * (3 - width)

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
    def show_player_status(player) -> None:
        """ 相棒の現在のステータスを表示する（育成部屋の表示形式 + HP/最大HP） """
        print(f"\n現在のステータス -> HP:{player.hp}/{player.max_hp}  攻撃:{player.attack}"
              f"  防御:{player.defense}  素早さ:{player.speed}")

    @staticmethod
    def show_map(map_data, hints: dict, player=None) -> None:
        """
        【担当：リーダー】
        5x5のマップの現在地と、上下左右のヒントを表示する。
        - 🦕 : 現在地 / ⬛ : 不明（隣接していないマスは探索済みでも ⬛）
        - 隣接マスのみ中身を表示 (✅:回復 👹:戦闘 🎁:イベント 💪:育成 👑:ボス)
        - hints は {"up": Room, ...} の形（Map.get_adjacent_rooms() の戻り値）
        """
        direction_labels = {"up": "上", "down": "下", "left": "左", "right": "右"}
        # 絵文字は幅2(East Asian Width = W)のものだけを使う。⚔ や 🗡 は幅が環境で変わり、枠がずれるので使わない
        type_marks = {"battle": "👹", "event": "🎁", "training": "💪", "boss": "👑"}
        hint_rooms = [id(room) for room in hints.values()]

        # --- マップ描画 ---
        # セルは幅4（_map_cell で揃える）
        border = "+----" * len(map_data.grid[0]) + "+"
        print(border)
        for y, row in enumerate(map_data.grid):
            cells = []
            for x, room in enumerate(row):
                if x == map_data.player_x and y == map_data.player_y:
                    mark = "🦕"
                elif id(room) in hint_rooms:
                    # 隣接マスだけ中身が分かる（探索済みなら ✅、それ以外は部屋の種類）
                    if room.is_cleared or room.room_type == "start":
                        mark = "✅"
                    else:
                        mark = type_marks.get(room.room_type, "⬛")
                else:
                    # 隣接していないマスは探索済みでも分からない
                    mark = "⬛"
                cells.append(_map_cell(mark))
            print("|" + "|".join(cells) + "|")
            print(border)
        print("🦕:現在地  ✅:回復  ⬛:不明")
        print("👹:戦闘  🎁:イベント  💪:育成  👑:ボス")

        # --- 相棒のステータス表示（マップの下） ---
        if player is not None:
            Views.show_player_status(player)

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
        for c in (monster, enemy):
            print(f"[{c.name}] HP:{c.hp}/{c.max_hp}  攻:{c.attack}  防:{c.defense}  速:{c.speed}")

    @staticmethod
    def show_event_options(event_data: Dict[str, Any]) -> None:
        """
        【担当：メンバーC】
        イベントのテキストと選択肢を表示する。
        """
        print(f"\n=== イベント：{event_data.get('name', 'イベント')} ===")
        print(event_data.get("description", event_data.get("text", "")))
        options = event_data.get("options", [])
        if isinstance(options, dict):
            for key, text in options.items():
                print(f"  {key}: {text}")
        else:
            for option in options:
                print(f"  {option}")

    @staticmethod
    def show_game_rule() -> None:
        """
        【担当：リーダー】
        ゲームのルールを表示する。
        """
        print("=========== ゲームのルール ===========")
        print("【目的】")
        print("  相棒モンスター🦕を育てながらダンジョンを探索し、最後に待つボスを倒そう！")
        print()
        print("【相棒のステータス】")
        print("  HP     : 0になると力尽きる。")
        print("  攻撃   : 敵に与えるダメージが増える。")
        print("  防御   : 敵から受けるダメージが減る。")
        print("  素早さ : 先攻・回避・逃走の成功しやすさに影響する。")
        print()
        print("【マップと移動】")
        print("  1. マップは5x5のマスで、左下のスタート地点から始まります。")
        print("  2. 1ターンに1回、上下左右（up / down / left / right）のどれかへ移動します。")
        print("     短縮キー: w/a/s/d（上/左/下/右）、または頭文字の大文字 U/D/R/L も使えます。")
        print("  3. 部屋の中身が分かるのは、今いるマスの上下左右の部屋だけです。")
        print("  4. 移動できるのは15ターンまで。15ターンが経過するとボスが現れます。")
        print()
        print("【部屋の種類】")
        print("  👹 戦闘部屋   : 敵と戦う。ターンが進むほど敵は強くなる。敵を倒すと報酬ポイントを獲得し、HP・攻撃・防御・素早さに自由に振り分けられます。")
        print("     （HPに振ると最大HPも上がります）")
        print("  💪 育成部屋   : 4〜7ptを獲得し、攻撃・防御・素早さの1つを強化できる。")
        print("  🎁 イベント部屋 : ランダムなイベントが発生。選択次第で得も損もする。")
        print("  ✅ 回復部屋 : 一度クリアした部屋に戻ると、休憩してHPが5回復する。")
        print("  👑 ボス部屋   : 入るとすぐにボス戦になる（15ターンを待たずに挑める）。")
        print()
        print("【戦闘】")
        print("  1. 毎ターン「1:戦う」か「2:逃げる」を選びます。")
        print("  2. 戦う : 素早さが高い方から攻撃します（同じなら相棒が先攻）。")
        print("  4. 逃げる : 失敗すると敵の攻撃を受けます。")
        print()
        print("【クリア条件】")
        print("  ボスに勝利するとゲームクリア！ボス戦では「逃げる」ことはできません。")
        print("======================================")
        
    @staticmethod
    def get_training_choice(points: int, current_atk: int, current_def: int, current_spd: int) -> str:
        """
        【担当：メンバーC】育成部屋用
        1. 「〇〇pt獲得！どこを上げる？」と表示。
        2. 攻撃・防御・素早さ から1つを選ばせる入力を受ける。
        3. 選ばれたステータスの英語名（"attack", "defense", "speed"）を返す。
        """
        print(f"\n=== 育成部屋 ===")
        print(f"{points}pt獲得！")
        print(f"現在のステータス -> 攻撃:{current_atk}  防御:{current_def}  素早さ:{current_spd}")
        print("どのステータスを上げますか？")
        print("1: 攻撃  2: 防御  3: 素早さ")

        choice_map = {1: "attack", 2: "defense", 3: "speed"}
        while True:
            try:
                user_input = int(input("番号を入力してください (1-3) > ").strip())
                if user_input in choice_map:
                    return choice_map[user_input]
                print("1, 2, 3 のいずれかの数値を入力してください。")
            except ValueError:
                print("無効な入力です。数字（1, 2, 3）を入力してください。")

    @staticmethod
    def get_reward_distribution(total_points: int) -> dict:
        """
        【担当：リーダー】戦闘勝利時用
        1. total_points をHP・攻撃・防御・素早さにどう振り分けるか、ループで1つずつ入力を受ける。
        2. 入力された値の合計が total_points になるまでやり直させる。
        3. 結果を辞書 {"hp": 〇, "attack": 〇, "defense": 〇, "speed": 〇} にして返す。
        """
        stat_labels = [("hp", "HP"), ("attack", "攻撃"), ("defense", "防御"), ("speed", "素早さ")]

        print(f"\n戦闘に勝利した！ {total_points}pt を獲得！")
        print("HP・攻撃・防御・素早さ に好きなように振り分けよう。")

        while True:
            distribution = {key: 0 for key, _ in stat_labels}
            remaining = total_points

            for key, label in stat_labels:
                # ポイントを使い切ったら、残りのステータスは 0 のまま入力を打ち切る
                if remaining == 0:
                    break
                # 1項目ずつ、正しい値が入力されるまで繰り返す
                while True:
                    raw = input(f"{label}に振り分けるポイント (残り{remaining}pt / Enterのみで0) > ").strip()
                    try:
                        # 何も入力せず Enter だけなら 0 とみなす
                        value = int(raw) if raw else 0
                    except ValueError:
                        print("エラー：数字を入力してください。")
                        continue
                    if value < 0:
                        print("エラー：マイナスの値は入力できません。")
                        continue
                    if value > remaining:
                        print(f"エラー：残りポイント({remaining}pt)を超えています。")
                        continue
                    break

                distribution[key] = value
                remaining -= value

            # 合計が total_points と一致しないときは最初からやり直し
            if sum(distribution.values()) != total_points:
                print(f"エラー：合計が {total_points}pt になっていません"
                      f"（{total_points - remaining}pt しか振り分けていません）。最初からやり直してください。\n")
                continue

            # 最終確認：振り分け一覧を表示して y/n を受け付ける
            print("\n--- 振り分け内容の確認 ---")
            for key, label in stat_labels:
                print(f"  {label}: +{distribution[key]}")
            while True:
                answer = input("この内容で確定しますか？ (y/n) > ").strip().lower()
                if answer in ("y", "n"):
                    break
                print("y か n を入力してください。")

            if answer == "y":
                print(f"振り分け完了！ HP+{distribution['hp']}  攻+{distribution['attack']}"
                      f"  防+{distribution['defense']}  速+{distribution['speed']}")
                return distribution

            print("振り分けを最初からやり直します。\n")