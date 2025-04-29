from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.api_client import APIClient
from config.settings import Config

api = APIClient()

class AutoPoster:
    def __init__(self, telegram_bot, discord_bot):
        self.scheduler = AsyncIOScheduler()
        self.telegram_bot = telegram_bot
        self.discord_bot = discord_bot

    def auto_post_job(self):
        data = api.fetch_cve(1)
        if data:
            for item in data["result"]["CVE_Items"][:3]:
                message = f"🔒 CVE Alert: {item['cve']['CVE_data_meta']['ID']}"
                self.telegram_bot.app.bot.send_message(
                    chat_id=Config.TELEGRAM_CHANNEL,
                    text=message
                )
                discord_channel = self.discord_bot.get_channel(Config.DISCORD_CHANNEL)
                self.discord_bot.loop.create_task(discord_channel.send(message))

    def start(self):
        self.scheduler.add_job(self.auto_post_job, 'interval', hours=1)
        self.scheduler.start()
