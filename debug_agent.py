import os
import requests
import json

MOLTBOOK_API = "https://www.moltbook.com/api/v1"
API_KEY = os.getenv("MOLTBOOK_API_KEY")

def deep_scan():
    print("🕵️ مولٹ بُک سسٹم کا گہرا معائنہ (Deep Scan)...")
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    # 1. سب مولٹس کی فہرست حاصل کریں
    print("\n📦 1. تمام 'Submolts' کی لسٹ ڈھونڈ رہے ہیں...")
    try:
        res = requests.get(f"{MOLTBOOK_API}/submolts", headers=headers)
        if res.status_code == 200:
            data = res.json().get('data', [])
            print(f"   ✅ کل {len(data)} سب مولٹس ملے:")
            for s in data:
                print(f"      - نام: {s.get('name')}, آئی ڈی: {s.get('id')}, سلگ: {s.get('slug')}")
        else:
            print(f"   ❌ سب مولٹس کی لسٹ نہیں ملی (Status: {res.status_code})")
    except Exception as e:
        print(f"   ⚠️ خطا: {str(e)}")

    # 2. عالمی پوسٹس (بغیر کسی فلٹر کے)
    print("\n🌍 2. تمام عالمی پوسٹس (Global Posts) چیک کر رہے ہیں...")
    try:
        res = requests.get(f"{MOLTBOOK_API}/posts", headers=headers)
        if res.status_code == 200:
            data = res.json().get('data', [])
            print(f"   ✅ {len(data)} پوسٹس ملیں۔")
            if data:
                print(f"      پہلی پوسٹ کا سب مولٹ: {data[0].get('submolt')}")
        else:
            print(f"   ❌ پوسٹس نہیں ملیں (Status: {res.status_code})")
    except:
        pass

if __name__ == "__main__":
    deep_scan()
        
