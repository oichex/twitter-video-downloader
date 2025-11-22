from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-video', methods=['POST'])
def get_video():
    url = request.form.get('url')

    if not url:
        return jsonify({'error': 'Lütfen bir URL girin.'}), 400

    # yt-dlp ayarları
    ydl_opts = {
        'quiet': True, # Konsolda çok fazla log çıkarmasın
        'no_warnings': True,
        'format': 'best', # En iyi kaliteyi seç
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Videoyu indirmeden sadece bilgisini çekiyoruz (extract_info)
            info = ydl.extract_info(url, download=False)
            
            # Videonun başlığı ve direkt indirme linki
            video_title = info.get('title', 'Twitter Video')
            video_url = info.get('url', None)
            thumbnail = info.get('thumbnail', None)

            if not video_url:
                return jsonify({'error': 'Video bulunamadı.'}), 404

            return jsonify({
                'title': video_title,
                'download_url': video_url,
                'thumbnail': thumbnail
            })

    except Exception as e:
        return jsonify({'error': f'Hata oluştu: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)