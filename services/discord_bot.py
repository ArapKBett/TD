import discord
from discord.ext import commands
from config.settings import Config
from database.db_handler import Database
from services.api_client import APIClient

db = Database()
api = APIClient()

class DiscordBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        self._register_commands()

    def _register_commands(self):
        @self.command(name='cve')
        async def cve(ctx, count: int = 5):
            data = api.fetch_cve()
            
            if data:
                for item in data["result"]["CVE_Items"][:count]:
                    embed = discord.Embed(
                        title=item['cve']['CVE_data_meta']['ID'],
                        description=item['cve']['description']['description_data'][0]['value'][:200],
                        color=0xff0000
                    )
                    embed.add_field(name="Severity", value=item['impact']['baseMetricV3']['cvssV3']['baseSeverity'], inline=True)
                    await ctx.send(embed=embed)

    async def run(self):
        await super().start(Config.DISCORD_TOKEN)

    async def shutdown(self):
        await self.close()
