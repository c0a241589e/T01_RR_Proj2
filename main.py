# main.py
from controllers.game_master import GameMaster

def main():
    print("=== RR(仮) システム起動 ===")
    try:
        game = GameMaster()
        game.run()
    except Exception as e:
        print(f"致命的なエラーが発生しました: {e}")
    finally:
        print("=== ゲーム終了 ===")

if __name__ == "__main__":
    main()