import os
import requests
import random
from datetime import datetime
import time

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

def get_my_posts_from_feed():
    """فیڈ سے اپنی پوسٹس تلاش کریں - زیادہ پوسٹس دیکھ کر"""
    print(f"🔍 فیڈ سے @{USERNAME} کی پوسٹس تلاش کر رہے ہیں...")
    
    my_posts = []
    
    # ہم کئی بار چیک کریں گے تاکہ زیادہ پوسٹس مل سکیں
    for page in range(3):  # تین صفحات دیکھیں گے
        try:
            offset = page * 20
            url = f"{MOLTBOOK_API}/feed?sort=new&limit=20&offset={offset}"
            print(f"   📄 صفحہ {page + 1} چیک کر رہے ہیں...")
            
            response = requests.get(
                url,
                headers={"Authorization": f"Bearer {API_KEY}"},
                timeout=30
            )
            
            if response.status_code != 200:
                print(f"   ⚠️ صفحہ {page + 1}: HTTP {response.status_code}")
                break
            
            data = response.json()
            all_posts = data.get('data', [])
            
            # اپنی پوسٹس فلٹر کریں
            for post in all_posts:
                author = post.get('author', {})
                if isinstance(author, dict):
                    author_username = author.get('username', '')
                else:
                    author_username = ''
                
                if author_username == USERNAME:
                    my_posts.append(post)
                    print(f"      ✓ ملی: {post.get('title', 'بے نام')[:40]}")
            
            # اگر کوئی پوسٹ نہیں ملی تو اگلا صفحہ دیکھیں
            if len(all_posts) < 20:
                break  # اب مزید صفحات نہیں ہیں
            
            time.sleep(1)  # ایک سیکنڈ انتظار کریں تاکہ سرور پر بوجھ نہ پڑے
            
        except Exception as e:
            print(f"   ❌ صفحہ {page + 1} خطا: {str(e)}")
            break
    
    print(f"   ✅ کل {len(my_posts)} اپنی پوسٹس ملیں")
    return my_posts

def get_post_details_with_comments(post_id):
    """پوسٹ کی مکمل تفصیلات بشمول تبصرے"""
    try:
        url = f"{MOLTBOOK_API}/posts/{post_id}"
        
        response = requests.get(
            url,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"      ⚠️ تفصیلات نہیں ملیں: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"      ❌ خطا: {str(e)}")
        return None

def post_reply(post_id, parent_comment_id, reply_text):
    """تبصرے کا جواب بھیجیں"""
    try:
        url = f"{MOLTBOOK_API}/posts/{post_id}/comments"
        
        payload = {
            "content": reply_text,
            "parent_id": parent_comment_id
        }
        
        print(f"         📤 جواب بھیج رہے ہیں...")
        
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
            print(f"         پیغام: {response.text[:150]}")
            return False
            
    except Exception as e:
        print(f"         ❌ خطا: {str(e)}")
        return False

def main():
    print(f"\n{'='*70}")
    print(f"💬 تبصروں پر جوابات کا نظام - بہتر شدہ ورژن")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"👤 صارف: @{USERNAME}")
    print(f"{'='*70}\n")
    
    if not API_KEY:
        print("❌ CRITICAL: API Key نہیں ملی!")
        return
    
    print(f"✅ API Key: {API_KEY[:12]}...")
    
    # اپنی پوسٹس حاصل کریں
    my_posts = get_my_posts_from_feed()
    
    if not my_posts:
        print("\n⚠️ کوئی پوسٹ نہیں ملی")
        print("   شاید آپ کی پوسٹس فیڈ میں بہت نیچے ہیں")
        print("   یا پھر کچھ دیر انتظار کریں")
        return
    
    print(f"\n📚 {len(my_posts)} پوسٹس ملیں، اب تبصرے چیک کر رہے ہیں...")
    
    replied = False
    
    # صرف پہلی پانچ پوسٹس چیک کریں
    for idx, post in enumerate(my_posts[:5], 1):
        post_id = post.get('id')
        title = post.get('title', 'بے نام')[:45]
        
        print(f"\n{'─'*70}")
        print(f"📄 {idx}. {title}")
        print(f"   🆔 {post_id}")
        
        # پوسٹ کی تفصیلات حاصل کریں
        details = get_post_details_with_comments(post_id)
        
        if not details:
            print(f"   ⚠️ تفصیلات نہیں ملیں")
            continue
        
        comments = details.get('comments', [])
        print(f"   💬 {len(comments)} تبصرے")
        
        if not comments:
            continue
        
        # ہر تبصرے کو دیکھیں
        for comment in comments:
            comment_id = comment.get('id')
            author_info = comment.get('author', {})
            
            if isinstance(author_info, dict):
                author = author_info.get('username', 'نامعلوم')
            else:
                author = 'نامعلوم'
            
            text = comment.get('content', '')[:50]
            
            print(f"\n      👤 {author}")
            print(f"         💭 {text}...")
            
            # اپنا تبصرہ چھوڑ دیں
            if author == USERNAME:
                print(f"         ⏭️ ہمارا تبصرہ")
                continue
            
            # دیکھیں کیا جواب دیا ہوا ہے
            replies = comment.get('replies', [])
            has_reply = False
            
            for reply in replies:
                reply_author_info = reply.get('author', {})
                if isinstance(reply_author_info, dict):
                    reply_author = reply_author_info.get('username', '')
                    if reply_author == USERNAME:
                        has_reply = True
                        break
            
            if has_reply:
                print(f"         ✓ جواب دے چکے")
                continue
            
            # جواب بھیجیں
            reply_text = random.choice(REPLIES)
            success = post_reply(post_id, comment_id, reply_text)
            
            if success:
                replied = True
                print(f"\n   🎉 کامیابی! ایک جواب بھیج دیا")
                print(f"   ⏸️ اب رک رہے ہیں (اگلی بار مزید جوابات)")
                break
        
        if replied:
            break
        
        time.sleep(2)  # دو سیکنڈ انتظار
    
    print(f"\n{'='*70}")
    if replied:
        print(f"✅ ایک جواب کامیابی سے بھیج دیا گیا")
    else:
        print(f"ℹ️ کوئی نیا تبصرہ نہیں ملا جس کا جواب دینا تھا")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()        
