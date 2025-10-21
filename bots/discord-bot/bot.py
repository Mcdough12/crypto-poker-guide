import os, re
import discord
from discord.ext import commands
from datetime import datetime


REF_BASE = "https://record.coinpokeraffiliates.com/_W8N9Np6OF21fWQTENI37dGNd7ZgqdRLk/1/"


def ref_url(source="discord", medium="bot"):
from urllib.parse import urlencode
q = urlencode({
"utm_source": source,
"utm_medium": medium,
"utm_campaign": "coinpoker"
})
return f"{REF_BASE}?{q}"


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)


INTRO = (
"Hey! I’m your crypto‑poker concierge. I can:\n"
"• Explain CoinPoker basics (deposits, rakeback, KYC)\n"
"• Do bankroll math (e.g., `!bankroll 1200 2%`)\n"
f"• Drop the signup link: {ref_url()}\n"
"_Affiliate disclosure: I may earn a commission if you sign up._"
)


@bot.event
async def on_ready():
print(f"Logged in as {bot.user} at {datetime.utcnow().isoformat()}Z")


@bot.command(name="start")
async def start(ctx):
await ctx.send(INTRO)


@bot.command(name="link")
async def link(ctx):
await ctx.send(f"🚀 Join CoinPoker → {ref_url()}")


@bot.command(name="faq")
async def faq(ctx, *, topic: str = ""):
t = topic.lower().strip()
faqs = {
"deposit": "Deposit USDT/ETH/CHP. Non‑custodial wallets recommended. Basic play without heavy KYC.",
"withdraw": "Withdraw crypto back to your wallet. Usually minutes to an hour depending on chain.",
"rakeback": "Competitive rake with tokenized rakeback; promos vary. Check current offers via the link."
}
if t in faqs:
await ctx.send(f"**{t.title()}** — {faqs[t]}\nSignup: {ref_url()}")
else:
await ctx.send("Try `!faq deposit`, `!faq withdraw`, or `!faq rakeback`.")


@bot.command(name="bankroll")
async def bankroll(ctx, roll: float, pct: str):
m = re.match(r"(\d+(?:\.\d+)?)%$", pct.strip())
if not m:
return await ctx.send("Usage: `!bankroll 1200 2%`")
p = float(m.group(1)) / 100.0
stake = round(roll * p, 2)
await ctx.send(f"Recommended stake at {pct}: **${stake}**. Play smart. Link: {ref_url()}")


@bot.event
async def on_message(message):
if message.author.bot:
return
if bot.user in message.mentions and "link" in message.content.lower():
await message.channel.send(f"Here you go → {ref_url()}")
await bot.process_commands(message)


if __name__ == "__main__":
token = os.environ.get("DISCORD_BOT_TOKEN")
if not token:
raise SystemExit("Missing DISCORD_BOT_TOKEN env var")
bot.run(token)