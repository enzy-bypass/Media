import os
import tempfile
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip

def download_media(url, format_type, cookie_text=None, audio_quality="192", save_dir="downloads"):
    """Hàm tách biệt chuyên xử lý tải media từ link và bypass bot"""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    cookie_file_path = None
    try:
        # Nếu người dùng có cấu hình Cookie ở mục Cài đặt, hệ thống sẽ kích hoạt để bypass bot
        if cookie_text and cookie_text.strip():
            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt') as tfile:
                tfile.write(cookie_text.strip())
                cookie_file_path = tfile.name

        outtmpl = os.path.join(save_dir, '%(title)s.%(ext)s')
        
        # Cấu hình luồng client tổng hợp tinh vi để giảm thiểu quét bot
        ydl_opts = {
            'outtmpl': outtmpl,
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'web_embedded']
                }
            },
            'nocheckcertificate': True,
            'quiet': True,
            'no_warnings': True
        }
        
        if cookie_file_path:
            ydl_opts['cookiefile'] = cookie_file_path
        
        if format_type == "mp3":
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': str(audio_quality),
                }],
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            })
            
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if format_type == "mp3":
                filename = os.path.splitext(filename)[0] + '.mp3'
            
            return filename, None
    except Exception as e:
        return None, str(e)
    finally:
        if cookie_file_path and os.path.exists(cookie_file_path):
            try:
                os.remove(cookie_file_path)
            except:
                pass

def convert_mp4_to_mp3(uploaded_file, save_dir="downloads"):
    """Hàm chuyên đổi đuôi video sang tệp âm thanh"""
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        
    try:
        input_path = os.path.join(save_dir, uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        output_filename = os.path.splitext(uploaded_file.name)[0] + ".mp3"
        output_path = os.path.join(save_dir, output_filename)
        
        video = VideoFileClip(input_path)
        video.audio.write_audiofile(output_path, logger=None)
        video.close()
        
        os.remove(input_path)
        return output_path, None
    except Exception as e:
        return None, str(e)
                  
