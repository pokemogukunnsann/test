from flask import Flask, jsonify, request, redirect, send_from_directory
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)

# CORSを設定（すべてのオリジン、GETとPOSTメソッドを許可）
CORS(app, origins='*', methods=['GET', 'POST'])

# index.htmlをstaticディレクトリから返す設定
@app.route('/')
def serve_index():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'index.html')

# nanikaは省略可能にする（<nanika>はデフォルト値'videos'を使用）
@app.route('/channel/<channelid>/', defaults={'nanika': 'videos'}, methods=['GET', 'POST'])
@app.route('/channel/<channelid>/<nanika>', methods=['GET', 'POST'])
def get_channel_data(channelid, nanika):
    youtube_url = f'https://www.youtube.com/channel/{channelid}/{nanika}?app=desktop'

    if request.method == 'GET':
        try:
            # curlでHTMLを取得
            result = subprocess.run(['curl', '-s', youtube_url], capture_output=True, text=True, check=True)
            html_content = result.stdout
        except subprocess.CalledProcessError as e:
            return jsonify({'error': 'Failed to fetch data from YouTube'}), 500
        
        return html_content

    # POSTメソッドでの処理（必要なら実装）
    elif request.method == 'POST':
        data = request.json  # JSONデータを受け取る
        return jsonify({'message': 'POST request received', 'data': data}), 200


@app.route('/playlist', methods=['GET', 'POST'])
def get_playlist_data():
    playlist_id = request.args.get('list')  # クエリパラメータからplaylistIDを取得
    if not playlist_id:
        return jsonify({'error': 'Playlist ID is required'}), 400

    youtube_url = f'https://inv.nadeko.net/playlist?list={playlist_id}'

    if request.method == 'GET':
        try:
            # curlでHTMLを取得
            result = subprocess.run(['curl', '-s', youtube_url], capture_output=True, text=True, check=True)
            html_content = result.stdout
        except subprocess.CalledProcessError as e:
            return jsonify({'error': 'Failed to fetch data from YouTube'}), 500
        
        return html_content

    # POSTメソッドでの処理（必要なら実装）
    elif request.method == 'POST':
        data = request.json  # JSONデータを受け取る
        return jsonify({'message': 'POST request received', 'data': data}), 200


#  url_for

@app.route('/search', methods=['GET'])
def search_redirect():
    search_query = request.args.get('q')
    if search_query:
        # https://pokemogukunnsann.github.io/v/search?q=検索ワード にリダイレクト
        return redirect(f'https://pokemogukunnsann.github.io/v/search?q={search_query}')
    else:
        return jsonify({'error': 'Search query is required'}), 400


@app.route('/watch', methods=['GET'])
def watch_redirect():
    video_id = request.args.get('v')
    if video_id:
        # https://pokemogukunnsann.github.io/v/watch?q=videoid にリダイレクト
        return redirect(f'https://pokemogukunnsann.github.io/v/watch?q={video_id}')
    else:
        return jsonify({'error': 'Video ID is required'}), 400

if __name__ == '__main__':
    app.run(debug=True)
