import os
import requests
import random
from datetime import datetime, timedelta

MOLTBOOK_API = "https://www.moltbook.com/api/v1"
API_KEY = os.getenv("MOLTBOOK_API_KEY")

# جوابات کے نمونے - یہ مختلف قسم کے جوابات ہیں جو تبصروں پر دیے جائیں گے
REPLIES = [
    "جزاك الله خيراً على هذه الملاحظة القيمة. بارك الله فيك.",
    "أحسنت، نقطة مهمة. شكراً على المشاركة.",
    "فائدة طيبة، نفع الله بك.",
    "ما شاء الله، إضافة جيدة للنقاش.",
    "بارك الله فيك على هذا التوضيح."
]

def get_my_recent_posts():
    """اپنی حالیہ پوسٹس کی فہرست حاصل کریں"""
    print("🔍 اپنی پوسٹس تلاش کر رہے ہیں...")
    
    try:
        # یہاں ہم فیڈ سے اپنی پوسٹس تلاش کریں گے
        response = requests.get(
            f"{MOLTBOOK_API}/feed?sort=new&limit=20",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30
        )
        
        if response.status_code == 200:
            all_posts = response.json().get('data', [])
            # صرف اپنی پوسٹس فلٹر کریں
            my_posts = [p for p in all_posts if p.get('author', {}).get('username') == 'AlMuhaqqiqAlTahawi']
            print(f"✅ {len(my_posts)} اپنی پوسٹس ملیں (کل {len(all_posts)} میں سے)")
            return my_posts
        else:
            print(f"❌ پوسٹس نہیں ملیں: HTTP {response.status_code}")
            print(f"   جواب: {response.text[:200]}")
            return []
    except Exception as e:
        print(f"❌ خطا پوسٹس لاتے وقت: {str(e)}")
        return []

def get_post_details(post_id):
    """کسی مخصوص پوسٹ کی تفصیلات حاصل کریں"""
    try:
        response = requests.get(
            f"{MOLTBOOK_API}/posts/{post_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"   ⚠️  پوسٹ کی تفصیلات نہیں ملیں: {post_id}")
            return None
    except Exception as e:
        print(f"   ❌ خطا: {str(e)}")
        return None

def reply_to_comment(post_id, parent_comment_id, reply_text):
    """تبصرے کا جواب دیں"""
    try:
        print(f"   📝 جواب بھیج رہے ہیں...")
        
        response = requests.post(
            f"{MOLTBOOK_API}/posts/{post_id}/comments",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "content": reply_text,
                "parent_id": parent_comment_id
            },
            timeout=30
        )
        
        if response.status_code == 200 or response.status_code == 201:
            print(f"   ✅ جواب کامیابی سے بھیج دیا گیا!")
            return True
        else:
            print(f"   ❌ جواب ناکام: HTTP {response.status_code}")
            print(f"   جواب: {response.text[:200]}")
            return False
    except Exception as e:
        print(f"   ❌ خطا جواب بھیجتے وقت: {str(e)}")
        return False

def main():
    """مرکزی فنکشن - یہ سب کچھ کنٹرول کرتا ہے"""
    print(f"\n{'='*60}")
    print(f"💬 تبصروں پر جوابات کا نظام شروع ہو رہا ہے")
    print(f"⏰ وقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    # اگر API Key نہیں ہے تو فوراً رک جائیں
    if not API_KEY:
        print("❌ CRITICAL: MOLTBOOK_API_KEY نہیں ملی!")
        print("   براہ کرم GitHub Secrets میں چیک کریں")
        return
    
    print(f"✅ API Key موجود ہے (پہلے 10 حروف: {API_KEY[:10]}...)")
    
    # اپنی پوسٹس حاصل کریں
    my_posts = get_my_recent_posts()
    
    if not my_posts:
        print("\n⚠️  کوئی پوسٹ نہیں ملی۔ ختم ہو رہا ہے۔")
        return
    
    # ہر پوسٹ کو چیک کریں
    total_comments_checked = 0
    total_replies_sent = 0
    
    for post in my_posts:
        post_id = post.get('id')
        post_title = post.get('title', 'بے نام')
        
        print(f"\n{'─'*60}")
        print(f"📄 پوسٹ: {post_title}")
        print(f"   ID: {post_id}")
        
        # پوسٹ کی مکمل تفصیلات حاصل کریں
        post_details = get_post_details(post_id)
        
        if not post_details:
            print(f"   ⚠️  تفصیلات نہیں ملیں، اگلی پوسٹ پر جا رہے ہیں")
            continue
        
        # تبصرے گنیں
        comments = post_details.get('comments', [])
        print(f"   💬 کل تبصرے: {len(comments)}")
        total_comments_checked += len(comments)
        
        if not comments:
            print(f"   ℹ️  کوئی تبصرہ نہیں ملا")
            continue
        
        # ہر تبصرے کو دیکھیں
        for comment in comments:
            comment_id = comment.get('id')
            comment_author = comment.get('author', {}).get('username', 'نامعلوم')
            comment_text = comment.get('content', '')[:50]  # پہلے 50 حروف
            
            print(f"\n   💭 تبصرہ از: {comment_author}")
            print(f"      متن: {comment_text}...")
            
            # اگر یہ ہمارا اپنا تبصرہ ہے تو چھوڑ دیں
            if comment_author == 'AlMuhaqqiqAlTahawi':
                print(f"      ⏭️  یہ ہمارا اپنا تبصرہ ہے، چھوڑ رہے ہیں")
                continue
            
            # دیکھیں کہ کیا ہم نے پہلے جواب دیا ہے
            replies = comment.get('replies', [])
            has_our_reply = any(
                r.get('author', {}).get('username') == 'AlMuhaqqiqAlTahawi'
                for r in replies
            )
            
            if has_our_reply:
                print(f"      ✓ ہم نے پہلے ہی جواب دے دیا ہے")
                continue
            
            # جواب بھیجیں
            reply_text = random.choice(REPLIES)
            print(f"      📤 جواب بھیج رہے ہیں: {reply_text[:40]}...")
            
            success = reply_to_comment(post_id, comment_id, reply_text)
            
            if success:
                total_replies_sent += 1
                print(f"      🎉 کامیابی!")
                # صرف ایک جواب بھیج کر رک جائیں (تاکہ سپیم نہ لگے)
                print(f"\n⏸️  اس دفعہ ایک جواب بھیج دیا، اب رک رہے ہیں")
                print(f"   (اگلی بار مزید تبصروں کا جواب دیں گے)")
                break
        
        # اگر ایک جواب بھیج چکے ہیں تو باہر نکل جائیں
        if total_replies_sent > 0:
            break
    
    # خلاصہ
    print(f"\n{'='*60}")
    print(f"📊 خلاصہ:")
    print(f"   ✓ کل تبصرے چیک کیے: {total_comments_checked}")
    print(f"   ✓ کل جوابات بھیجے: {total_replies_sent}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
