# api/tasks.py
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta
from .models import ChatMessage

def delete_old_chats():
    cutoff_date = timezone.now() - timedelta(days=30)
    deleted_count, _ = ChatMessage.objects.filter(created_at__lt=cutoff_date).delete()
    print(f"Cleanup Task Executed: Deleted {deleted_count} old messages.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(delete_old_chats, 'interval', hours=24)
    scheduler.start()