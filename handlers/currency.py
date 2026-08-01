"""Telegram currency command handlers."""

from __future__ import annotations

from telegram import Update
from telegram.ext import ContextTypes

from services.currency import CurrencyService


async def currency_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Convert a currency amount using live rates."""

    if update.message is None:
        return

    if len(context.args) < 3:
        await update.message.reply_text("Usage: /fx amount from_currency to_currency")
        return

    try:
        amount = float(context.args[0])
        from_currency = context.args[1]
        to_currency = context.args[2]
        quote = await CurrencyService().convert(amount, from_currency, to_currency)
    except Exception:
        await update.message.reply_text("Could not convert that currency pair")
        return

    await update.message.reply_text(
        f"{quote.amount:.2f} {quote.from_currency} = {quote.converted_amount:.2f} {quote.to_currency}\n"
        f"Rate: {quote.rate:.6f}"
    )
