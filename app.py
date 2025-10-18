import os
import io
import tempfile
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import librosa
import soundfile as sf
import noisereduce as nr
import numpy as np
from werkzeug.utils import secure_filename
from zipfile import ZipFile

app = Flask(__name__)
CORS(app)

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max file size
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Supported audio formats
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'flac', 'm4a', 'aac', 'ogg', 'wma'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_audio(input_path, output_path, noise_reduction_level=0.8):
    """
    Process audio file to remove background noise
    """
    try:
        # Check if input file exists
        if not os.path.exists(input_path):
            return False, "Input file not found"
        
        # Load audio file
        audio_data, sample_rate = librosa.load(input_path, sr=None)
        
        # Check if audio data is valid
        if len(audio_data) == 0:
            return False, "Audio file appears to be empty"
        
        # Apply noise reduction
        reduced_noise = nr.reduce_noise(
            y=audio_data, 
            sr=sample_rate,
            stationary=True,
            prop_decrease=noise_reduction_level
        )
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Save processed audio
        sf.write(output_path, reduced_noise, sample_rate)
        
        # Verify output file was created
        if not os.path.exists(output_path):
            return False, "Failed to create output file"
        
        return True, None
        
    except librosa.util.exceptions.NoBackendError:
        return False, "Audio backend not available. Please install ffmpeg."
    except Exception as e:
        return False, f"Audio processing error: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Detect batch upload
        num_files = int(request.form.get('num_files', '1'))
        files = []
        if num_files > 1:
            # Batch upload
            for k in range(num_files):
                myfile = request.files.get(f'file{k}', None)
                if myfile: files.append(myfile)
            if not files:
                return jsonify({'success': False, 'error': 'No files provided'}), 400
        else:
            # Single upload fallback
            a_file = request.files.get('file') or next(iter(request.files.values()), None)
            if a_file: files.append(a_file)
            else:
                return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        # Read noise level
        try:
            noise_level = float(request.form.get('noise_level', 0.8))
            noise_level = max(0.1, min(1.0, noise_level))
        except (ValueError, TypeError):
            noise_level = 0.8
        
        input_paths, output_paths, output_names = [], [], []
        try:
            for file in files:
                if file.filename == '': continue
                if not allowed_file(file.filename): continue
                filename = secure_filename(file.filename)
                input_path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(input_path)
                name, ext = os.path.splitext(filename)
                output_name = f"{name}_denoised{ext}"
                output_path = os.path.join(OUTPUT_FOLDER, output_name)
                succ, err = process_audio(input_path, output_path, noise_level)
                if succ:
                    output_paths.append(output_path)
                    output_names.append(output_name)
                input_paths.append(input_path)
            # Clean up uploaded files
            for p in input_paths:
                if os.path.exists(p):
                    try: os.remove(p)
                    except: pass
        except Exception as e:
            return jsonify({'success': False, 'error': f'Processing failed: {str(e)}'}), 500
        
        # Respond with one file or a zip
        if len(output_paths) == 0:
            return jsonify({'success': False, 'error': f'No files processed successfully.'}), 500
        if len(output_paths) == 1:
            # Single file logic (as before)
            output_filename = output_names[0]
            return jsonify({
                'success': True,
                'output_filename': output_filename,
                'download_url': f'/download/{output_filename}'
            })
        else:
            # Multiple: zip all outputs
            import time
            zip_name = f"denoised_outputs_{int(time.time())}.zip"
            zip_path = os.path.join('outputs', zip_name)
            with ZipFile(zip_path, 'w') as zipf:
                for file, arcname in zip(output_paths, output_names):
                    if os.path.exists(file):
                        zipf.write(file, arcname)
            # Optional: Clean up output files after zipping
            for file in output_paths:
                try: os.remove(file)
                except: pass
            return jsonify({
                'success': True,
                'zip_url': f'/download_zip/{zip_name}',
                'zip_name': zip_name
            })
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({'success': False, 'error': f'Upload failed: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(OUTPUT_FOLDER, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=filename)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/download_zip/<zipname>')
def download_zip(zipname):
    try:
        file_path = os.path.join(OUTPUT_FOLDER, zipname)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True, download_name=zipname)
        else:
            return jsonify({'error': 'ZIP not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Download failed: {str(e)}'}), 500

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
