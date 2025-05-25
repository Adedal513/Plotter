import pandas as pd
import tempfile
import matplotlib.pyplot as plt
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from bot.plotting import plot_histogram

# Стейты ConversationHandler
ASK_COLUMN = 1

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "👋 Привет! Я бот для анализа CSV-файлов.\n\n"
        "Отправь мне .csv — и я покажу структуру данных, а затем предложу действия."
    )
    await update.message.reply_text(msg)

async def handle_csv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if not document.file_name.endswith(".csv"):
        await update.message.reply_text("Пожалуйста, отправьте файл с расширением `.csv`.")
        return

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp:
        path = tmp.name
        file = await context.bot.get_file(document.file_id)
        await file.download_to_drive(path)

    try:
        df = pd.read_csv(path)
        context.user_data["df"] = df

        info = "**🧾 Обнаружены столбцы:**\n\n"
        for col in df.columns:
            info += f"- `{col.strip()}`: `{df[col].dtype}`\n"

        # Кнопки
        keyboard = [
            [InlineKeyboardButton("📊 Построить гистограмму", callback_data="histogram")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(info, parse_mode="Markdown")
        await update.message.reply_text("Выберите, что сделать с данными:", reply_markup=reply_markup)

    except Exception as e:
        await update.message.reply_text(f"⚠️ Не удалось прочитать CSV: {e}")


# Обработка кнопки "Гистограмма"
async def option_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "histogram":
        await query.edit_message_text("Введите название столбца для построения гистограммы:")
        return ASK_COLUMN


# Обработка названия столбца
async def column_input_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    column = update.message.text.strip()
    df = context.user_data.get("df")

    if df is None or column not in df.columns:
        await update.message.reply_text("Такой столбец не найден. Попробуйте снова.")
        return ASK_COLUMN

    try:
        # Построим график
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp_img:
            plot_histogram(df, column, tmp_img.name)
            await update.message.reply_photo(photo=open(tmp_img.name, "rb"), caption=f"Гистограмма по столбцу `{column}`", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"Ошибка при построении графика: {e}")

    return ConversationHandler.END
