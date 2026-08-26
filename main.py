import os, telebot, tempfile, whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
model = whisper.load_model("base")

# මේ Line එක තමයි Font Problem එක හදන්නේ
FONT_PATH = os.path.join(os.path.dirname(__file__), "NotoSansSinhala.ttf")

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Video එකක් එවන්න Boss ✔ Subtitle දලා දෙන්නම්")

@bot.message_handler(content_types=['video', 'document'])
def handle_video(m):
    msg = bot.reply_to(m, "⏳ Download කරනවා...")
    try:
        file_info = bot.get_file(m.video.file_id if m.video else m.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_video.write(downloaded_file)
        temp_video.close()
        
        bot.reply_to(m, "🎤 Audio එකෙන් Text ගන්නවා...")
        result = model.transcribe(temp_video.name, language="si")
        
        bot.reply_to(m, "✍️ Subtitle දානවා...")
        video = VideoFileClip(temp_video.name)
        subtitles = []
        
        for segment in result["segments"]:
            txt = TextClip(segment["text"], fontsize=40, font=FONT_PATH, color='white', stroke_color='black', stroke_width=2, method='caption', size=(video.w*0.9, None)).set_position('center').set_start(segment["start"]).set_duration(segment["end"] - segment["start"])
            subtitles.append(txt)
            
        final = CompositeVideoClip([video] + subtitles)
        final.write_videofile("output.mp4", codec="libx264")
        
        bot.send_video(m.chat.id, open("output.mp4", "rb"))
        bot.reply_to(m, "✅ ඉවරයි Boss")
        
    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

print("Bot is running...")
bot.polling()
import os, telebot, tempfile, whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
model = whisper.load_model("base")

# මේ Line එක තමයි Font Problem එක හදන්නේ
FONT_PATH = os.path.join(os.path.dirname(__file__), "NotoSansSinhala.ttf")

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "Video එකක් එවන්න Boss ✔ Subtitle දලා දෙන්නම්")

@bot.message_handler(content_types=['video', 'document'])
def handle_video(m):
    msg = bot.reply_to(m, "⏳ Download කරනවා...")
    try:
        file_info = bot.get_file(m.video.file_id if m.video else m.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        temp_video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
        temp_video.write(downloaded_file)
        temp_video.close()
        
        bot.reply_to(m, "🎤 Audio එකෙන් Text ගන්නවා...")
        result = model.transcribe(temp_video.name, language="si")
        
        bot.reply_to(m, "✍️ Subtitle දානවා...")
        video = VideoFileClip(temp_video.name)
        subtitles = []
        
        for segment in result["segments"]:
            txt = TextClip(segment["text"], fontsize=40, font=FONT_PATH, color='white', stroke_color='black', stroke_width=2, method='caption', size=(video.w*0.9, None)).set_position('center').set_start(segment["start"]).set_duration(segment["end"] - segment["start"])
            subtitles.append(txt)
            
        final = CompositeVideoClip([video] + subtitles)
        final.write_videofile("output.mp4", codec="libx264")
        
        bot.send_video(m.chat.id, open("output.mp4", "rb"))
        bot.reply_to(m, "✅ ඉවරයි Boss")
        
    except Exception as e:
        bot.reply_to(m, f"Error: {e}")

print("Bot is running...")
bot.polling()
import os, telebot, tempfile, whisper
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
model = whisper.load_model("base")
FONT_PATH = "NotoSansSinhala.ttf"

@bot.message_handler(commands=['start'])
def start(m): 
    bot.reply_to(m, "Video එකක් එවන්න Boss ✅ Subtitle දාලා දෙන්නම්")

@bot.message_handler(content_types=['video', 'document'])
def handle_video(m):
    try:
        msg = bot.reply_to(m, "⏳ Download කරනවා...")
        file_info = bot.get_file(m.video.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp: 
            tmp.write(downloaded_file); video_path = tmp.name
        
        bot.edit_message_text("🎙️ Subtitle හදනවා...", msg.chat.id, msg.message_id)
        result = model.transcribe(video_path, language="si")
        
        bot.edit_message_text("🎬 Burn කරනවා...", msg.chat.id, msg.message_id)
        video = VideoFileClip(video_path); clips = [video]
        for seg in result["segments"]:
            if seg["text"].strip():
                txt = TextClip(seg["text"], fontsize=38, font=FONT_PATH, color='white', stroke_color='black', stroke_width=2, size=(video.w*0.9, None))
                txt = txt.set_position(('center','bottom')).set_start(seg["start"]).set_end(seg["end"]); clips.append(txt)
        
        output_path = video_path.replace(".mp4", "_sub.mp4")
        CompositeVideoClip(clips).write_videofile(output_path, codec="libx264", audio_codec="aac")
        bot.send_video(m.chat.id, open(output_path, "rb"), caption="ඉවරයි ✅")
        os.remove(video_path); os.remove(output_path)
    except Exception as e:
        bot.reply_to(m, f"Error: {e}")
bot.polling(none_stop=True)