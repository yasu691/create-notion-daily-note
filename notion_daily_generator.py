import os
from datetime import datetime
from notion_client import Client
import pytz

# Notion APIクライアントの初期化
notion = Client(auth=os.environ.get("NOTION_API_KEY"))
DATABASE_ID = os.environ.get("DATABASE_ID", "")

# 日本時間の現在時刻を取得
now = datetime.now(pytz.timezone("Asia/Tokyo"))
YYYYMMDD = now.strftime("%Y-%m-%d")
YYYYMMDDdd = now.strftime("%Y-%m-%d (%a)")

# メイン処理を非同期関数として定義
def main():
    # 既存のページをチェック
    already_exist = notion.databases.query(
        database_id=DATABASE_ID,
        filter={
            "property": "Name",
            "title": {
                "equals": YYYYMMDDdd
            },
        }
    )
    
    if already_exist["results"]:
        print("すでに作成されています")
        return

    try:
        # 新しいページを作成
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties={
                "Name": {
                    "title": [
                        {
                            "text": {
                                "content": YYYYMMDDdd
                            }
                        }
                    ]
                },
                "Date": {
                    "type": "date",
                    "date": {
                        "start": YYYYMMDD,
                        "end": None
                    }
                }
            }
        )
        print("作成したぞ")
    except Exception as e:
        print(e)

# スクリプトが直接実行された場合にのみmain()を実行
if __name__ == "__main__":
    main()