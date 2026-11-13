# models/event_manager.py
import random
from typing import Dict, Any, List
from models.partner_monster import PartnerMonster

class EventManager:
    def __init__(self):
        """
        【担当：メンバーC】
        7種類のイベントデータを辞書やリストなどで定義しておく。
        （謎の泉、不思議な果実、謎の結晶、休息できる隠し部屋、呪われた宝箱、謎のモンスターとの遭遇、毒ガスの罠）
        """
        self.events: List[Dict[str, Any]] = [
            {
                "id": 1,
                "name": "謎の泉",
                "description": "モンスターが不思議な泉を見つけた。",
                "options": [
                    "1: 泉の水を飲む（HPが20回復）",
                    "2: 大量に飲む（全能力がランダムに変化）",
                ],
            },
            {
                "id": 2,
                "name": "不思議な果実",
                "description": "光る果実が落ちている。",
                "options": [
                    "1: 食べる",
                    "2: 食べずに立ち去る",
                ],
            },
            {
                "id": 3,
                "name": "謎の結晶",
                "description": "結晶の力がモンスターに流れ込む。どの結晶を選ぶ？",
                "options": [
                    "1: 攻撃型の結晶（攻撃力+8、防御力-3）",
                    "2: 防御型の結晶（防御力+8、素早さ-3）",
                    "3: 俊敏型の結晶（素早さ+8、最大HP-5）",
                ],
            },
            {
                "id": 5,
                "name": "休息できる隠し部屋",
                "description": "静かな部屋を見つけた。",
                "options": [
                    "1: 休む（HPが30回復）",
                    "2: 特訓する（攻撃または防御が上昇するが、HPが減少）",
                ],
            },
            {
                "id": 6,
                "name": "呪われた宝箱",
                "description": "宝箱から強い力を感じる。",
                "options": [
                    "1: 開ける",
                    "2: 無視する",
                ],
            },
            {
                "id": 7,
                "name": "謎のモンスターとの遭遇",
                "description": "野生のモンスターが現れた。",
                "options": [
                    "1: 仲良くする",
                    "2: 挑発する",
                    "3: 逃げる",
                ],
            },
            {
                "id": 8,
                "name": "毒ガスの罠",
                "description": "部屋に入ると毒ガスが噴き出した！",
                "options": [
                    "1: 回避を試みる",
                ],
            },
        ]

    def get_random_event(self) -> Dict[str, Any]:
        """
        【担当：メンバーC】
        定義したイベントの中からランダムに1つを選び、イベントデータを辞書で返す。
        """
        return random.choice(self.events)

    def process_event_result(self, event_id: int, choice: str, player: PartnerMonster) -> Dict[str, Any]:
        """
        【担当：メンバーC】
        プレイヤーの選択結果に応じて、ステータスの増減を処理する。
        - 引数 player のメソッド (heal, boost_single_stat, take_damage など) を呼び出して結果を反映する。
        - 戻り値として、画面に表示するメッセージと、GameMasterへの指示(アクション)を辞書で返す。
        """
        stat_labels = {
            "hp": "最大HP",
            "attack": "攻撃力",
            "defense": "防御力",
            "speed": "素早さ",
        }

        if event_id == 1:  # 1. 謎の泉
            if choice in ("1", "A", "a"):
                player.heal(20)
                return {"message": "泉の水を飲んだ！HPが20回復した！", "action": "none"}
            else:
                hp_diff = random.randint(-5, 5)
                atk_diff = random.randint(-3, 5)
                def_diff = random.randint(-3, 5)
                spd_diff = random.randint(-3, 5)

                player.max_hp = max(1, player.max_hp + hp_diff)
                if hp_diff > 0:
                    player.heal(hp_diff)
                else:
                    player.hp = min(player.hp, player.max_hp)
                player.attack = max(1, player.attack + atk_diff)
                player.defense = max(1, player.defense + def_diff)
                player.speed = max(1, player.speed + spd_diff)

                return {
                    "message": (
                        f"泉の水を大量に飲んだ！全能力がランダムに変化した！"
                        f"（最大HP:{hp_diff:+d}, 攻撃:{atk_diff:+d}, 防御:{def_diff:+d}, 素早さ:{spd_diff:+d}）"
                    ),
                    "action": "none",
                }

        elif event_id == 2:  # 2. 不思議な果実
            if choice == "1":
                player.boost_single_stat("attack", 5)
                # 低確率（25%）でお腹を壊し、HPが1~5減少
                if random.random() < 0.25:
                    dmg = random.randint(1, 5)
                    player.take_damage(dmg)
                    return {
                        "message": f"光る果実を食べて攻撃力が5上がった！しかしお腹を壊してHPが{dmg}減少した…",
                        "action": "none",
                    }
                return {"message": "光る果実を食べた！攻撃力が5上がった！", "action": "none"}
            return {"message": "果実には触れずに立ち去った。", "action": "none"}

        elif event_id == 3:  # 3. 謎の結晶
            if choice == "1":
                player.boost_single_stat("attack", 8)
                player.defense = max(0, player.defense - 3)
                return {
                    "message": "攻撃型の結晶を選んだ！攻撃力が8上がり、防御力が3下がった！",
                    "action": "none",
                }
            elif choice == "2":
                player.boost_single_stat("defense", 8)
                player.speed = max(0, player.speed - 3)
                return {
                    "message": "防御型の結晶を選んだ！防御力が8上がり、素早さが3下がった！",
                    "action": "none",
                }
            else:
                player.boost_single_stat("speed", 8)
                player.max_hp = max(1, player.max_hp - 5)
                player.hp = min(player.hp, player.max_hp)
                return {
                    "message": "俊敏型の結晶を選んだ！素早さが8上がり、最大HPが5下がった！",
                    "action": "none",
                }

        elif event_id == 5:  # 5. 休息できる隠し部屋
            if choice == "1":
                player.heal(30)
                return {"message": "静かな部屋でゆっくり休んだ！HPが30回復した！", "action": "none"}
            else:
                target = random.choice(["attack", "defense"])
                gain = random.randint(1, 5)
                dmg = random.randint(1, 5)
                player.boost_single_stat(target, gain)
                player.take_damage(dmg)
                return {
                    "message": f"特訓を行った！HPが{dmg}減少したが、{stat_labels[target]}が{gain}上がった！",
                    "action": "none",
                }

        elif event_id == 6:  # 6. 呪われた宝箱
            if choice == "1":
                up_stat = random.choice(["hp", "attack", "defense", "speed"])
                down_stat = random.choice(["hp", "attack", "defense", "speed"])
                curse_loss = random.randint(1, 5)

                if up_stat == "hp":
                    player.distribute_reward({"hp": 15})
                else:
                    player.boost_single_stat(up_stat, 15)

                if down_stat == "hp":
                    player.max_hp = max(1, player.max_hp - curse_loss)
                    player.hp = min(player.hp, player.max_hp)
                elif down_stat == "attack":
                    player.attack = max(0, player.attack - curse_loss)
                elif down_stat == "defense":
                    player.defense = max(0, player.defense - curse_loss)
                elif down_stat == "speed":
                    player.speed = max(0, player.speed - curse_loss)

                return {
                    "message": (
                        f"宝箱を開けた！{stat_labels[up_stat]}が15上昇したが、"
                        f"呪いを受けて{stat_labels[down_stat]}が{curse_loss}低下した！"
                    ),
                    "action": "none",
                }
            return {"message": "宝箱を無視して通り過ぎた。何も起こらなかった。", "action": "none"}

        elif event_id == 7:  # 7. 謎のモンスターとの遭遇
            if choice == "1":
                target = random.choice(["hp", "attack", "defense", "speed"])
                gain = random.randint(1, 5)
                if target == "hp":
                    player.distribute_reward({"hp": gain})
                else:
                    player.boost_single_stat(target, gain)
                return {
                    "message": f"野生のモンスターと仲良くなった！{stat_labels[target]}が{gain}上がった！",
                    "action": "none",
                }
            elif choice == "2":
                return {
                    "message": "野生のモンスターを挑発した！特別な戦闘が発生した！",
                    "action": "start_battle",
                }
            else:
                dmg = random.randint(1, 5)
                player.take_damage(dmg)
                return {
                    "message": f"HPを{dmg}消費して急いで部屋を通過した！",
                    "action": "none",
                }

        elif event_id == 8:  # 8. 毒ガスの罠
            # 素早さが高い場合（基準値10以上）は回避して無傷、低い場合はHPが1~5減少
            if player.speed >= 10:
                return {
                    "message": "毒ガスが噴き出したが、高い素早さで回避し無傷だった！",
                    "action": "none",
                }
            else:
                dmg = random.randint(1, 5)
                player.take_damage(dmg)
                return {
                    "message": f"毒ガスを避けきれなかった！HPが{dmg}減少した！",
                    "action": "none",
                }

        return {"message": "何も起こらなかった。", "action": "none"}