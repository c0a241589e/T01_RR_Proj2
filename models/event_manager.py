# models/event_manager.py
import random
from typing import Dict, Any
from models.partner_monster import PartnerMonster

class EventManager:
    def __init__(self):
        """
        【担当：メンバーC】
        7種類のイベントデータを辞書やリストなどで定義しておく。
        （謎の泉、不思議な果実、謎の結晶、隠し部屋、呪われた宝箱、謎のモンスター、毒ガス）
        """
        pass

    def get_random_event(self) -> Dict[str, Any]:
        """
        【担当：メンバーC】
        定義したイベントの中からランダムに1つを選び、イベントデータを辞書で返す。
        - 戻り値の例: 
          {
              "id": 1, 
              "text": "モンスターが不思議な泉を見つけた。", 
              "options": {"A": "泉の水を飲む", "B": "大量に飲む"}
          }
        """
        pass

    def process_event_result(self, event_id: int, choice: str, player: PartnerMonster) -> Dict[str, Any]:
        """
        【担当：メンバーC】
        プレイヤーの選択結果に応じて、ステータスの増減を処理する。
        
        - 引数 player のメソッド (heal, boost_stats, take_damage など) を呼び出して結果を反映する。
        - 戻り値として、画面に表示するメッセージと、GameMasterへの指示(アクション)を辞書で返す。
        
        【処理の例】
        - 泉でAを選んだ場合: player.heal(20) を実行。
        - 遭遇(ID:7)で「挑発」を選んだ場合: 戻り値に "action": "start_battle" を含める。
        
        - 戻り値の例:
          {
              "message": "HPが20回復した！",
              "action": "none"  # 戦闘が発生する場合は "start_battle" にする
          }
        """
        pass