import os
import atexit
import shutil
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
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
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size (increased for larger MIDI files)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# Ensure directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def cleanup_output_files():
    """Delete all output files when server shuts down"""
    try:
        output_folder = app.config['OUTPUT_FOLDER']
        if os.path.exists(output_folder):
            for filename in os.listdir(output_folder):
                file_path = os.path.join(output_folder, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Cleaned up output file: {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")
        print("Output files cleanup completed")
    except Exception as e:
        print(f"Error during cleanup: {e}")

def cleanup_upload_files():
    """Delete all upload files when server shuts down"""
    try:
        upload_folder = app.config['UPLOAD_FOLDER']
        if os.path.exists(upload_folder):
            for filename in os.listdir(upload_folder):
                file_path = os.path.join(upload_folder, filename)
                try:
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                        print(f"Cleaned up upload file: {filename}")
                except Exception as e:
                    print(f"Error deleting {filename}: {e}")
        print("Upload files cleanup completed")
    except Exception as e:
        print(f"Error during cleanup: {e}")

# Register cleanup functions to run on server shutdown
atexit.register(cleanup_output_files)
atexit.register(cleanup_upload_files)

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
        note_agent_result = note_agent.run(roles, features)
        
        # Extract assignments and explanations
        if isinstance(note_agent_result, dict) and "assignments" in note_agent_result:
            assignments = note_agent_result["assignments"]
            explanations = note_agent_result.get("explanations", {})
        else:
            # Fallback for old format
            assignments = note_agent_result
            explanations = {}
        
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
        
        # Store results - use file reference instead of full content in session
        # (Flask sessions are cookie-based with 4KB limit, can't store large MusicXML)
        download_url = f'/download/{output_filename}'
        
        # Store only metadata in session (small data)
        session['output_filename'] = output_filename
        session['instruments'] = instruments
        session['tempo'] = round(tempo, 2)
        session['download_url'] = download_url
        session['explanations'] = explanations  # Store Gemini's explanations
        
        # Mark session as modified to ensure it's saved
        session.modified = True
        
        # Clean up uploaded file
        os.remove(filepath)
        
        print(f"Session stored - filename: {output_filename}, instruments: {instruments}, tempo: {tempo}")
        
        return jsonify({
            'success': True,
            'redirect_url': '/results',  # Use absolute path
            'musicxml': musicxml_content,  # Still send in response for preview
            'instruments': instruments,
            'tempo': round(tempo, 2),
            'download_url': download_url
        })
    
    except Exception as e:
        # Clean up on error
        if 'filepath' in locals() and os.path.exists(filepath):
            os.remove(filepath)
        
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/results')
def results():
    """Display results page with orchestration data"""
    # Get file reference from session
    output_filename = session.get('output_filename', '')
    instruments = session.get('instruments', [])
    tempo = session.get('tempo', 0)
    download_url = session.get('download_url', '')
    explanations = session.get('explanations', {})
    
    # Debug: Check what's in session
    print(f"Results page - Session keys: {list(session.keys())}")
    print(f"Results page - output_filename: {output_filename}")
    print(f"Results page - instruments: {instruments}, tempo: {tempo}")
    print(f"Results page - explanations: {explanations}")
    
    if not output_filename:
        # If no file reference in session, redirect to home
        print("WARNING: No output_filename in session, redirecting to index")
        return redirect(url_for('index'))
    
    # Verify file exists (don't read it - too large for template)
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    if not os.path.exists(filepath):
        print(f"WARNING: File not found: {filepath}, redirecting to index")
        return redirect(url_for('index'))
    
    # Don't read the MusicXML file - it's too large and causes lag
    # Just pass empty string since we removed the preview section
    return render_template('results.html', 
                         musicxml='',  # Empty - preview removed for performance
                         instruments=instruments,
                         tempo=tempo,
                         download_url=download_url,
                         explanations=explanations)

@app.route('/download/<filename>')
def download(filename):
    """
    Download the generated MusicXML file using streaming for large files.
    Similar to how Google Drive handles large downloads.
    """
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
    
    if os.path.exists(filepath):
        # Get file size for proper headers
        file_size = os.path.getsize(filepath)
        
        # Use streaming for large files (like Google Drive does)
        def generate():
            with open(filepath, 'rb') as f:
                # Stream in chunks to handle large files efficiently
                chunk_size = 8192  # 8KB chunks
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
        
        from flask import Response
        response = Response(
            generate(),
            mimetype='application/xml',
            headers={
                'Content-Disposition': f'attachment; filename=orchestral_score.musicxml',
                'Content-Type': 'application/xml; charset=utf-8',
                'Content-Length': str(file_size),
                'Accept-Ranges': 'bytes',  # Support for range requests
            }
        )
        return response
    else:
        # Fallback: try to get filename from session and read file
        output_filename = session.get('output_filename', '')
        if output_filename:
            fallback_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            if os.path.exists(fallback_path):
                return send_file(
                    fallback_path,
                    as_attachment=True,
                    download_name='orchestral_score.musicxml',
                    mimetype='application/xml'
                )
        return jsonify({
            'success': False,
            'error': 'File not found'
        }), 404

@app.route('/download-blob')
def download_blob():
    """Alternative download endpoint that streams MusicXML from file"""
    output_filename = session.get('output_filename', '')
    if not output_filename:
        return jsonify({
            'success': False,
            'error': 'No MusicXML file available'
        }), 404
    
    filepath = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
    if not os.path.exists(filepath):
        return jsonify({
            'success': False,
            'error': 'File not found'
        }), 404
    
    # Stream from file
    return send_file(
        filepath,
        as_attachment=True,
        download_name='orchestral_score.musicxml',
        mimetype='application/xml'
    )

if __name__ == '__main__':
    try:
        print("Starting MIDI Converter server...")
        print(f"Upload limit: {app.config['MAX_CONTENT_LENGTH'] / (1024*1024):.0f}MB")
        print("Cleanup registered: Output files will be deleted on server shutdown")
        app.run(debug=True, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        print("\nServer shutting down...")
        cleanup_output_files()
        cleanup_upload_files()
    except Exception as e:
        print(f"Server error: {e}")
        cleanup_output_files()
        cleanup_upload_files()
        raise

