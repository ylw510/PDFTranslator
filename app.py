from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
from pdf_parser import PDFParser
from translator import PDFTranslator
from config import Config

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH

# 确保上传目录存在
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
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

@app.route('/translate', methods=['POST'])
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
