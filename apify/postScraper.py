from apify_client import ApifyClient
import os
import json
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import threading
import re

from db.upsert import upsert_post

load_dotenv()

MAX_DB_WORKERS = 4
DB_BATCH_SIZE = 25


def safe_int(val):
    """
    Converts values like '348,660' -> 348660
    """
    if val is None:
        return None
    if isinstance(val, int):
        return val
    if isinstance(val, str):
        val = val.replace(",", "")
        return int(val) if val.isdigit() else None
    return None

def normalize_post(item: dict) -> dict:
    """
    Clean + normalize Apify payload so DB never crashes
    """
    return {
        "urn": item.get("urn"),
        "text": item.get("text"),
        "url": item.get("url"),

        "posted_at_timestamp": item.get("postedAtTimestamp"),
        "posted_at_iso": item.get("postedAtISO"),
        "time_since_posted": item.get("timeSincePosted"),
        "is_repost": item.get("isRepost"),

        "author_type": item.get("authorType"),
        "author_profile_url": item.get("authorProfileUrl"),
        "author_profile_id": item.get("authorProfileId"),
        "author_headline": item.get("authorHeadline"),
        "author_name": item.get("authorName"),

        "type": item.get("type"),
        "share_urn": item.get("shareUrn"),

        "attributes": item.get("attributes") or [],
        "comments": item.get("comments") or [],
        "reactions": item.get("reactions") or [],

        "num_shares": safe_int(item.get("numShares")),
        "num_likes": safe_int(item.get("numLikes")),
        "num_comments": safe_int(item.get("numComments")),

        "can_react": item.get("canReact"),
        "can_post_comments": item.get("canPostComments"),
        "can_share": item.get("canShare"),
        "commenting_disabled": item.get("commentingDisabled"),

        "allowed_commenters_scope": item.get("allowedCommentersScope"),
        "root_share": item.get("rootShare"),
        "share_audience": item.get("shareAudience"),

        "author": item.get("author"),
        "author_profile_picture": item.get("authorProfilePicture"),
        "author_urn": item.get("authorUrn"),

        "document": item.get("document"),
        "is_activity": item.get("isActivity"),
        "input_url": item.get("inputUrl"),
        "linkedin_video": item.get("linkedinVideo"),
        "author_followers_count": safe_int(item.get("authorFollowersCount")),
        "poll": item.get("poll"),
        "article": item.get("article"),
        "reshared_post": item.get("resharedPost"),
        "activity_description": item.get("activityDescription"),
        "images": item.get("images"),
        "image": item.get("image"),
    }

def fetch_linkedin_posts_and_save_db():
    APIFY_KEY = os.getenv("APIFY_KEY")
    if not APIFY_KEY:
        raise Exception("Set APIFY_KEY in .env")

    client = ApifyClient(APIFY_KEY)

    print("🚀 Running LinkedIn post search scraper...")

    run_input = {
        "cookie": [
    {
        "domain": ".linkedin.com",
        "expirationDate": 1772112473.353728,
        "hostOnly": False,
        "httpOnly": False,
        "name": "lms_ads",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "AQFW_RJ-qL_dtQAAAZv_o6SCaX1KOduxkLO7-XhWttjCuCTBwCH1ZzCBwCKhr0AeqVY5zvceim-RNSmoyOaDy3NNvtGsnj8V"
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1773608495.279007,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_guid",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "46aabe54-879d-48fd-a43c-de63f28a8471"
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1785084263.900284,
        "hostOnly": False,
        "httpOnly": False,
        "name": "bcookie",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "\"v=2&33acc1e9-b661-4a43-85e9-5cadc39726cb\""
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1772112473.356138,
        "hostOnly": False,
        "httpOnly": False,
        "name": "lms_analytics",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "AQFW_RJ-qL_dtQAAAZv_o6SCaX1KOduxkLO7-XhWttjCuCTBwCH1ZzCBwCKhr0AeqVY5zvceim-RNSmoyOaDy3NNvtGsnj8V"
    },
    {
        "domain": ".linkedin.com",
        "hostOnly": False,
        "httpOnly": True,
        "name": "fptctx2",
        "path": "/",
        "sameSite": None,
        "secure": True,
        "session": True,
        "storeId": None,
        "value": "taBcrIH61PuCVH7eNCyH0K%252fD9DJ44Cptuv0RyrXgXCugmyqDvmFRXiG5mptaNUPrhio87gXflYlvSoWxMzgtgzCKMRNR5kUjhNIx83MfUbIwLq90JJdj0V41OShLcw%252f3w5IqQgyBDzMjq0LGi9Sj93QdDKrZ3pAGt40kaMea2vFYW%252fJiqQ%252bfMX%252ffXhJK%252byMd5q5GVGZCS0im6WpF7Nxsv8JInBwocSLV5jpRSHNSO4pVy5OgaV6%252b5Yp990Uejk2E2KfVwMDXvsugjCNgynNGC2J8HwjorjbXSYtL1J%252bTqU8DpULph9HoCbwpeAvm5kMChvXEY0mL1O5SqV947MdwgacGpvCL1BQUCRHBkp66cEY%253d"
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1785084192.271144,
        "hostOnly": False,
        "httpOnly": True,
        "name": "li_at",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "AQEDATJ71_MAyph4AAABmSsIHUEAAAGcJGLwtE4AubP46keypauj-YAxXZOwqyywrufg-DcfsUVZaZZz4OlMI9hae3mzwy-BL8XEaukzvpAKy6Hzy2nLg6nbA2nsq8494QN3nXfoRb-DH6A0GwsX7hL5"
    },
    {
        "domain": ".linkedin.com",
        "hostOnly": False,
        "httpOnly": False,
        "name": "lang",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": True,
        "storeId": None,
        "value": "v=2&lang=en-us"
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1769546053.391148,
        "hostOnly": False,
        "httpOnly": False,
        "name": "lidc",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "\"b=VB11:s=V:r=V:a=V:p=V:g=5709:u=2067:x=1:i=1769532264:t=1769546053:v=2:sig=AQHZR8fFT4BbxNVBntzEg4KrcC844Y3T\""
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1772112460.486457,
        "hostOnly": False,
        "httpOnly": False,
        "name": "AnalyticsSyncHistory",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "AQJbTHCOgd6R2wAAAZv_o3LSopD1xoLSRio_L6tcL_AL8Zp6Du8o538X0H_f7ZgZKrap6CMRUPxA93JPKIDalg"
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1785084260.49641,
        "hostOnly": False,
        "httpOnly": True,
        "name": "bscookie",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "\"v=1&202507141538461ea0f9b3-9770-4289-82e5-fecca630fc54AQHUMnzyMaOLWc0IC6GASVQjBvodbefF\""
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1772915588.703095,
        "hostOnly": False,
        "httpOnly": True,
        "name": "dfpfpt",
        "path": "/",
        "sameSite": None,
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "d2bc11a1278547e9af52533dea3d8e25"
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1785084192.271345,
        "hostOnly": False,
        "httpOnly": False,
        "name": "JSESSIONID",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "\"ajax:8133692680277467994\""
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1772915582.067793,
        "hostOnly": False,
        "httpOnly": True,
        "name": "li_rm",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "AQH2ehKqyrO_kQAAAZkrCApEXie6ETTBVrkDO011T5k4p9GoC-OLPGr1Vc7cn72Wz590g3vhff9a4sX_j7c8QuDuNYxL1mhWLuw21kIUhJn4MIVO4jtj0b4V"
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1777308263.900228,
        "hostOnly": False,
        "httpOnly": False,
        "name": "li_sugr",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "1bf14182-4acc-43a3-b0e8-c27a38554e67"
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1785084262,
        "hostOnly": False,
        "httpOnly": False,
        "name": "li_theme",
        "path": "/",
        "sameSite": None,
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "light"
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1785084262,
        "hostOnly": False,
        "httpOnly": False,
        "name": "li_theme_set",
        "path": "/",
        "sameSite": None,
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "app"
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1785084192.271271,
        "hostOnly": False,
        "httpOnly": False,
        "name": "liap",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "True"
    },
    {
        "domain": ".www.linkedin.com",
        "expirationDate": 1770741862,
        "hostOnly": False,
        "httpOnly": False,
        "name": "timezone",
        "path": "/",
        "sameSite": None,
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "Asia/Calcutta"
    },
    {
        "domain": ".linkedin.com",
        "expirationDate": 1772124260.496261,
        "hostOnly": False,
        "httpOnly": True,
        "name": "UserMatchHistory",
        "path": "/",
        "sameSite": "no_restriction",
        "secure": True,
        "session": False,
        "storeId": None,
        "value": "AQLOlkpgsqPY4wAAAZwAV4DKZqAA4KqzpLdotCHGyQ-SXGdvGdaa8mVaMEkKS5Lo8QVXMP5o9sb0d0_oRF_A5HjtAvUl9GjZUZdT3ZGn3Suzu7roKXH5hqJWn0vMFGSDbTKJ-GmO_5um6LvO6v-XBfROAh6oTgD8pW02Q0VGdhdHWN7R8Y3SJmIlQn3pvefmWVRo8bWqUurohgmfQBrKfbRQ2cs8tGVfkDuYnKW0GAQZHv-ikblGolzb6yCRYiGtp3XUYchXIh4kd9k3a1iEQESTJ1vxMjL5u811kU1MWZQBRZQhK8ghVC_SPWi80pikIlPjaRpq5msxN6fU9rKDgIiS_qcGh1ZQqjrMhvGsvMfKw5464g"
    }
],
        "deepScrape": True,
        "limitPerSource": 50,
        "maxDelay": 20,
        "minDelay": 10,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyCountry": "US"
        },
        "rawData": False,
        "urls": [
            # learn trading
            "https://www.linkedin.com/search/results/content/?keywords=learn%20forex%20trading&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=learn%20how%20to%20trade%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=learn%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=learn%20to%20trade%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=how%20to%20learn%20forex%20trading&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=learning%20forex%20trading&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=how%20to%20learn%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20learning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20learning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=learn%20trade%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=learning%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=learning%20to%20trade%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=learn%20forex%20trading%20step%20by%20step&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=how%20can%20i%20learn%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=how%20do%20i%20learn%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=learn%20how%20to%20trade%20the%20forex%20market&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20for%20beginners&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20basics&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20course&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20education&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20training&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=how%20to%20start%20forex%20trading&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20roadmap&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20mentorship&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20coach&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=lost%20money%20in%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=why%20forex%20trading%20is%20hard&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20losses&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20mistakes&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20psychology&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=fear%20and%20greed%20in%20trading&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20discipline&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trader%20struggling&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=blown%20trading%20account&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=why%20traders%20fail%20in%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20as%20a%20career&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=can%20forex%20trading%20replace%20job&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20side%20income&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20part%20time&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=make%20money%20with%20forex%20trading&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20full%20time&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=is%20forex%20trading%20profitable&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=price%20action%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=risk%20management%20forex&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20system&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20strategy&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20rules&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=position%20sizing%20forex&sortBy=DATE",

            # retirement
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=financial%20independence&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=long%20term%20wealth%20creation&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=passive%20income%20planning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=wealth%20preservation&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=early%20retirement%20planning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=financial%20planning%20for%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=side%20income%20for%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=401k%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=IRA%20retirement%20planning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=US%20retirement%20planning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=financial%20advisor%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=tax%20efficient%20investing&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=wealth%20management%20clients&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20income%20planning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=financial%20advice%20for%20retirement%20planning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20services&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20financial%20planning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=planning%20for%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=alternative%20retirement%20plan&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20software&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=financial%20planning%20retirement%20planning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=financial%20retirement%20plan&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20plan%20services&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20news&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=best%20retirement%20plan&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20financial%20services&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=planning%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20plan%20consultants&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=best%20plan%20for%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=best%20retirement%20plans%20for%20individuals&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=financial%20planning%20in%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20investment%20plan&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20plan%20administrators&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20plan%20advisors&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20advice&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20advisor&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20plans%20for%20small%20business&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=savings%20plans%20for%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=simple%20retirement%20plan&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=what%20is%20the%20best%20retirement%20plan&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20financial%20plan&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20plan%20administrator&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20strategies&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20financial&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20checklist&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=how%20to%20plan%20your%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20savings%20planning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=how%20much%20money%20needed%20for%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20corpus%20calculation&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20savings%20not%20enough&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=late%20retirement%20planning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=planning%20retirement%20in%2040s&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=planning%20retirement%20in%2050s&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20anxiety&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=worried%20about%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=financial%20independence%20retire%20early&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=FIRE%20movement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=passive%20income%20for%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=wealth%20building%20for%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=long%20term%20wealth%20planning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=capital%20preservation%20strategies&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20for%20entrepreneurs&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20for%20freelancers&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20for%20self%20employed&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20planning%20for%20small%20business%20owners&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20portfolio%20allocation&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=safe%20investments%20for%20retirement&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=retirement%20without%20pension&sortBy=DATE",

            # prop trading
            "https://www.linkedin.com/search/results/content/?keywords=prop%20trading&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=prop%20trading%20firms&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=prop%20firm&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=prop%20firms&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=prop%20trading%20challenge&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=prop%20firm%20challenge&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=how%20to%20pass%20prop%20firm%20challenge&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=how%20to%20pass%20prop%20trading%20challenge&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=failing%20prop%20firm%20challenge&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=failed%20prop%20firm%20challenge&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=why%20prop%20firm%20challenge%20is%20hard&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=prop%20firm%20challenge%20rules&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=prop%20firm%20evaluation&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=best%20prop%20trading%20firms&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=prop%20trading%20for%20beginners&sortBy=DATE",

            # trading challenges
            "https://www.linkedin.com/search/results/content/?keywords=most%20traders%20fail&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=why%20traders%20fail&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=why%20forex%20traders%20fail&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=trading%20failure%20reasons&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=lost%20money%20trading&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=blew%20trading%20account&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=trading%20burnout&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=trading%20frustration&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=trading%20stress&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=trading%20anxiety&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=trading%20psychology%20problems&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=trading%20without%20edge&sortBy=DATE",

            # trading reality
            "https://www.linkedin.com/search/results/content/?keywords=trading%20is%20not%20easy&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=trading%20is%20hard&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20reality&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=truth%20about%20forex%20trading&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=forex%20trading%20myths&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=why%20trading%20is%20not%20profitable&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=why%20trading%20systems%20fail&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=why%20indicators%20fail&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=trading%20math%20problem&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=risk%20reward%20trading%20problem&sortBy=DATE",

            # low risk trading
            "https://www.linkedin.com/search/results/content/?keywords=trade%20without%20risking%20capital&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=learn%20trading%20without%20losing%20money&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=practice%20trading%20without%20money&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=trading%20without%20pressure&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=risk%20free%20trading%20learning&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=paper%20trading%20vs%20real%20trading&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=capital%20preservation%20trading&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=reduce%20trading%20losses&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=low%20risk%20trading%20approach&sortBy=DATE",

            # professional trading
            "https://www.linkedin.com/search/results/content/?keywords=serious%20traders%20only&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=professional%20trading%20mindset&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=long%20term%20trading%20success&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=trading%20discipline%20required&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=trading%20patience%20required&sortBy=DATE",
            "https://www.linkedin.com/search/results/content/?keywords=realistic%20trading%20expectations&sortBy=DATE"

        ],
        "userAgent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/142.0.0.0 Safari/537.36"
        )
    }
    run = client.actor(
        "curious_coder/linkedin-post-search-scraper"
    ).call(run_input=run_input, timeout_secs= 0) # infinite time duration

    dataset_id = run.get("defaultDatasetId")
    print(f"💾 Dataset ID: {dataset_id}")

    post_queue = Queue()

    def db_worker():
        batch = []
        while True:
            post = post_queue.get()
            if post is None:
                break

            batch.append(post)

            if len(batch) >= DB_BATCH_SIZE:
                for p in batch:
                    try:
                        upsert_post(p)
                    except Exception as e:
                        print("❌ DB error:", e)
                batch.clear()

            post_queue.task_done()

        # flush remaining
        for p in batch:
            try:
                upsert_post(p)
            except Exception as e:
                print("❌ DB error:", e)

    workers = []
    for _ in range(MAX_DB_WORKERS):
        t = threading.Thread(target=db_worker, daemon=True)
        t.start()
        workers.append(t)

    count = 0
    for item in client.dataset(dataset_id).iterate_items():
        post = normalize_post(item)
        if post["urn"]:
            post_queue.put(post)
            count += 1

    print(f"📦 Queued {count} posts for DB insert")

    for _ in workers:
        post_queue.put(None)

    for t in workers:
        t.join()

    print("✅ All posts saved safely to DB")
