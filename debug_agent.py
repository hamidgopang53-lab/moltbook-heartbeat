import os
import requests

# سیٹ اپ
BASE_URL = "https://www.moltbook.com/api/v1"
API_KEY = os.getenv("MOLTBOOK_API_KEY")
USERNAME = "AlMuhaqqiqAlTahawi"

def check_endpoint(name, url_suffix):
    full_url = f"{BASE_URL}{url_suffix}"
    print(f"\n🔍 چیک کر رہے ہیں: {name}")
    print(f"   URL: {full_url}")
    
    try:
        response = requests.get(
            full_url,
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=15
        )
        print(f"   سٹیٹس کوڈ: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ کامیابی! راستہ مل گیا۔")
            try:
                print(f"   ڈیٹا کی جھلک: {str(response.json())[:100]}")
            except:
                pass
        else:
            print("   ❌ یہاں کچھ نہیں ملا۔")
    except Exception as e:
        print(f"   ⚠️ ایرر: {str(e)}")

def main():
    print("--- 🚀 ایجنٹ کا راستہ تلاش کرنے کا آپریشن ---")
    if not API_KEY:
        print("❌ API Key غائب ہے!")
        return

    # 1. سب سے عام راستہ
    check_endpoint("آپشن 1: میری پوسٹس", "/me/posts")
    
    # 2. یوزر آئی ڈی ڈھونڈنا
    print("\n🕵️ User ID تلاش کر رہے ہیں...")
    try:
        res = requests.get(f"{BASE_URL}/auth/me", headers={"Authorization": f"Bearer {API_KEY}"})
        if res.status_code == 200:
            data = res.json()
            user_id = data.get('data', {}).get('id') or data.get('id')
            print(f"   ✅ ID مل گئی: {user_id}")
            if user_id:
                check_endpoint("آپشن 3: ID والا راستہ", f"/users/{user_id}/posts")
        else:
            print("   ❌ User ID نہیں ملی۔")
    except:
        pass

    # 3. نام والا پرانا راستہ
    check_endpoint("آپشن 4: نام والا راستہ", f"/users/{USERNAME}/posts")

if __name__ == "__main__":
    main()
      
