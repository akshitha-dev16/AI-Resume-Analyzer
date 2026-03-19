import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from utils.parser import parse_resume
from openai import OpenAI
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Create uploads folder if not exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize OpenAI client (API Key pre-configured in environment)
client = OpenAI()

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Parse the resume
        parsed_text = parse_resume(file_path)
        
        # Call OpenAI for analysis
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {"role": "system", "content": "You are a professional HR and ATS expert. Analyze the following resume text and provide a JSON response with 'summary', 'skills_identified', 'strengths', 'weaknesses', and 'ats_score' (out of 100)."},
                    {"role": "user", "content": parsed_text}
                ],
                response_format={"type": "json_object"}
            )
            analysis = json.loads(response.choices[0].message.content)
            
            # Clean up uploaded file
            os.remove(file_path)
            
            return jsonify({
                "status": "success",
                "filename": filename,
                "analysis": analysis
            })
            
        except Exception as e:
            return jsonify({"error": f"AI Analysis failed: {str(e)}"}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to AI Resume Analyzer API. Use /analyze (POST) to upload and analyze resumes."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
