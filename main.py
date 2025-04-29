from services.telegram_bot import TelegramBot
from services.discord_bot import DiscordBot
from utilities.scheduler import AutoPoster

def main():
    # Initialize bots
    tg_bot = TelegramBot()
    ds_bot = DiscordBot()
    
    # Start auto-posting
    poster = AutoPoster(tg_bot, ds_bot)
    poster.start()
    
    # Start bots
    tg_bot.run()
    ds_bot.run()

if __name__ == "__main__":
    main()
