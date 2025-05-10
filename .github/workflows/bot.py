import os  
import json  
import gspread  
from google.oauth2.service_account import Credentials  
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup  

# Загрузка секретов из GitHub Actions  
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")  
GOOGLE_CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS")  

# Сохраните credentials.json временно  
with open("credentials.json", "w") as f:  
    f.write(GOOGLE_CREDENTIALS_JSON)  

# Подключение к Google Таблицам  
scopes = ["https://www.googleapis.com/auth/spreadsheets "]  
credentials = Credentials.from_service_account_file("credentials.json", scopes=scopes)  
gc = gspread.authorize(credentials)  
sh = gc.open_by_key(SPREADSHEET_ID)  
worksheet = sh.sheet1  

# Получение данных  
data = worksheet.get_all_records()  

# Отправка уведомлений в Telegram  
bot = Bot(token=TELEGRAM_TOKEN)  
for row in data:  
    if row["Статус"] == "новый":  
        message = f"Новый заказ!\nID: {row['ID заказа']}\nКлиент: {row['Имя клиента']}"  
        keyboard = InlineKeyboardButton("Отправить промокод", callback_data=f"promo_{row['ID заказа']}")  
        bot.send_message(  
            chat_id="ВАШ_CHAT_ID",  
            text=message,  
            reply_markup=InlineKeyboardMarkup([[keyboard]])  
        )  
        worksheet.update_cell(row["ID заказа"] + 1, 4, "обработан")  
