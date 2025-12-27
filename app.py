import os
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from agents.midi_analysis_agent import MIDIAnalysisAgent
from agents.role_assignment_agent import RoleAssignmentAgent
from agents.note_assignment_agent import NoteAssignmentAgent
from agents.feature_extraction_agent import FeatureExtractionAgent
from utils.score_renderer import render_score

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'mid', 'midi'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({
            'success': False,
            'error': 'No file uploaded'
        }), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            'success': False,
            'error': 'No file selected'
        }), 400
    
    if not allowed_file(file.filename):
        return jsonify({
            'success': False,
            'error': 'Invalid file type. Please upload a .mid or .midi file.'
        }), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Initialize agents
        midi_agent = MIDIAnalysisAgent()
        role_agent = RoleAssignmentAgent()
        note_agent = NoteAssignmentAgent()
        feature_agent = FeatureExtractionAgent()
        
        # Run conversion pipeline
        notes, tempo = midi_agent.run(filepath)
        melody, harmony, bass = role_agent.run(notes)
        roles = {
            "Melody": melody,
            "Harmony": harmony,
            "Bass": bass
        }
        features = feature_agent.run(roles, tempo)
        assignments = note_agent.run(roles, features)
        
        # Generate unique output filename
        output_filename = f"orchestral_score_{os.urandom(8).hex()}.musicxml"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
        
        # Render score
        render_score(assignments, tempo, output_path)
        
        # Read the generated MusicXML
        with open(output_path, 'r', encoding='utf-8') as f:
            musicxml_content = f.read()
        
        # Get instrument list
        instruments = list(assignments.keys())
        
        # Clean up uploaded file
        os.remove(filepath)
        
        return jsonify({
            'success': True,
            'musicxml': musicxml_content,
            'instruments': instruments,
            'tempo': round(tempo, 2),
            'download_url': f'/download/{output_filename}'
        })
    
    except Exception as e:
        # Clean up on error
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name='orchestral_score.musicxml')
    else:
        flash('File not found')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

