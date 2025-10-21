import os, re, logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


logging.basicConfig(level=logging.INFO)


REF_BASE = "https://record.coinpokeraffiliates.com/_W8N9Np6OF21fWQTENI37dGNd7ZgqdRLk/1/"


def ref_url(source="telegram", medium="bot"):
from urllib.parse import urlencode
q = urlencode({
"utm_source": source,
"utm_medium": medium,
"utm_campaign": "coinpoker"
})
return f"{REF_BASE}?{q}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(
f"Welcome! Use /link /faq /bankroll.\nSignup: {ref_url()}\n_Affiliate disclosure._"
)


async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
await update.message.reply_text(f"🚀 {ref_url()}")


async def faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
topic = " ".join(context.args).lower().strip()
mapping = {
"deposit":"USDT/ETH/CHP; non‑custodial wallet recommended.",
"withdraw":"Crypto out; usually minutes to an hour.",
"rakeback":"Tokenized rakeback; promos vary—see link."
}
reply = mapping.get(topic, "Try: /faq deposit, /faq withdraw, /faq rakeback")
await update.message.reply_text(f"{reply}\n\nSignup: {ref_url()}")


async def bankroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
if len(context.args) != 2:
return await update.message.reply_text("Usage: /bankroll 1200 2%")
roll = float(context.args[0])
m = re.match(r"(\d+(?:\.\d+)?)%$", context.args[1])
if not m:
return await update.message.reply_text("Use % like 1% or 2%")
pct = float(m.group(1)) / 100.0
stake = round(roll * pct, 2)
await update.message.reply_text(f"Stake: ${stake} • Link: {ref_url()}")


if __name__ == "__main__":
token = os.environ.get("TELEGRAM_BOT_TOKEN")
if not token:
raise SystemExit("Missing TELEGRAM_BOT_TOKEN env var")
app = ApplicationBuilder().token(token).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("link", link))
app.add_handler(CommandHandler("faq", faq))
app.add_handler(CommandHandler("bankroll", bankroll))
app.run_polling()