# models/enemy.py
from models.character import Character
from models.partner_monster import PartnerMonster

class Enemy(Character):
    def __init__(self, name: str, hp: int, attack: int, defense: int, speed: int, is_boss: bool = False):
        """
        【データ保持用】受け取った値を親クラスに渡すだけ。
        """
        super().__init__(name, hp, attack, defense, speed)
        self.is_boss = is_boss

    @classmethod
    def create_enemy(cls, turn: int, is_boss: bool = False) -> 'Enemy':
        """
        【担当：メンバーD】
        ターン数に応じた敵を生成して返すファクトリメソッド。
        - is_boss=True の場合は、非常に強力なボスを生成して return cls(...)
        - 通常時は turn (経過ターン) の数値を計算式に入れてステータスを決め、return cls(...)
        """
        pass