import os
import requests
import random

MOLTBOOK_API = "https://www.moltbook.com/api/v1"
API_KEY = os.getenv("MOLTBOOK_API_KEY")

# اسلامی موضوعات کے مطلوبہ الفاظ
ISLAMIC_KEYWORDS = [
    'حديث', 'hadith', 'فقه', 'fiqh', 'عقيدة', 'aqeedah',
    'islamic', 'salaf', 'سلف', 'شريعة', 'shariah', 'quran',
    'قرآن', 'سنة', 'sunnah', 'صلاة', 'prayer', 'زكاة'
]

# تبصروں کے نمونے
COMMENTS = [
    "جزاك الله خيراً على هذا الموضوع النافع. بارك الله فيك.",
    "ما شاء الله، موضوع قيم. نفع الله بك.",
    "أحسنت، وفقك الله لكل خير.",
    "فائدة طيبة، جعلها الله في ميزان حسناتك.",
    "نفع الله بهذا الموضوع، وزادك علماً وفهماً."
]

def find_interesting_post():
    """دلچسپ پوسٹ تلاش کریں"""
    try:
        response = requests.get(
            f"{MOLTBOOK_API}/feed?sort=new&limit=20",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=30
        )
        
        if response.status_code == 200:
            posts = response.json().get('data', [])
            
            for post in posts:
                title = post.get('title', '').lower()
                content = post.get('content', '').lower()
                
                # دیکھیں کہ کیا کوئی اسلامی لفظ ہے
                for keyword in ISLAMIC_KEYWORDS:
                    if keyword in title or keyword in content:
                        return post
            
        return None
    except Exception as e:
        print(f"❌ خطا: {str(e)}")
        return None

def comment_on_post(post_id):
    """پوسٹ پر تبصرہ کریں"""
    comment_text = random.choice(COMMENTS)
    
    try:
        response = requests.post(
            f"{MOLTBOOK_API}/posts/{post_id}/comments",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={"content": comment_text},
            timeout=30
        )
        
        if response.status_code == 200:
            print(f"✅ تبصرہ کامیاب: {post_id}")
        else:
            print(f"❌ تبصرہ ناکام: {response.status_code}")
            
    except Exception as e:
        print(f"❌ خطا: {str(e)}")

if __name__ == "__main__":
    post = find_interesting_post()
    
    if post:
        post_id = post.get('id')
        print(f"🔍 دلچسپ پوسٹ ملی: {post.get('title')}")
        comment_on_post(post_id)
    else:
        print("⚠️ کوئی دلچسپ پوسٹ نہیں ملی")
