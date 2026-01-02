# MyAIPlug Audio Converter

High quality audio format converter with support for multiple formats and comprehensive conversion options.

## Features

- 🎵 **Multiple Format Support**: Convert between MP3, WAV, OGG, FLAC, and M4A
- ⚙️ **Flexible Options**: Control bitrate, sample rate, and channel configuration
- 🖥️ **CLI Interface**: Easy-to-use command-line interface
- 📊 **Audio Info**: Get detailed information about audio files
- 🔒 **Robust Error Handling**: Comprehensive validation and error messages
- 🧪 **Well Tested**: Comprehensive test suite with unit and integration tests
- 📦 **Easy Installation**: Simple pip installation with minimal dependencies

## Installation

### Requirements

- Python 3.8 or higher
- FFmpeg (required by pydub for audio processing)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH.

### Install MyAIPlug Audio Converter

```bash
pip install -r requirements.txt
pip install -e .
```

## Usage

### Command Line Interface

#### Convert Audio Files

Basic conversion (format inferred from output filename):
```bash
audioconvert convert input.wav output.mp3
```

Specify output format explicitly:
```bash
audioconvert convert input.flac output.audio -f mp3
```

Convert with custom bitrate (for compressed formats):
```bash
audioconvert convert input.wav output.mp3 -b 320k
```

Convert with custom sample rate:
```bash
audioconvert convert input.mp3 output.wav -r 48000
```

Convert to mono:
```bash
audioconvert convert input.wav output.mp3 -c 1
```

Combine options:
```bash
audioconvert convert input.flac output.mp3 -b 320k -r 44100 -c 2
```

#### Get Audio File Information

```bash
audioconvert info audio.mp3
```

Output example:
```
Reading audio.mp3...

Audio File Information:
  Duration: 180.45 seconds
  Channels: 2 (stereo)
  Sample Rate: 44100 Hz
  Sample Width: 2 bytes
  Frame Count: 7953945
  File Size: 5,234,567 bytes (4.99 MB)
```

#### List Supported Formats

```bash
audioconvert formats
```

### Python API

```python
from audioconvert import AudioConverter

# Create converter instance
converter = AudioConverter()

# Basic conversion
converter.convert('input.wav', 'output.mp3')

# Conversion with options
converter.convert(
    input_file='input.flac',
    output_file='output.mp3',
    bitrate='320k',
    sample_rate=48000,
    channels=2
)

# Get audio file information
info = converter.get_audio_info('audio.mp3')
print(f"Duration: {info['duration_seconds']} seconds")
print(f"Sample Rate: {info['sample_rate']} Hz")
```

## Supported Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| MP3    | .mp3      | MPEG Audio Layer 3 (lossy compression) |
| WAV    | .wav      | Waveform Audio File Format (uncompressed) |
| OGG    | .ogg      | Ogg Vorbis (lossy compression) |
| FLAC   | .flac     | Free Lossless Audio Codec |
| M4A    | .m4a      | MPEG-4 Audio with AAC codec (lossy compression) |

## Development

### Setup Development Environment

```bash
# Install dependencies including dev requirements
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=audioconvert --cov-report=html

# Run specific test file
pytest tests/test_converter.py

# Run specific test
pytest tests/test_converter.py::TestAudioConverter::test_initialization
```

### Project Structure

```
myaiplug-audioconvert/
├── audioconvert/           # Main package
│   ├── __init__.py        # Package initialization
│   ├── converter.py       # Core conversion logic
│   └── cli.py             # Command-line interface
├── tests/                 # Test suite
│   ├── __init__.py
│   ├── test_converter.py  # Converter tests
│   └── test_cli.py        # CLI tests
├── requirements.txt       # Production dependencies
├── requirements-dev.txt   # Development dependencies
├── setup.py              # Package setup
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## Error Handling

The converter includes comprehensive error handling:

- **FileNotFoundError**: When input file doesn't exist
- **ValueError**: For invalid formats, parameters, or file access issues
- **RuntimeError**: For conversion failures or file reading errors

All errors include clear, actionable error messages.

## Performance Considerations

- Conversion speed depends on file size, format, and system resources
- Uncompressed formats (WAV, FLAC) are faster to read/write
- Compressed formats (MP3, OGG, AAC) require more CPU for encoding/decoding
- Higher bitrates and sample rates increase file size and processing time

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## Support

For questions, issues, or feature requests, please open an issue on GitHub.
