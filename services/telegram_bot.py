from telegram import Update, ParseMode
from telegram.ext import Application, CommandHandler, ContextTypes
from config.settings import Config
from database.db_handler import Database
from services.api_client import APIClient

db = Database()
api = APIClient()

class TelegramBot:
    def __init__(self):
        self.db = db
        self.api = api
        self.app = Application.builder().token(Config.TELEGRAM_TOKEN).build()
        self._register_handlers()

    def _register_handlers(self):
        handlers = [
            CommandHandler('start', self.start),
            CommandHandler('cve', self.cve),
        ]
        
        for handler in handlers:
            self.app.add_handler(handler)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = """
🔒 Welcome to CyberSecurity Bot!
Available commands:
/cve [count] - Latest CVEs
        """
        await update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    async def cve(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        count = int(context.args[0]) if context.args else 5
        data = self.api.fetch_cve(count)
        
        if data:
            formatted = "\n\n".join([
                f"🔺 *{item['cve']['CVE_data_meta']['ID']}*\n"
                f"Severity: {item['impact']['baseMetricV3']['cvssV3']['baseSeverity']}\n"
                f"{item['cve']['description']['description_data'][0]['value'][:200]}"
                for item in data["result"]["CVE_Items"][:count]
            ])
            await update.message.reply_text(formatted, parse_mode=ParseMode.MARKDOWN)

    async def run(self):
        await self.app.initialize()
        await self.app.start()
        await self.app.updater.start_polling()

    async def shutdown(self):
        if self.app.updater.running:
            await self.app.updater.stop()
        await self.app.stop()
        await self.app.shutdown()
