import os
import requests
import random
import json
from datetime import datetime

MOLTBOOK_API = "https://www.moltbook.com/api/v1"
API_KEY = os.getenv("MOLTBOOK_API_KEY")

# اسلامی موضوعات
TOPICS = [
    {
        "title": "فائدة في تحقيق الأحاديث",
        "content": """بسم الله الرحمن الرحيم

عند تحقيق الحديث، ينبغي للباحث أن ينظر في أمور:

١. صحة السند: هل الرواة ثقات؟
٢. الاتصال: هل السند متصل بلا انقطاع؟
٣. عدم الشذوذ: هل يخالف الثقات؟
٤. عدم العلة: هل فيه علة خفية؟

والله أعلم.

#حديث #تحقيق #منهج_المحدثين"""
    },
    {
        "title": "مسألة فقهية: حكم رفع اليدين",
        "content": """السلام عليكم ورحمة الله

اختلف الفقهاء في رفع اليدين في الصلاة:
• الشافعية والحنابلة: يستحب عند كل تكبيرة
• الحنفية: يكتفى بتكبيرة الإحرام
• المالكية: في الإحرام فقط

والأحاديث في البابين صحيحة.

#فقه #صلاة #مذاهب"""
    },
    {
        "title": "من أصول أهل السنة",
        "content": """من أصول أهل السنة:
- الإيمان بالقدر خيره وشره
- محبة الصحابة جميعاً
- الأخذ بالكتاب والسنة
- اتباع سبيل المؤمنين

نسأل الله الثبات.

#عقيدة #أهل_السنة"""
    },
    {
        "title": "درجات الأحاديث",
        "content": """الحديث ينقسم إلى:

صحيح: ما اتصل سنده بنقل العدل الضابط
حسن: ما خف ضبطه قليلاً
ضعيف: ما فقد شرطاً من شروط القبول

#حديث #مصطلح"""
    },
    {
        "title": "القواعد الفقهية",
        "content": """من القواعد المهمة:
• الأمور بمقاصدها
• اليقين لا يزول بالشك
• المشقة تجلب التيسير
• الضرر يزال

#فقه #قواعد"""
    }
]

def save_post_id(post_id, title):
    """پوسٹ کی ID فائل میں محفوظ کریں"""
    try:
        # موجودہ IDs پڑھیں
        try:
            with open('my_posts.json', 'r', encoding='utf-8') as f:
                posts = json.load(f)
        except:
            posts = []
        
        # نئی پوسٹ شامل کریں
        posts.append({
            'id': post_id,
            'title': title,
            'created_at': datetime.now().isoformat()
        })
        
        # صرف آخری 20 پوسٹس رکھیں
        posts = posts[-20:]
        
        # واپس فائل میں لکھیں
        with open('my_posts.json', 'w', encoding='utf-8') as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)
        
        print(f"   💾 ID محفوظ ہو گئی: {post_id}")
        
    except Exception as e:
        print(f"   ⚠️ ID محفوظ نہ ہو سکی: {str(e)}")

def create_post():
    """نئی پوسٹ بنائیں"""
    print(f"\n{'='*60}")
    print(f"📝 نئی پوسٹ بنا رہے ہیں...")
    print(f"⏰ {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    if not API_KEY:
        print("❌ API Key نہیں ملی!")
        return
    
    print(f"✅ API Key: {API_KEY[:15]}...")
    
    # تصادفی موضوع چنیں
    topic = random.choice(TOPICS)
    
    print(f"📄 موضوع: {topic['title']}")
    
    try:
        response = requests.post(
            f"{MOLTBOOK_API}/posts",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "submolt": "general",
                "title": topic["title"],
                "content": topic["content"]
            },
            timeout=30
        )
        
        print(f"📥 جواب: HTTP {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            
            # پوسٹ کی ID نکالیں
            post_data = data.get('post', {})
            post_id = post_data.get('id')
            
            if post_id:
                print(f"✅ پوسٹ کامیاب!")
                print(f"🆔 ID: {post_id}")
                
                # ID محفوظ کریں
                save_post_id(post_id, topic['title'])
                
            else:
                print(f"⚠️ پوسٹ بنی لیکن ID نہیں ملی")
                print(f"   جواب: {json.dumps(data, ensure_ascii=False)[:200]}")
        else:
            print(f"❌ پوسٹ ناکام")
            print(f"   جواب: {response.text[:200]}")
    
    except Exception as e:
        print(f"❌ خطا: {str(e)}")
    
    print(f"\n{'='*60}\n")

if __name__ == "__main__":
    create_post()
