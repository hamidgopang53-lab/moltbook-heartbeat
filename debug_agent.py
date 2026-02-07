import os
import requests
import json

# --- سیٹ اپ ---
BASE_URL = "https://www.moltbook.com/api/v1"
API_KEY = os.getenv("MOLTBOOK_API_KEY")

def inspect_feed():
    print("🚀 آپریشن: فیڈ کی جاسوسی")
    print("=========================")
    
    # ہم جانتے ہیں کہ فیڈ کام کرتی ہے، اس لیے وہیں چلتے ہیں
    url = f"{BASE_URL}/feed?limit=5"
    
    try:
        print(f"📡 فیڈ سے ڈیٹا منگوا رہے ہیں...")
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=15
        )
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', [])
            
            if not posts:
                print("❌ فیڈ خالی ہے۔")
                return

            print(f"✅ {len(posts)} پوسٹس مل گئیں۔")
            
            # پہلی پوسٹ کا مکمل پوسٹ مارٹم
            first_post = posts[0]
            print("\n🔬 پہلی پوسٹ کا تجزیہ (Post Analysis):")
            print(f"   - Post ID: {first_post.get('id')}")
            
            author = first_post.get('author', {})
            print(f"   - Author Data: {author}")
            
            if isinstance(author, dict):
                print(f"   👉 Author ID: {author.get('id')}")
                print(f"   👉 Username: {author.get('username')}")
            
            # اب ہم دیکھتے ہیں کہ اس پوسٹ کے تبصرے (Comments) کس لنک پر ہیں
            print(f"\n🔗 لنکس کا ڈھانچہ:")
            # اکثر API خود بتاتی ہے کہ اگلا لنک کیا ہے
            print(json.dumps(first_post, indent=2)[:500]) # صرف شروع کا حصہ دیکھیں
            
        else:
            print(f"❌ فیڈ نہیں ملی (Status: {response.status_code})")
            
    except Exception as e:
        print(f"⚠️ ایرر: {str(e)}")

if __name__ == "__main__":
    inspect_feed()
    
