from apscheduler.schedulers.background import BackgroundScheduler
from services.api_client import APIClient
from database.db_handler import Database
from config.settings import Config
from utilities.formatters import format_message

api = APIClient()
db = Database()

class AutoPoster:
    def __init__(self, telegram_bot, discord_bot):
        self.scheduler = BackgroundScheduler()
        self.telegram_bot = telegram_bot
        self.discord_bot = discord_bot
        
    def auto_post_job(self):
        data = api.fetch_cve(1)  # Last hour CVEs
        if data:
            for item in data["result"]["CVE_Items"][:3]:
                message = format_message(item)
                self._send_to_platforms(message)
                
    def _send_to_platforms(self, message):
        # Telegram
        self.telegram_bot.updater.bot.send_message(
            chat_id=Config.TELEGRAM_CHANNEL,
            text=message,
            parse_mode="Markdown"
        )
        
        # Discord
        channel = self.discord_bot.get_channel(Config.DISCORD_CHANNEL)
        self.discord_bot.loop.create_task(channel.send(message))
        
    def start(self):
        self.scheduler.add_job(self.auto_post_job, 'interval', hours=1)
        self.scheduler.start()
