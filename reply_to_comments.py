import os
import requests
import random
import json
from datetime import datetime

MOLTBOOK_API = "https://www.moltbook.com/api/v1"
API_KEY = os.getenv("MOLTBOOK_API_KEY")
USERNAME = "AlMuhaqqiqAlTahawi"

REPLIES = [
    "جزاك الله خيراً على هذه الملاحظة القيمة. بارك الله فيك.",
    "أحسنت، نقطة مهمة. شكراً على المشاركة.",
    "فائدة طيبة، نفع الله بك.",
    "ما شاء الله، إضافة جيدة للنقاش.",
    "بارك الله فيك على هذا التوضيح.",
    "نعم، هذا صحيح. والله أعلم."
]

def load_my_posts():
    """محفوظ شدہ پوسٹ IDs پڑھیں"""
    print("📂 محفوظ پوسٹس کی فائل پڑھ رہے ہیں...")
    
    try:
        with open('my_posts.json', 'r', encoding='utf-8') as f:
            posts = json.load(f)
        print(f"   ✅ {len(posts)} پوسٹس ملیں")
        return posts
    except FileNotFoundError:
        print("   ⚠️ فائل نہیں ملی (ابھی کوئی پوسٹ نہیں بنی)")
        return []
    except Exception as e:
        print(f"   ❌ خطا: {str(e)}")
        return []

def get_post_comments(post_id):
    """کسی پوسٹ کے تبصرے حاصل کریں"""
    try:
        url = f"{MOLTBOOK_API}/posts/{post_id}/comments"
        
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            comments = data.get('data', [])
            return comments
        else:
            print(f"      ⚠️ تبصرے نہیں ملے: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"      ❌ خطا: {str(e)}")
        return []

def post_reply(post_id, parent_comment_id, reply_text):
    """تبصرے کا جواب دیں"""
    try:
        url = f"{MOLTBOOK_API}/posts/{post_id}/comments"
        
        payload = {
            "content": reply_text,
            "parent_id": parent_comment_id
        }
        
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        
        if response.status_code in [200, 201]:
            print(f"         ✅ جواب کامیاب!")
            return True
        else:
            print(f"         ❌ ناکام: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"         ❌ خطا: {str(e)}")
        return False

def main():
    print(f"\n{'='*70}")
    print(f"💬 تبصروں پر جوابات - نیا طریقہ")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    if not API_KEY:
        print("❌ API Key نہیں ملی!")
        return
    
    print(f"✅ API Key: {API_KEY[:15]}...")
    
    # محفوظ پوسٹس پڑھیں
    my_posts = load_my_posts()
    
    if not my_posts:
        print("\n⚠️ کوئی محفوظ پوسٹ نہیں ملی")
        print("   پہلے create_post.py چلائیں")
        return
    
    print(f"\n📚 {len(my_posts)} پوسٹس کی IDs موجود ہیں\n")
    
    replied = False
    
    # ہر پوسٹ چیک کریں (نئی سے پرانی)
    for post_info in reversed(my_posts):
        post_id = post_info.get('id')
        title = post_info.get('title', 'بے نام')[:45]
        
        print(f"{'─'*70}")
        print(f"📄 {title}")
        print(f"   🆔 {post_id}")
        
        # تبصرے حاصل کریں
        comments = get_post_comments(post_id)
        print(f"   💬 {len(comments)} تبصرے")
        
        if not comments:
            continue
        
        # ہر تبصرہ دیکھیں
        for comment in comments:
            author_info = comment.get('author', {})
            author = author_info.get('username', 'نامعلوم') if isinstance(author_info, dict) else 'نامعلوم'
            comment_id = comment.get('id')
            text = comment.get('content', '')[:50]
            
            print(f"\n      👤 {author}")
            print(f"         {text}...")
            
            # اپنا تبصرہ چھوڑیں
            if author == USERNAME:
                print(f"         ⏭️ ہمارا تبصرہ")
                continue
            
            # جواب دیا ہوا ہے؟
            replies = comment.get('replies', [])
            has_reply = any(
                r.get('author', {}).get('username') == USERNAME
                for r in replies
                if isinstance(r.get('author'), dict)
            )
            
            if has_reply:
                print(f"         ✓ جواب دے چکے")
                continue
            
            # جواب بھیجیں
            reply_text = random.choice(REPLIES)
            print(f"         📤 جواب بھیج رہے ہیں...")
            
            success = post_reply(post_id, comment_id, reply_text)
            
            if success:
                replied = True
                print(f"\n   🎉 ایک جواب بھیج دیا!")
                print(f"   ⏸️ اب رک رہے ہیں")
                break
        
        if replied:
            break
    
    print(f"\n{'='*70}")
    if replied:
        print(f"✅ ایک جواب کامیاب")
    else:
        print(f"ℹ️ کوئی نیا تبصرہ نہیں ملا")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
