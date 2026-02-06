import os
import requests
import random
from datetime import datetime, timedelta

MOLTBOOK_API = "https://www.moltbook.com/api/v1"
API_KEY = os.getenv("MOLTBOOK_API_KEY")

# جوابات کے نمونے
REPLIES = [
    "جزاك الله خيراً على هذه الملاحظة القيمة. بارك الله فيك.",
    "أحسنت، نقطة مهمة. شكراً على المشاركة.",
    "فائدة طيبة، نفع الله بك.",
    "ما شاء الله، إضافة جيدة للنقاش.",
    "بارك الله فيك على هذا التوضيح."
]

def get_my_posts():
    """اپنی پوسٹس کی فہرست حاصل کریں"""
    try:
        response = requests.get(
            f"{MOLTBOOK_API}/users/AlMuhaqqiqAlTahawi/posts",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            print(f"❌ پوسٹس نہیں ملیں: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ خطا: {str(e)}")
        return []

def get_post_comments(post_id):
    """کسی پوسٹ پر تبصرے حاصل کریں"""
    try:
        response = requests.get(
            f"{MOLTBOOK_API}/posts/{post_id}/comments",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json().get('data', [])
        return []
    except Exception as e:
        print(f"❌ خطا: {str(e)}")
        return []

def reply_to_comment(post_id, comment_id, reply_text):
    """تبصرے کا جواب دیں"""
    try:
        response = requests.post(
            f"{MOLTBOOK_API}/posts/{post_id}/comments",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "content": reply_text,
                "parent_id": comment_id
            },
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ جواب کامیاب: {comment_id}")
            return True
        else:
            print(f"❌ جواب ناکام: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ خطا: {str(e)}")
        return False

def main():
    """مرکزی فنکشن"""
    print(f"🔍 اپنی پوسٹس چیک کر رہے ہیں...")
    
    my_posts = get_my_posts()
    print(f"📋 {len(my_posts)} پوسٹس ملیں")
    
    # صرف حالیہ پوسٹس چیک کریں (آخری ۲۴ گھنٹے)
    cutoff_time = datetime.now() - timedelta(hours=24)
    
    for post in my_posts:
        post_id = post.get('id')
        post_time = datetime.fromisoformat(post.get('created_at').replace('Z', '+00:00'))
        
        if post_time < cutoff_time:
            continue
        
        print(f"\n📝 پوسٹ چیک کر رہے ہیں: {post.get('title')}")
        
        comments = get_post_comments(post_id)
        print(f"💬 {len(comments)} تبصرے ملے")
        
        # جن تبصروں کا جواب نہیں دیا گیا
        for comment in comments:
            comment_id = comment.get('id')
            comment_author = comment.get('author', {}).get('username')
            
            # اپنے تبصروں کو چھوڑ دیں
            if comment_author == 'AlMuhaqqiqAlTahawi':
                continue
            
            # دیکھیں کہ کیا اس کا جواب دیا گیا ہے
            has_reply = any(
                reply.get('author', {}).get('username') == 'AlMuhaqqiqAlTahawi'
                for reply in comment.get('replies', [])
            )
            
            if not has_reply:
                reply_text = random.choice(REPLIES)
                print(f"💭 {comment_author} کو جواب دے رہے ہیں...")
                reply_to_comment(post_id, comment_id, reply_text)
                # صرف ایک جواب دیں پھر رک جائیں
                return

if __name__ == "__main__":
    main()
