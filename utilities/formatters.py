from datetime import datetime
from config.settings import Config

def format_message(item, source='cve'):
    """Format raw API data into human-readable message"""
    if source == 'cve':
        return (
            f"🛡️ **New CVE Alert** 🛡️\n"
            f"🔖 ID: `{item['cve']['CVE_data_meta']['ID']}`\n"
            f"📅 Published: {datetime.fromisoformat(item['publishedDate']).strftime('%Y-%m-%d %H:%M')}\n"
            f"⚠️ Severity: {_get_severity(item)}\n"
            f"📝 Description: {item['cve']['description']['description_data'][0]['value'][:250]}..."
        )
    elif source == 'github':
        return (
            f"🐱 **GitHub Security Update** 🐱\n"
            f"📦 Repo: [{item['name']}]({item['html_url']})\n"
            f"⭐ Stars: {item['stargazers_count']}\n"
            f"🔄 Updated: {datetime.strptime(item['updated_at'], '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d %H:%M')}\n"
            f"📜 Description: {item['description'][:200] if item['description'] else 'No description'}"
        )

def format_embed(title, description, color, fields=None):
    """Create Discord embed message"""
    embed = discord.Embed(
        title=title[:256],
        description=description[:2048],
        color=color,
        timestamp=datetime.utcnow()
    )
    if fields:
        for name, value, inline in fields:
            embed.add_field(
                name=name[:256],
                value=value[:1024],
                inline=inline
            )
    embed.set_footer(text="Cybersecurity Bot • Real-time Threat Intelligence")
    return embed

def _get_severity(item):
    try:
        return item['impact']['baseMetricV3']['cvssV3']['baseSeverity']
    except KeyError:
        return "N/A"
