import os
import requests
import random
import time

MOLTBOOK_API = "https://www.moltbook.com/api/v1"
API_KEY = os.getenv("MOLTBOOK_API_KEY")
MY_USERNAME = "AlMuhaqqiqAlTahawi"

REPLIES = [
    "جزاک اللہ خیراً۔ بہت ہی عمدہ اضافہ۔",
    "بارک اللہ فیک۔ آپ کی رائے قابلِ قدر ہے۔",
    "ماشاءاللہ، بہت مفید معلومات شیئر کی ہیں۔",
    "نفع اللہ بک۔ اللہ آپ کے علم میں اضافہ فرمائے۔",
    "احسنت! بہت ہی اہم نکتہ بیان کیا ہے۔"
]

def get_posts_from_submolt(submolt_name="general"):
    """خاص سب مولٹ سے پوسٹس حاصل کرنا"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    # ہم براہِ راست سب مولٹ کا راستہ آزمائیں گے
    url = f"{MOLTBOOK_API}/submolts/{submolt_name}/posts"
    
    print(f"🔍 سب مولٹ '{submolt_name}' میں پوسٹس تلاش کر رہے ہیں...")
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            # اگر پہلا راستہ کام نہ کرے تو دوسرا آزمائیں
            print(f"⚠️ پہلا راستہ ناکام ({response.status_code})، متبادل آزما رہے ہیں...")
            alt_url = f"{MOLTBOOK_API}/posts?submolt={submolt_name}"
            response = requests.get(alt_url, headers=headers, timeout=30)
            return response.json().get('data', [])
    except:
        return []

def main():
    if not API_KEY:
        print("❌ API Key نہیں ملی!")
        return

    posts = get_posts_from_submolt("general")
    
    if not posts:
        print("ℹ️ کوئی پوسٹ نہیں ملی۔ شاید ابھی 'general' میں کوئی نئی علمی گفتگو نہیں ہو رہی۔")
        return

    print(f"✅ {len(posts)} پوسٹس ملیں۔ تبصرے چیک کر رہے ہیں...")

    for post in posts:
        post_id = post.get('id')
        title = post.get('title', 'بے نام')[:30]
        
        # تبصرے حاصل کریں
        res = requests.get(f"{MOLTBOOK_API}/posts/{post_id}/comments", 
                           headers={"Authorization": f"Bearer {API_KEY}"})
        
        if res.status_code == 200:
            comments = res.json().get('data', [])
            for comment in comments:
                author = comment.get('author', {}).get('username')
                if author and author != MY_USERNAME:
                    # جواب بھیجیں
                    reply_text = random.choice(REPLIES)
                    requests.post(f"{MOLTBOOK_API}/posts/{post_id}/comments",
                                 headers={"Authorization": f"Bearer {API_KEY}"},
                                 json={"content": reply_text, "parent_id": comment.get('id')})
                    print(f"✅ جواب دے دیا گیا: '{reply_text}' برائے {author}")
                    time.sleep(2)

if __name__ == "__main__":
    main()
                
