import json
import datetime
import os
from groq import Groq

# Groq APIキーの設定 (環境変数から取得)
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("エラー: GROQ_API_KEY環境変数が設定されていません。")
    exit()

# Groqクライアントの作成
client = Groq(api_key=GROQ_API_KEY)

# モデル名の設定
MODEL_NAME = "llama3-70b-8192"  # 使用するモデル（利用可能なモデルに変更）

# システムプロンプトの設定 (固定)
def create_system_prompt(input_info=""):
  """input_infoの内容に応じてシステムプロンプトを生成"""
  base_prompt = "あなたは日本語で回答する便利なアシスタントです。"
  if input_info:
      base_prompt += f" 以下の情報を考慮して回答してください: {input_info}" # input_infoを組み込む
  return {"role": "system", "content": base_prompt}

# プロンプトと結果を保存する関数 (Groq API経由でLLMの出力を取得する)
def save_prompt_and_result():
    """
    プロンプト、Llama 3の出力結果、追加情報をファイルに保存します。
    会話するごとに保存するかどうかをユーザーに確認します。
    LLMを使用するかどうかをユーザーに選択させ、LLMを使用しない場合は、出力結果を
    手動で入力できるようにする。
    """
    try:
        # サービスの入力 (LLMに影響しない情報)
        service_name = input("モデル名を入力してね (例: llama3-70b-8192): ")

        # 追加情報の入力 (LLMに影響を与える情報)
        input_info = input("追加情報を入力してね (例: トーン、キーワード): ")

        # LLMを使用するかどうかの確認
        use_llm_confirmation = input("LLMを使用しますか？ (y/n): ")

        if use_llm_confirmation.lower() == "y":
            # LLMを使用する場合
            # チャット履歴の初期化
            chat_history = [create_system_prompt(input_info)]
            # --- 変更点 ---
            prompt = ""  # prompt変数を初期化
            # --- ここまで ---

            while True:
                prompt = input("プロンプトを入力してね (終了するには 'exit' と入力): ") # ここでpromptに代入
                if prompt.lower() == 'exit':
                    break

                # チャット履歴にユーザーの入力を追加
                chat_history.append({"role": "user", "content": prompt})

                # Groq APIリクエストを実行
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=chat_history,
                    max_tokens=1024,
                )

                result = response.choices[0].message.content  # APIのレスポンスから結果を取得
                print("出力結果:", result)

                # チャット履歴にLLMの出力を追加
                chat_history.append({"role": "assistant", "content": result})

                # 保存の確認
                save_confirmation = input("この会話を保存しますか？ (y/n): ")
                if save_confirmation.lower() == "y":
                    now = datetime.datetime.now()
                    file_name = now.strftime("%Y%m%d_%H%M%S.json")
                    file_path = os.path.join("prompts", file_name)
                    os.makedirs("prompts", exist_ok=True)

                    data = {
                        "service_name": service_name,
                        "input_info": input_info,
                        "timestamp": now.isoformat(),
                        "prompt": prompt, # 直近のプロンプト
                        "result": result, # 直近の結果
                        "history": []
                    }

                    with open(file_path, "w", encoding="utf-8") as file:
                        json.dump(data, file, ensure_ascii=False, indent=2, separators=(',', ': '))
                    print(f"'{file_name}' に保存したよ！")
        else:
            # LLMを使用しない場合
            prompt = input("プロンプトを入力してね: ")
            result = input("出力結果を入力してね: ")  # 手動で結果を入力
            now = datetime.datetime.now()
            file_name = now.strftime("%Y%m%d_%H%M%S.json")
            file_path = os.path.join("prompts", file_name)
            os.makedirs("prompts", exist_ok=True)
            data = {
                "service_name": service_name,
                "input_info": input_info,
                "timestamp": now.isoformat(),
                "prompt": prompt,
                "result": result,
                "history": []
            }

            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=2, separators=(',', ': '))
            print(f"'{file_name}' に保存したよ！")

    except FileNotFoundError:
        print("エラー: 'prompts' フォルダが見つかりません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

# 保存したプロンプトと結果を読み込み、編集する関数
def load_prompt_and_result(file_name, edit_mode=False):
    """
    指定されたファイル名からプロンプト、結果、追加情報を読み込み、表示します。
    edit_modeがTrueの場合、編集モードになります。
    編集履歴を保存する機能も追加。
    編集したプロンプトで出力結果を再生成する機能を追加。
    """
    file_path = os.path.join("prompts", file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            print("プロンプト:", data["prompt"])
            print("結果:", data["result"])
            print("追加情報:", data["input_info"], "モデル名:", data.get("service_name", "")) #モデル名を表示

            # 履歴表示 (編集モードでなくても表示)
            if "history" not in data:  # historyキーが存在しない場合は初期化
                data["history"] = []
            print("\n--- 編集履歴 ---")
            for i, entry in enumerate(reversed(data["history"])):  # 履歴を新しいものから表示
                print(f"--- 履歴 {i+1} ---")
                print("日時:", entry["timestamp"])
                print("プロンプト:", entry["prompt"])
                print("結果:", entry["result"])
                print("追加情報:", entry["input_info"], "モデル名:", entry.get("old_service_name", "")) # 履歴でもサービス名を表示

            if edit_mode:
                # 編集モード
                print("\n--- 編集モード ---")

                # 編集前の状態を表示
                print("--- 編集前の情報 ---")
                print("プロンプト:", data["prompt"])
                print("結果:", data["result"])
                print("追加情報:", data["input_info"], "モデル名:", data.get("service_name", ""))

                # 編集
                new_prompt = input(f"新しいプロンプト (現在のプロンプト: {data['prompt']}): ") or data["prompt"]
                new_input_info = input(f"新しい追加情報 (現在の追加情報: {data['input_info']}): ") or data["input_info"]
                new_service_name = input(f"新しいモデル名 (現在のモデル名: {data.get('service_name', '')}): ") or data.get("service_name", "")

                # 出力結果の再生成
                regenerate_confirmation = input("出力結果を再生成しますか？ (y/n): ")
                if regenerate_confirmation.lower() == "y":
                    try:
                        # チャット履歴の初期化
                        chat_history = [create_system_prompt(new_input_info), {"role": "user", "content": new_prompt}]

                        # Groq APIリクエストを実行
                        response = client.chat.completions.create(
                            model=MODEL_NAME,
                            messages=chat_history,
                            max_tokens=1024,
                        )
                        new_result = response.choices[0].message.content  # APIのレスポンスから結果を取得
                        print("新しい結果:", new_result)
                    except Exception as e:
                        print(f"エラー: 出力結果の再生成に失敗しました: {e}")
                else:
                    new_result = input(f"新しい結果 (現在の結果: {data['result']}): ") or data["result"]

                # 編集履歴に追加
                now = datetime.datetime.now()
                data["history"].append({  # 履歴にすべての情報を追加
                    "timestamp": now.isoformat(),
                    "prompt": data["prompt"],
                    "result": data["result"],
                    "input_info": data["input_info"],
                    "old_service_name": data.get("service_name", ""), # 履歴に古いモデル名を記録
                    "new_service_name": new_service_name # 新しいモデル名を記録
                })

                # 編集
                data["prompt"] = new_prompt
                data["input_info"] = new_input_info
                data["result"] = new_result
                data["service_name"] = new_service_name # 新しいモデル名をdataに保存

                # 保存の確認 (新しい結果に基づいて確認)
                save_confirmation = input("変更を保存しますか？ (y/n): ")
                if save_confirmation.lower() == "y":
                    # 変更を保存
                    with open(file_path, "w", encoding="utf-8") as file:
                        json.dump(data, file, ensure_ascii=False, indent=2, separators=(',', ': '))
                    print("プロンプトを更新しました。")
                else:
                    print("変更を破棄しました。")
            # 履歴表示は、もうここにはない
    except FileNotFoundError:
        print("エラー: ファイルが見つかりません。")
    except json.JSONDecodeError:
        print("エラー: ファイルがJSON形式ではありません。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
# メニューを表示する関数
def display_menu():
    """
    メニューを表示し、ユーザーの操作を選択させます。
    """
    print("\nプロンプト管理システム")
    print("1. プロンプトと結果を保存")
    print("2. プロンプトを読み込む")
    print("3. プロンプトを編集")  # 編集機能の追加
    print("4. 終了")  # 終了機能の追加

# ユーザーの入力を受け付ける関数
def get_user_choice():
    """
    ユーザーの操作を選択させ、選択された操作番号を返します。
    """
    while True:
        choice = input("操作を選択してください (1-4): ")  # メニュー選択肢の変更
        if choice in ("1", "2", "3", "4"):  # メニュー選択肢の変更
            return choice
        else:
            print("無効な選択です。")

# メインの実行部分
def main():
    """
    プロンプト管理システムのメイン処理を実行します。
    """
    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            save_prompt_and_result()
        elif choice == "2":
            file_name = input("読み込むファイル名を入力してください (例: 20231027_123456.json): ")
            if file_name:
                load_prompt_and_result(file_name)
        elif choice == "3":  # 編集機能を選択した場合
            file_name = input("編集するファイル名を入力してください (例: 20231027_123456.json): ")
            if file_name:
                load_prompt_and_result(file_name, edit_mode=True)  # edit_modeをTrueで呼び出す
        elif choice == "4":  # 終了
            print("終了します")
            break

if __name__ == "__main__":
    main()