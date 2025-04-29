import discord
from discord.ext import commands
from config.settings import Config
from database.db_handler import Database
from services.api_client import APIClient
from utilities.security import restricted, rate_limit
from utilities.formatters import format_embed

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
        @restricted
        @rate_limit
        async def cve(ctx, count: int = 5):
            data = api.fetch_cve()
            
            if data:
                items = data["result"]["CVE_Items"][:count]
                for item in items:
                    embed = format_embed(
                        title=item['cve']['CVE_data_meta']['ID'],
                        description=item['cve']['description']['description_data'][0]['value'][:200],
                        color=0xff0000,
                        fields=[
                            ("Severity", self._get_severity(item), True),
                            ("Published", item['publishedDate'], True)
                        ]
                    )
                    await ctx.send(embed=embed)

        @self.command(name='code')
        @restricted
        @rate_limit
        async def code_sample(ctx, tool: str):
            # Implement code sample retrieval from database
            with db.cursor() as c:
                c.execute('''
                    SELECT title, code_sample FROM security_data
                    WHERE category = 'code' AND title LIKE ?
                    ORDER BY timestamp DESC LIMIT 1
                ''', (f"%{tool}%",))
                result = c.fetchone()
                
            if result:
                await ctx.send(f"**{result[0]}**\n```{result[1]}```")
            else:
                await ctx.send(f"No code samples found for {tool}")

    async def on_ready(self):
        print(f'Logged in as {self.user}')

    def _get_severity(self, item):
        try:
            return item['impact']['baseMetricV3']['cvssV3']['baseSeverity']
        except KeyError:
            return "N/A"

    def run(self):
        super().run(Config.DISCORD_TOKEN)
