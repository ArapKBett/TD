from functools import wraps
from datetime import datetime, timedelta
from config.settings import Config
from database.db_handler import Database

db = Database()

def restricted(func):
    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        if ctx.author.id not in Config.ALLOWED_USERS:
            await ctx.send("🚫 Access Denied")
            return
        return await func(ctx, *args, **kwargs)
    return wrapper

def rate_limit(func):
    rate_limits = {}
    
    @wraps(func)
    async def wrapper(ctx, *args, **kwargs):
        user_id = ctx.author.id
        now = datetime.now()
        
        if user_id not in rate_limits:
            rate_limits[user_id] = []
        
        # Cleanup old requests
        rate_limits[user_id] = [
            t for t in rate_limits[user_id]
            if t > now - timedelta(minutes=1)
        ]
        
        if len(rate_limits[user_id]) >= Config.RATE_LIMIT:
            await ctx.send("⚠️ Rate limit exceeded. Try again later.")
            return
        
        rate_limits[user_id].append(now)
        db.log_request(user_id)
        return await func(ctx, *args, **kwargs)
    
    return wrapper
