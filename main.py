    import telebot
    import whisper
    import moviepy.editor as mp
    import os

    BOT_TOKEN = "8722560855:AAGKsuibEb2U_5ALPHTyJie_vUrBCVhb7YM"
    bot = telebot.TeleBot(BOT_TOKEN)
    print("Loading Whisper Model...")
    model = whisper.load_model("base")
    print("Model Loaded!")

    @bot.message_handler(content_types=['video','voice','audio','document'])
    def handle_audio(message):
        try:
            bot.reply_to(message, "File එක ආවා! Audio හදනවා...")
            file_info = bot.get_file(message.document.file_id if message.document else message.video.file_id if message.video else message.voice.file_id if message.voice else message.audio.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            with open("input.mp4", 'wb') as f: f.write(downloaded_file)
            
            clip = mp.VideoFileClip("input.mp4")
            clip.audio.write_audiofile("output.mp3")
            clip.close()
            
            result = model.transcribe("output.mp3", language="si")
            text = result["text"]
            
            with open("output.mp3", "rb") as audio:
                bot.send_audio(message.chat.id, audio, caption=text[:1000])
            os.remove("input.mp4"); os.remove("output.mp3")
        except Exception as e:
            bot.reply_to(message, f"Error: {e}")

    bot.infinity_polling()
