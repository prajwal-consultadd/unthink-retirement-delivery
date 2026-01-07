from apify_client import ApifyClient
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

APIFY_KEY = os.getenv("APIFY_KEY")

if not APIFY_KEY:
    raise Exception("Set APIFY_KEY in .env before running")

client = ApifyClient(APIFY_KEY)

# Build actor input
run_input = {
    "cookie": [
        {
            "domain": ".linkedin.com",
            "expirationDate": 1768424495.337998,
            "hostOnly": False,
            "httpOnly": False,
            "name": "lms_ads",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "AQE8A-7_IfJZogAAAZsj0ZCpS7uQOJuL8Kl8eQBLypQwZT7eGzQxZzBXCZakW8Yq_BTRj-NppXCD90oeUW7fFKp25G9KbT2F"
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
            "expirationDate": 1781448183.078292,
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
            "expirationDate": 1768424495.338181,
            "hostOnly": False,
            "httpOnly": False,
            "name": "lms_analytics",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "AQE8A-7_IfJZogAAAZsj0ZCpS7uQOJuL8Kl8eQBLypQwZT7eGzQxZzBXCZakW8Yq_BTRj-NppXCD90oeUW7fFKp25G9KbT2F"
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
            "value": "taBcrIH61PuCVH7eNCyH0K%252fD9DJ44Cptuv0RyrXgXCugmyqDvmFRXiG5mptaNUPrhio87gXflYlvSoWxMzgtgzCKMRNR5kUjhNIx83MfUbIwLq90JJdj0V41OShLcw%252f3w5IqQgyBDzMjq0LGi9Sj97hyndLiwyxAfTG%252bYnBw6gGpi7L9cpbMiqzEWUp4mfq1hQrlp3oP97W%252fHzP3%252bpKExCzelbc5gY1j5g3FZY9r8OcU%252fP2Ei59HeFMNJ3aVNTmJiwmtuh6Dvtf79UU2PA7XKb8HXbTTpOah1YSg69OCHg1hwhibXMl2FJvShGaS11lZ%252b86kgguCgKL2JzN%252bkMsoFdaikaUPs%252bPSE18rfktqcXI%253d"
        },
        {
            "domain": ".www.linkedin.com",
            "expirationDate": 1781384492.661612,
            "hostOnly": False,
            "httpOnly": True,
            "name": "li_at",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "AQEDATJ71_MAyph4AAABmSsIHUEAAAGbR94Jx04AVzH-m0Qe1E5-vNuiyPe82Ue0J7zRf77N_uz9pSkIxpvqDcfOs5N9oQG-W5toHsqmpFrs4lWgSDhm1mZEK3b0zbPqjVJ9FxmOkRF8JehWX_G32872"
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
            "expirationDate": 1765906268.639933,
            "hostOnly": False,
            "httpOnly": False,
            "name": "lidc",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "\"b=OB11:s=O:r=O:a=O:p=O:g=2350:u=2035:x=1:i=1765904408:t=1765906268:v=2:sig=AQFuMNZVIMUCXWWCBBy8Swop2hjDms9g\""
        },
        {
            "domain": ".linkedin.com",
            "expirationDate": 1768424495.039245,
            "hostOnly": False,
            "httpOnly": False,
            "name": "AnalyticsSyncHistory",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "AQJ9pf7xf6gohwAAAZsj0Y-CNUZagKEQgcKMuU7P9BTbExdiGeu1JsO0zQj4ZADJsGBd4Lvc7SYOgMFl3XFkGw"
        },
        {
            "domain": ".www.linkedin.com",
            "expirationDate": 1781387602.86667,
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
            "expirationDate": 1781384492.661887,
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
            "expirationDate": 1773672183.078217,
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
            "expirationDate": 1781448181,
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
            "expirationDate": 1781448181,
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
            "expirationDate": 1781384492.661788,
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
            "expirationDate": 1767105780,
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
            "expirationDate": 1768427589.405213,
            "hostOnly": False,
            "httpOnly": True,
            "name": "UserMatchHistory",
            "path": "/",
            "sameSite": "no_restriction",
            "secure": True,
            "session": False,
            "storeId": None,
            "value": "AQKH8_yneo3GZAAAAZskAMbHKTDaY9g8tPMIXGta215X2SCMwGOrl7LMf8uipz5z48BwUNCOQQJtt3wMPwcR-JTa3o3ghhktIZ7ZN0-niGxrAZPkP5zUYVQD5obIpAW5zBGNY9W9kDnJb8YbztfLocndkWBv9aUPhVmIV7jpL5QhSCMScg8kM_Y77KjhN3QQ7_E-7g09rRxHNB5UxtoC0D2eBBQKdWW6ja_uze-z7I7p51Qpu16lLFA32sfzjct3XH522LSsCru4ECmJHmqECuLRqOjRlTo9ZSyW7ok_nWFq37qsX-72x3owZ4iZib-_jrjERY86OaqNTHxjps-C-LgZWcAzRT88E7RQTmvnD12Z_9vgBA"
        }
    ],
    "deepScrape": True,
    "limitPerSource": 5,
    "maxDelay": 8,
    "minDelay": 2,
    "proxy": {
        "useApifyProxy": True,
        "apifyProxyCountry": "US"
    },
    "rawData": False,
    "urls": [
         "https://www.linkedin.com/feed/hashtag/forexeducation/",
        "https://www.linkedin.com/search/results/content/?keywords=learning%20forex&sortBy=DATE"
    ],
    "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
}

print("🚀 Running LinkedIn post search scraper...")

# Call the Apify actor
run = client.actor("curious_coder/linkedin-post-search-scraper").call(run_input=run_input)

# The run returns a dataset ID where scraped items are stored
dataset_id = run.get("defaultDatasetId")
print(f"💾 Check your data at: https://console.apify.com/storage/datasets/{dataset_id}")

# ---- Fetch ALL items from dataset ----
items = list(client.dataset(dataset_id).iterate_items())

if not items:
    print("⚠️ Dataset is empty. Nothing to save.")
    exit(0)

# ---- Convert to DataFrame (keeps ALL fields) ----
df = pd.DataFrame(items)

# ---- Save to Excel ----
output_file = f"linkedin_posts_{dataset_id}.xlsx"
df.to_excel(output_file, index=False, engine="openpyxl")

# Iterate through the dataset
# print("\n📝 Posts:")
# for item in client.dataset(dataset_id).iterate_items():
#     post_url = item.get("postUrl")
#     text = item.get("text")
#     author = item.get("authorName")
#     profile = item.get("authorProfileUrl")
#     created_at = item.get("createdAt")
#     comments_count = item.get("commentsCount")
#     reactions_count = item.get("reactionsCount")

#     print("------")
#     print("Post URL:", post_url)
#     print("Author:", author)
#     print("Profile:", profile)
#     print("Created at:", created_at)
#     print("Text:", text[:200], "..." if len(text) > 200 else "")
#     print("Comments:", comments_count, "  Reactions:", reactions_count)
#     print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
#     print(item)
