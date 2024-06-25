# my_library/app.py
import os
import json
import logging
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
from .utils import allowed_file, encode_image, sanitize_filename
from .db import initialize_database
import openai

def create_app(config):
    app = Flask(__name__)
    app.secret_key = config['FLASK_SECRET_KEY']
    app.config['UPLOAD_FOLDER'] = config['UPLOAD_FOLDER']

    # Ensure the upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Ensure the JSON folder exists
    JSON_FOLDER = config['JSON_FOLDER']
    os.makedirs(JSON_FOLDER, exist_ok=True)

    @app.route('/')
    def upload_form():
        return render_template('upload.html')

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded')
            return redirect(url_for('upload_form'))
        else:
            flash('Allowed file types are png, jpg, jpeg, gif')
            return redirect(request.url)

    @app.route('/ask', methods=['POST'])
    def ask_question():
        try:
            data = request.form.get('data')
            if not data:
                return jsonify({'error': 'No data part'}), 400

            data = json.loads(data)
            question = data.get('question')
            if not question:
                return jsonify({'error': 'Question is required'}), 400

            messages = [
                {"role": "system", "content": config['instructions']},
                {"role": "user", "content": question}
            ]

            images_data = []
            for i in range(1, 3):
                file_key = f'file{i}'
                if file_key in request.files:
                    file = request.files[file_key]
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(file_path)
                        images_data.append(encode_image(file_path))

            if images_data:
                for i, image_data in enumerate(images_data):
                    messages[1]["content"] = [{"type": "text", "text": question},
                                              {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_data}"}}]

            client = openai.OpenAI(api_key=config['api_key'])
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )

            response_text = response.choices[0].message.content

            response_data = {
                'user': question,
                'assistant': response_text,
                'images': images_data
            }

            # Save the response data to a JSON file
            sanitized_question = sanitize_filename(question[:50])
            json_filename = os.path.join(JSON_FOLDER, f"{sanitized_question}.json")
            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump(response_data, json_file, ensure_ascii=False, indent=4)

            return jsonify(response_data)
        except Exception as e:
            logging.error(f"Error during the OpenAI API call: {e}")
            return jsonify({'error': 'An error occurred while processing your request'}), 500

    return app
