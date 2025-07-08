import schedule
import time
from main import main  # your scraping/notification logic

def job():
    print("⏰ Running scheduled job...")
    main()

# Schedule to run every hour
schedule.every().minute.do(job) #every minutes

print("🔁 Scheduler started. Waiting for next run...", flush=True)

while True:
    schedule.run_pending()
    time.sleep(60)
