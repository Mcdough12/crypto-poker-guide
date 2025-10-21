import os, re, datetime, pathlib
from textwrap import dedent


# Uses OpenAI Chat Completions API via requests to avoid extra deps
import json, urllib.request


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
raise SystemExit("Missing OPENAI_API_KEY env var")


REF_BASE = "https://record.coinpokeraffiliates.com/_W8N9Np6OF21fWQTENI37dGNd7ZgqdRLk/1/"


def ref_url(source="seo", medium="blog"):
from urllib.parse import urlencode
q = urlencode({"utm_source":source, "utm_medium":medium, "utm_campaign":"coinpoker"})
return f"{REF_BASE}?{q}"


BRAND = os.getenv("SITE_BRAND", "Crypto Poker Guide")
TOPICS = [
"How to play poker with USDT on CoinPoker (beginner guide)",
"Bankroll management for micro-stakes in crypto poker",
"Understanding rake and rakeback on crypto poker sites",
"How to fund your wallet safely (ETH vs USDT, fees, chains)",
"Freeroll strategies to build a bankroll from zero"
]


def slugify(s):
return re.sub(r"[^a-z0-9]+","-", s.lower()).strip("-")


def front_matter(title, description, tags):
return dedent(f"""---
title: "{title}"
description: "{description}"
date: {datetime.date.today().isoformat()}
tags: {tags}
layout: post
---
""")


def cta_block():
url = ref_url()
return f"\n> 🚀 Ready to play? Join CoinPoker here: [{url}]({url})\n\n_Affiliate disclosure: we may earn a commission if you sign up._\n"


def openai_chat(prompt):
req = urllib.request.Request(
"https://api.openai.com/v1/chat/completions",
data=json.dumps({
"model":"gpt-4.1-mini",
"messages":[
{"role":"system","content":"You are a seasoned poker/crypto writer."},
{"role":"user","content": prompt}
],
"temperature":0.7
}).encode(),
headers={"Content-Type":"application/json","Authorization":f"Bearer {OPENAI_API_KEY}"}
)
with urllib.request.urlopen(req) as r:
resp = json.loads(r.read().decode())
return resp["choices"][0]["message"]["content"]


def write_post(topic):
title = topic.title()
prompt = f"""Write a practical, honest 900-1200 word article titled "{title}" for {BRAND}.
Include step-by-step bullets, mini checklists, cautions (fees/KYC/security), and a short poker example hand.
Avoid hype. Be clear about risk. Insert a strong call-to-action near the top and bottom: {ref_url()}"""
body = openai_chat(prompt)
body = f"{cta_block()}\n{body}\n{cta_block()}"
path = pathlib.Path("posts"); path.mkdir(exist_ok=True)
fn = path / f"{datetime.date.today().isoformat()}-{slugify(title)}.md"
fm = front_matter(title, f"{title} — explained clearly.", ["poker","crypto","coinpoker"])
fn.write_text(fm + "\n" + body, encoding="utf-8")
print("Wrote:", fn)


if __name__ == "__main__":
for t in TOPICS:
write_post(t)