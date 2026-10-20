# models/enemy.py
import random

class Enemy:
    def __init__(self, is_boss: bool = False):
        """
        【担当：メンバーD】
        敵の初期ステータスを生成する。
        - is_boss が True の場合、非常に高いステータス（HP50など）と専用の名前を設定する。
        - is_boss が False の場合、通常のランダムなステータス（HP, attack, defense, speed）を設定する。
        """
        self.is_boss: bool = is_boss
        self.name: str = ""
        self.hp: int = 0
        self.attack: int = 0
        self.defense: int = 0
        self.speed: int = 0
        
        # メンバーDがここにステータス生成の具体的なロジック（if文など）を書く
        pass

    def take_damage(self, amount: int) -> int:
        """
        【担当：メンバーB】
        敵がダメージを受ける処理。
        - self.hp から amount を引く
        - HPが0未満にならないように調整する（0を維持）
        - 実際に減ったダメージ量を return する
        """
        pass