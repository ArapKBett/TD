from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
from config.settings import Config
from database.db_handler import Database
from services.api_client import APIClient
from utilities.security import restricted, rate_limit

db = Database()
api = APIClient()

class TelegramBot:
    def __init__(self):
        self.updater = Updater(token=Config.TELEGRAM_TOKEN, use_context=True)
        self._register_handlers()

    def _register_handlers(self):
        handlers = [
            CommandHandler('start', self.start),
            CommandHandler('cve', self.cve),
            CommandHandler('exploit', self.exploit),
            CommandHandler('search', self.search),
            CommandHandler('code', self.code_sample)
        ]
        
        for handler in handlers:
            self.updater.dispatcher.add_handler(handler)

    @restricted
    @rate_limit
    def start(self, update: Update, context: CallbackContext):
        text = """
🔒 *CyberSecurity Bot* 🔒
Available commands:
- /cve [count] - Latest CVEs
- /exploit [tool] - Exploit techniques
- /search [query] - Search security tips
- /code [tool] - Get code samples
        """
        update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)

    @restricted
    @rate_limit
    def cve(self, update: Update, context: CallbackContext):
        count = int(context.args[0]) if context.args else 5
        data = api.fetch_cve()
        
        if data:
            items = data["result"]["CVE_Items"][:count]
            formatted = "\n\n".join([
                f"🔺 *{item['cve']['CVE_data_meta']['ID']}*\n"
                f"Severity: {self._get_severity(item)}\n"
                f"{item['cve']['description']['description_data'][0]['value'][:200]}"
                for item in items
            ])
            update.message.reply_text(formatted, parse_mode=ParseMode.MARKDOWN)
            
            # Store in database
            with db.cursor() as c:
                for item in items:
                    c.execute('''
                        INSERT INTO security_data 
                        (source, category, title, description, severity)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (
                        'nvd',
                        'cve',
                        item['cve']['CVE_data_meta']['ID'],
                        item['cve']['description']['description_data'][0]['value'],
                        self._get_severity(item)
                    ))
                db.conn.commit()

    def _get_severity(self, item):
        try:
            return item['impact']['baseMetricV3']['cvssV3']['baseSeverity']
        except KeyError:
            return "N/A"

    def run(self):
        self.updater.start_polling()
        self.updater.idle()
