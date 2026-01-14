from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from pdf_parser import PDFParser
from translator import PDFTranslator
from config import Config

# 开发模式：前端在3000端口，后端在5000端口
# 生产模式：前端构建后放在dist目录
if os.path.exists('frontend/dist'):
    app = Flask(__name__, static_folder='frontend/dist', static_url_path='')
else:
    app = Flask(__name__)

CORS(app)  # 允许跨域请求

app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

# 确保上传目录存在
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    if app.static_folder and os.path.exists(os.path.join(app.static_folder, 'index.html')):
        return send_from_directory(app.static_folder, 'index.html')
    else:
        # 开发模式，返回简单提示
        return jsonify({
            'message': '后端API服务运行中',
            'frontend': '请访问 http://localhost:3000 查看前端界面',
            'api_docs': {
                'upload': '/api/upload (POST)',
                'translate': '/api/translate (POST)'
            }
        })

@app.route('/api/upload', methods=['POST'])
@app.route('/upload', methods=['POST'])  # 保持向后兼容
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': '没有文件上传'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '未选择文件'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            # 解析PDF
            parser = PDFParser(filepath)
            pdf_data = parser.extract_text()

            return jsonify({
                'success': True,
                'filename': filename,
                'filepath': filepath,
                'total_pages': pdf_data['total_pages'],
                'pages': pdf_data['pages']
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': '不支持的文件类型'}), 400

@app.route('/api/translate', methods=['POST'])
@app.route('/translate', methods=['POST'])  # 保持向后兼容
def translate():
    data = request.json
    filepath = data.get('filepath')
    page_numbers = data.get('page_numbers', [])  # 可选：指定翻译的页面

    if not filepath:
        return jsonify({'error': '缺少文件路径'}), 400

    try:
        # 解析PDF
        parser = PDFParser(filepath)
        pdf_data = parser.extract_text()

        # 选择要翻译的页面
        if page_numbers:
            pages_to_translate = [p for p in pdf_data['pages'] if p['page'] in page_numbers]
        else:
            pages_to_translate = pdf_data['pages']

        # 翻译
        translator = PDFTranslator()
        translated_pages = translator.translate_pages(pages_to_translate)

        return jsonify({
            'success': True,
            'translated_pages': translated_pages,
            'total_pages': len(translated_pages)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
