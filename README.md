# BG Noise Remover 🎵

A powerful web-based audio denoising tool that removes background noise from audio files using AI-powered noise reduction algorithms.

## Features

- **Multi-format Support**: Supports WAV, MP3, FLAC, M4A, AAC, OGG, and WMA audio formats
- **Adjustable Noise Reduction**: Customizable noise reduction levels (10% - 100%)
- **Web Interface**: Beautiful, responsive web interface with drag-and-drop functionality
- **Real-time Processing**: Fast audio processing with progress indicators
- **High Quality Output**: Preserves original audio quality while removing unwanted noise

## Installation

1. **Clone or download this project**
   ```bash
   cd "BG Noise Remover"
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   Navigate to `http://localhost:5000`

## Usage

1. **Upload Audio**: Click the upload area or drag & drop your audio file
2. **Adjust Settings**: Use the slider to set the noise reduction level (recommended: 80%)
3. **Process**: Click "Process Audio" and wait for the processing to complete
4. **Download**: Download your cleaned audio file

## Supported Audio Formats

- WAV (Waveform Audio File Format)
- MP3 (MPEG Audio Layer III)
- FLAC (Free Lossless Audio Codec)
- M4A (MPEG-4 Audio)
- AAC (Advanced Audio Coding)
- OGG (Ogg Vorbis)
- WMA (Windows Media Audio)

## Technical Details

- **Backend**: Flask (Python web framework)
- **Audio Processing**: librosa and noisereduce libraries
- **Noise Reduction**: Spectral gating and stationary noise reduction
- **Maximum File Size**: 100MB
- **Processing**: Server-side audio processing for optimal quality

## Troubleshooting

### Common Issues

1. **File Upload Errors**: Ensure your audio file is in a supported format and under 100MB
2. **Processing Errors**: Try reducing the noise reduction level or check if the audio file is corrupted
3. **Slow Processing**: Large files or high noise reduction levels may take longer to process

### System Requirements

- Python 3.7 or higher
- At least 2GB RAM
- Sufficient disk space for temporary file processing

## API Endpoints

- `GET /` - Main web interface
- `POST /upload` - Upload and process audio file
- `GET /download/<filename>` - Download processed audio file
- `GET /health` - Health check endpoint

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests!
