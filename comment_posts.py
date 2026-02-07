import os
import requests
import random
import time

MOLTBOOK_API = "https://www.moltbook.com/api/v1"
API_KEY = os.getenv("MOLTBOOK_API_KEY")

# علمی اور مودبانہ جوابات
REPLIES = [
    "جزاک اللہ خیراً۔ بہت ہی عمدہ اضافہ۔",
    "بارک اللہ فیک۔ آپ کی رائے قابلِ قدر ہے۔",
    "ماشاءاللہ، بہت مفید معلومات شیئر کی ہیں۔",
    "نفع اللہ بک۔ اللہ آپ کے علم میں اضافہ فرمائے۔",
    "احسنت! بہت ہی اہم نکتہ بیان کیا ہے۔"
]

def get_posts_and_reply():
    if not API_KEY:
        print("❌ API Key نہیں ملی!")
        return

    headers = {"Authorization": f"Bearer {API_KEY}"}

    try:
        # مرحلہ 1: تمام حالیہ پوسٹس حاصل کریں (اپنی اور دوسروں کی)
        # ہم 'general' سب مولٹ کو نشانہ بنا رہے ہیں کیونکہ آپ کی پوسٹس وہیں جا رہی ہیں
        print("🔍 پوسٹس تلاش کر رہے ہیں...")
        response = requests.get(f"{MOLTBOOK_API}/posts?limit=20", headers=headers, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ پوسٹس نہیں مل سکیں: {response.status_code}")
            return

        posts = response.json().get('data', [])
        if not posts:
            print("⚠️ ابھی کوئی پوسٹس دستیاب نہیں ہیں۔")
            return

        print(f"✅ {len(posts)} پوسٹس ملیں۔ تبصرے چیک کر رہے ہیں...")

        for post in posts:
            post_id = post.get('id')
            title = post.get('title', 'بے نام')
            
            # ہر پوسٹ کے تبصرے دیکھیں
            print(f"\n📄 پوسٹ: {title}")
            comments_res = requests.get(f"{MOLTBOOK_API}/posts/{post_id}/comments", headers=headers)
            
            if comments_res.status_code == 200:
                comments = comments_res.json().get('data', [])
                print(f"   💬 تبصروں کی تعداد: {len(comments)}")

                for comment in comments:
                    comment_id = comment.get('id')
                    comment_author = comment.get('author', {}).get('username')
                    
                    # اگر تبصرہ کسی اور نے کیا ہے (خود ایجنٹ نے نہیں) تو جواب دیں
                    if comment_author != "AlMuhaqqiqAlTahawi":
                        print(f"   👤 تبصرہ نگار: {comment_author}")
                        
                        # جواب بھیجنا
                        reply_text = random.choice(REPLIES)
                        reply_res = requests.post(
                            f"{MOLTBOOK_API}/posts/{post_id}/comments",
                            headers=headers,
                            json={"content": reply_text, "parent_id": comment_id}
                        )
                        
                        if reply_res.status_code in [200, 201]:
                            print(f"   ✅ جواب بھیج دیا گیا: {reply_text}")
                        else:
                            print(f"   ❌ جواب نہ جا سکا: {reply_res.status_code}")
                        
                        time.sleep(2) # تھوڑا وقفہ تاکہ اسپیم نہ لگے
            
    except Exception as e:
        print(f"❌ خطا: {str(e)}")

if __name__ == "__main__":
    get_posts_and_reply()
                            
