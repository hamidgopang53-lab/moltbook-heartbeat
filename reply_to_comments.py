import os
import requests
import random
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
    "نعم، هذا صحيح. والله أعلم.",
    "موضوع جيد للنقاش. وفقك الله."
]

def get_user_posts():
    """صارف کی پوسٹس براہ راست پروفائل سے حاصل کریں"""
    print(f"🔍 @{USERNAME} کی پوسٹس لا رہے ہیں...")
    
    try:
        url = f"{MOLTBOOK_API}/users/{USERNAME}/posts"
        print(f"   📡 URL: {url}")
        
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30
        )
        
        print(f"   📥 HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', [])
            print(f"   ✅ {len(posts)} پوسٹس ملیں")
            return posts
        else:
            print(f"   ❌ خرابی: {response.status_code}")
            print(f"   پیغام: {response.text[:300]}")
            return []
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
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
        print(f"      ❌ Exception: {str(e)}")
        return []

def post_comment(post_id, content, parent_id=None):
    """پوسٹ پر تبصرہ یا جواب بھیجیں"""
    try:
        url = f"{MOLTBOOK_API}/posts/{post_id}/comments"
        
        payload = {"content": content}
        if parent_id:
            payload["parent_id"] = parent_id
        
        print(f"      📤 تبصرہ بھیج رہے ہیں...")
        print(f"      متن: {content[:50]}...")
        
        response = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        
        print(f"      📥 Response: {response.status_code}")
        
        if response.status_code in [200, 201]:
            print(f"      ✅ کامیابی!")
            return True
        else:
            print(f"      ❌ ناکام: {response.text[:200]}")
            return False
            
    except Exception as e:
        print(f"      ❌ Exception: {str(e)}")
        return False

def main():
    print(f"\n{'='*70}")
    print(f"💬 تبصروں پر جوابات کا نظام")
    print(f"⏰ {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
    print(f"{'='*70}\n")
    
    if not API_KEY:
        print("❌ CRITICAL: API Key نہیں ملی!")
        return
    
    print(f"✅ API Key موجود: {API_KEY[:15]}...")
    
    posts = get_user_posts()
    
    if not posts:
        print("\n⚠️ کوئی پوسٹ نہیں ملی")
        return
    
    print(f"\n📚 کل {len(posts)} پوسٹس ملیں")
    
    replied_count = 0
    
    for idx, post in enumerate(posts[:5], 1):
        post_id = post.get('id')
        title = post.get('title', 'بے نام')[:40]
        
        print(f"\n{'─'*70}")
        print(f"📄 پوسٹ {idx}: {title}")
        print(f"   ID: {post_id}")
        
        comments = get_post_comments(post_id)
        print(f"   💬 {len(comments)} تبصرے")
        
        if not comments:
            print(f"   ℹ️ کوئی تبصرہ نہیں")
            continue
        
        for comment in comments:
            author = comment.get('author', {}).get('username', 'نامعلوم')
            comment_id = comment.get('id')
            text = comment.get('content', '')[:60]
            
            print(f"\n      👤 {author}: {text}...")
            
            if author == USERNAME:
                print(f"         ⏭️ ہمارا اپنا تبصرہ")
                continue
            
            has_our_reply = False
            replies = comment.get('replies', [])
            
            for reply in replies:
                reply_author = reply.get('author', {}).get('username')
                if reply_author == USERNAME:
                    has_our_reply = True
                    break
            
            if has_our_reply:
                print(f"         ✓ پہلے جواب دے چکے")
                continue
            
            reply_text = random.choice(REPLIES)
            success = post_comment(post_id, reply_text, comment_id)
            
            if success:
                replied_count += 1
                print(f"\n   🎉 جواب کامیاب!")
                print(f"   ⏸️ ایک جواب بھیج دیا، اب رک رہے ہیں")
                break
        
        if replied_count > 0:
            break
    
    print(f"\n{'='*70}")
    print(f"📊 نتیجہ: {replied_count} جواب بھیجے")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
