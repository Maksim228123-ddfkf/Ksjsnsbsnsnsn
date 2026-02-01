import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка
BOT_TOKEN = "7883886140:AAGsubv1LTvUy281XvHG1vsQcjxgsA25EQE"
ADMIN_IDS = [7957374923, 7064142309]  # Вы и второй админ

# Логирование
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Здравствуйте! Меня зовут @ange1chid\n\n"
        "Я создал этого бота для приема сообщений от пользователей. "
        "Это удобный способ связаться с нами, если у вас есть вопросы, предложения "
        "или нужна помощь.\n\n"
        "Также у нас есть менеджер @Glycinefor_pain, который поможет вам "
        "с решением различных вопросов.\n\n"
        "Мы работаем, чтобы быстро отвечать на ваши обращения "
        "и обеспечивать качественную поддержку.\n\n"
        "Просто напишите ваше сообщение ниже, и мы обязательно ответим!"
    )

async def forward_to_admins(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message
    
    # Информация о пользователе
    user_info = (
        f"Новое сообщение от пользователя:\n"
        f"Имя: {user.first_name or 'Не указано'}\n"
        f"ID: {user.id}\n"
        f"Юзернейм: @{user.username if user.username else 'Нет'}\n"
        f"---\n"
    )
    
    try:
        # Отправляем всем админам
        for admin_id in ADMIN_IDS:
            try:
                if message.text:
                    await context.bot.send_message(
                        admin_id, 
                        f"{user_info}Сообщение:\n{message.text}"
                    )
                elif message.photo:
                    await context.bot.send_photo(
                        admin_id,
                        message.photo[-1].file_id,
                        caption=f"{user_info}Фото"
                    )
                elif message.document:
                    await context.bot.send_document(
                        admin_id,
                        message.document.file_id,
                        caption=f"{user_info}Документ"
                    )
                elif message.video:
                    await context.bot.send_video(
                        admin_id,
                        message.video.file_id,
                        caption=f"{user_info}Видео"
                    )
                elif message.audio:
                    await context.bot.send_audio(
                        admin_id,
                        message.audio.file_id,
                        caption=f"{user_info}Аудио"
                    )
                elif message.voice:
                    await context.bot.send_voice(
                        admin_id,
                        message.voice.file_id,
                        caption=f"{user_info}Голосовое сообщение"
                    )
                else:
                    await context.bot.send_message(
                        admin_id,
                        f"{user_info}Другой тип сообщения"
                    )
                
                logging.info(f"Сообщение отправлено админу {admin_id}")
                
            except Exception as e:
                logging.error(f"Ошибка отправки админу {admin_id}: {e}")
        
        # Подтверждение пользователю
        await update.message.reply_text(
            "Ваше сообщение получено и отправлено администраторам! "
            "Мы ответим вам в ближайшее время."
        )
        
    except Exception as e:
        await update.message.reply_text("Произошла ошибка при отправке сообщения. Попробуйте еще раз.")
        logging.error(f"Общая ошибка: {e}")

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Ответ админа"""
    if update.message.reply_to_message and update.message.from_user.id in ADMIN_IDS:
        try:
            text = update.message.reply_to_message.text
            if text and "ID:" in text:
                lines = text.split('\n')
                for line in lines:
                    if "ID:" in line:
                        user_id = int(line.split("ID:")[1].strip())
                        
                        # Отправляем ответ пользователю
                        await context.bot.send_message(
                            user_id,
                            f"Ответ от администратора:\n\n{update.message.text}"
                        )
                        
                        # Уведомляем админа
                        await update.message.reply_text("Ответ отправлен пользователю!")
                        
                        # Уведомляем другого админа об ответе
                        for admin_id in ADMIN_IDS:
                            if admin_id != update.message.from_user.id:
                                try:
                                    admin_name = "@Glycinefor_pain" if admin_id == 7064142309 else "@ange1chid"
                                    await context.bot.send_message(
                                        admin_id,
                                        f"Администратор ответил пользователю ID: {user_id}"
                                    )
                                except:
                                    pass
                        break
        except Exception as e:
            await update.message.reply_text(f"Ошибка: {e}")
            logging.error(f"Ошибка ответа админа: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    
    # Ответы админов
    app.add_handler(MessageHandler(
        filters.TEXT & filters.REPLY & (filters.User(ADMIN_IDS[0]) | filters.User(ADMIN_IDS[1])), 
        admin_reply
    ))
    
    # Все остальные сообщения от пользователей
    app.add_handler(MessageHandler(
        filters.ALL & ~filters.COMMAND & ~filters.User(ADMIN_IDS[0]) & ~filters.User(ADMIN_IDS[1]),
        forward_to_admins
    ))
    
    print("Бот запущен!")
    print(f"Админы: {ADMIN_IDS}")
    print("Напишите /start в Telegram боту")
    print("Ctrl+C для остановки")
    
    app.run_polling()

if __name__ == '__main__':
    main()
