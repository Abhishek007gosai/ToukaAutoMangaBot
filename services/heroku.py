# Made by @codexnano from scratch.
# If you find any bugs, please let us know in the channel updates.
# You can 'git pull' to stay updated with the latest changes.

import aiohttp
import logging
from config import Config
log = logging.getLogger(__name__)
class Heroku:
    BASE_URL = "https://api.heroku.com"
    HEADERS = {
        "Accept": "application/vnd.heroku+json; version=3",
        "Authorization": f"Bearer {Config.HEROKU_API_KEY}" if hasattr(Config, 'HEROKU_API_KEY') and Config.HEROKU_API_KEY else ""
    }
    @classmethod
    async def _req(cls, method, path, data=None):
        if not Config.HEROKU_API_KEY or not Config.HEROKU_APP_NAME:
            return None, "Heroku credentials not set"
        async with aiohttp.ClientSession(headers=cls.HEADERS) as sess:
            url = f"{cls.BASE_URL}/apps/{Config.HEROKU_APP_NAME}{path}"
            async with sess.request(method, url, json=data) as resp:
                if resp.status >= 400:
                    try:
                        err = await resp.json()
                        return None, err.get('message', 'Unknown error')
                    except:
                        return None, f"HTTP {resp.status}"
                return await resp.json(), None
    @classmethod
    async def get_app(cls):
        return await cls._req("GET", "")
    @classmethod
    async def get_dynos(cls):
        return await cls._req("GET", "/dynos")
    @classmethod
    async def restart_all(cls):
        return await cls._req("DELETE", "/dynos")
    @classmethod
    async def restart_dyno(cls, dyno_id):
        return await cls._req("DELETE", f"/dynos/{dyno_id}")
    @classmethod
    async def get_logs(cls, lines=100):
        res, err = await cls._req("POST", "/log-sessions", {"lines": lines})
        if err: return None, err
        log_url = res.get('logplex_url')
        if not log_url: return None, "Log URL not found"
        async with aiohttp.ClientSession() as sess:
            async with sess.get(log_url) as resp:
                if resp.status == 200:
                    return await resp.text(), None
                return None, f"Failed to fetch logs: {resp.status}"
    @classmethod
    async def get_vars(cls):
        return await cls._req("GET", "/config-vars")
    @classmethod
    async def set_var(cls, key, val):
        return await cls._req("PATCH", "/config-vars", {key: val})
    @classmethod
    async def del_var(cls, key):
        return await cls._req("PATCH", "/config-vars", {key: None})
