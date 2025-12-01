from flask import Flask, jsonify, request
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "Saavnify YT Backend LIVE"})

@app.route("/audio")
def get_audio():
    video_id = request.args.get("id")
    if not video_id:
        return jsonify({"error": "Missing id"}), 400

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://youtube.com/watch?v={video_id}", download=False)
            
            # Best audio format dhund le
            formats = info.get('formats', [])
            best_audio = None
            for f in formats:
                if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                    if not best_audio or (f.get('abr', 0) > best_audio.get('abr', 0)):
                        best_audio = f

            if not best_audio:
                audio_url = info.get('url')
            else:
                audio_url = best_audio['url']

            return jsonify({
                "title": info.get('title', 'Unknown Title'),
                "singers": info.get('uploader', 'Unknown Artist'),
                "image_url": info.get('thumbnail', ''),
                "url": audio_url,
                "duration": info.get('duration', 0),
                "source": "yt-audio"
            })

    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e), "fallback": "use_iframe"}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)