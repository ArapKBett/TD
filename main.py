import logging
import asyncio
from services.telegram_bot import TelegramBot
from services.discord_bot import DiscordBot
from utilities.scheduler import AutoPoster

logger = logging.getLogger(__name__)

async def main():
    # Initialize bots
    tg_bot = TelegramBot()
    ds_bot = DiscordBot()
    
    # Start auto-poster
    poster = AutoPoster(tg_bot, ds_bot)
    poster.start()
    
    try:
        # Run both bots asynchronously
        await asyncio.gather(
            tg_bot.run(),
            ds_bot.run()
        )
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
    finally:
        # Proper shutdown of bots and scheduler
        try:
            await tg_bot.shutdown()
            await ds_bot.shutdown()
            poster.scheduler.shutdown(wait=False)
        except Exception as shutdown_error:
            logger.error(f"Error during shutdown: {str(shutdown_error)}")
        logger.info("Shutting down CyberSecurity Bot")

if __name__ == "__main__":
    asyncio.run(main())
