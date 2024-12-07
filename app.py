import os
from flask import Flask, request, jsonify, render_template, send_from_directory
import subprocess


# 上传文件夹和结果文件夹路径
UPLOAD_FOLDER = 'F:/yolov5/yolov5/web/web/uploads'
RUNS_FOLDER = './runs/detect'
app = Flask(__name__,
            template_folder=os.path.join(os.getcwd(), 'web', 'web', 'templates'),  # 模板文件夹
            static_folder=os.path.join(os.getcwd(), 'web', 'web', 'static'))  # 静态文件夹

os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # 如果文件夹不存在则创建

@app.route('/')
def index():
    """渲染 index.html 页面"""
    return render_template('index.html')

@app.route('/upload')
def upload_page():
    """渲染上传页面"""
    return render_template('page_upload.html')

@app.route('/instruction')
def instruction():
    """渲染上传页面"""
    return render_template('instruction.html')
@app.route('/page2')
def page2():
    """渲染上传页面"""
    return render_template('page2.html')
@app.route('/data-set')
def data_set():
    """渲染上传页面"""
    return render_template('data-set.html')
@app.route('/about')
def about():
    """渲染上传页面"""
    return render_template('about.html')
@app.route('/historical-record')
def historical_record():
    """渲染上传页面"""
    return render_template('historical-record.html')
@app.route('/aj13-page1')
def aj13_page1():
    """渲染上传页面"""
    return render_template('aj13-page1.html')
@app.route('/aj3-page1')
def aj3_page1():
    """渲染上传页面"""
    return render_template('aj3-page1.html')
@app.route('/aj4-page1')
def aj4_page1():
    """渲染上传页面"""
    return render_template('aj4-page1.html')
@app.route('/aj2-page1')
def aj2_page1():
    """渲染上传页面"""
    return render_template('aj2-page1.html')
@app.route('/aj11-page1')
def aj11_page1():
    """渲染上传页面"""
    return render_template('aj11-page1.html')
@app.route('/aj13')
def aj13():
    """渲染上传页面"""
    return render_template('aj13.html')
@app.route('/aj11')
def aj11():
    """渲染上传页面"""
    return render_template('aj11.html')
@app.route('/aj2')
def aj2():
    """渲染上传页面"""
    return render_template('aj2.html')
@app.route('/aj3')
def aj3():
    """渲染上传页面"""
    return render_template('aj3.html')
@app.route('/aj4')
def aj4():
    """渲染上传页面"""
    return render_template('aj4.html')
@app.route('/upload_file', methods=['POST'])
def upload_file():
    """处理文件上传"""
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "没有选择文件"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "文件名为空"})

    try:
        # 保存文件并返回文件路径
        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(save_path)
        return jsonify({"success": True, "file_path": f'F:/yolov5/yolov5/web/web/uploads/{file.filename}'})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})




from flask import send_file

@app.route('/static/result/<path:filename>')
def serve_video(filename):
    filepath = os.path.join('web', 'web', 'static', 'result', filename)
    try:
        return send_file(filepath, mimetype='video/mp4')
    except FileNotFoundError:
        return "文件未找到", 404


import os
import shutil
import time
import re
from flask import jsonify



@app.route('/run-detect', methods=['POST'])
def run_detect():
    try:
        result = subprocess.run(
            ['python', 'detect_test.py'],
            capture_output=True, text=True, encoding='utf-8'
        )

        if result.returncode == 0:
            output_lines = result.stdout.strip().split('\n')
            last_line = output_lines[-2].strip()
            match = re.search(r"您上传的图片/视频中出现了: (.+)", last_line)
            recognized_text = match.group(1) if match else "未识别到内容"

            exp_folders = [f for f in os.listdir(RUNS_FOLDER) if f.startswith('exp')]
            latest_exp_folder = max(exp_folders, key=lambda f: os.path.getmtime(os.path.join(RUNS_FOLDER, f)))

            processed_file_folder = os.path.join(RUNS_FOLDER, latest_exp_folder)

            timeout = 60
            start_time = time.time()
            processed_files = []

            while not processed_files and time.time() - start_time < timeout:
                processed_files = [f for f in os.listdir(processed_file_folder) if
                                   f.endswith('.jpg') or f.endswith('.png') or f.endswith('.mp4')]
                try:
                    if processed_files:
                        with open(os.path.join(processed_file_folder, processed_files[-1]), 'rb'):
                            break
                except IOError:
                    processed_files = []
                time.sleep(1)

            if processed_files:
                static_result_folder = os.path.join(os.getcwd(), 'web', 'web', 'static', 'result')
                os.makedirs(static_result_folder, exist_ok=True)
                target_file_path = os.path.join(static_result_folder, processed_files[-1])

                shutil.copy(os.path.join(processed_file_folder, processed_files[-1]), target_file_path)
                relative_file_path = f"result/{processed_files[-1]}"

                return jsonify({
                    "success": True,
                    "result": recognized_text,
                    "processed_file": relative_file_path
                })
            else:
                return jsonify({"success": False, "error": "未找到处理后的文件，超时未生成"})
        else:
            return jsonify({"success": False, "error": result.stderr.strip()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})


@app.route('/result')
def result_page():
    """显示识别结果和处理后的图片"""
    result = request.args.get('result', '未识别到结果')
    processed_file = request.args.get('processed_file', '')

    return render_template('result.html', result=result, processed_file=processed_file)


@app.template_filter('endswith')
def endswith_filter(value, suffix):
    return value.endswith(suffix)

app.jinja_env.filters['endswith'] = endswith_filter

@app.route('/runs/detect/<path:filename>')
def get_processed_file(filename):
    """提供处理后的文件供前端访问"""
    return send_from_directory('runs/detect', filename)

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)
