# models/partner_monster.py
from models.character import Character

class PartnerMonster(Character):
    def __init__(self):
        """
        【担当：メンバーD】
        初期ステータスのランダム生成。
        - hp=10 で親クラス(Character)を初期化する
        - attack, defense, speed を 2〜6 の乱数で生成してセットする
        """
        super().__init__(name="相棒", hp=10, attack=5, defense=5, speed=5)
        # ここに乱数処理を書く


    def heal(self, amount: int) -> None:
        """
        【担当：メンバーC】
        回復処理。
        - self.hp に amount を足す
        - 最大HP (self.max_hp) を超えないように調整する
        """
        pass

    def boost_stats(self, target: str, points: int) -> None:
        """
        【担当：メンバーC】
        育成・イベント用のステータス強化。
        - target に応じて、attack, defense, speed のいずれかに points を加算する
        - マイナス（呪いなど）にも対応できるよう、そのまま加算(+=)する
        """
        pass