"""
Unit tests for audio converter
"""

import os
import pytest
from pathlib import Path
from audioconvert.converter import AudioConverter


class TestAudioConverter:
    """Test cases for AudioConverter class"""
    
    def test_initialization(self):
        """Test that AudioConverter initializes correctly"""
        converter = AudioConverter()
        assert converter is not None
        assert hasattr(converter, 'logger')
    
    def test_supported_formats(self):
        """Test that all expected formats are supported"""
        converter = AudioConverter()
        expected_formats = ['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a']
        
        for fmt in expected_formats:
            assert fmt in converter.SUPPORTED_FORMATS
    
    def test_validate_output_format_valid(self):
        """Test format validation with valid formats"""
        converter = AudioConverter()
        
        # Test lowercase
        assert converter.validate_output_format('mp3') == 'mp3'
        assert converter.validate_output_format('wav') == 'wav'
        
        # Test uppercase
        assert converter.validate_output_format('MP3') == 'mp3'
        assert converter.validate_output_format('WAV') == 'wav'
        
        # Test with leading dot
        assert converter.validate_output_format('.mp3') == 'mp3'
        assert converter.validate_output_format('.WAV') == 'wav'
    
    def test_validate_output_format_invalid(self):
        """Test format validation with invalid formats"""
        converter = AudioConverter()
        
        with pytest.raises(ValueError, match="Unsupported output format"):
            converter.validate_output_format('xyz')
        
        with pytest.raises(ValueError, match="Unsupported output format"):
            converter.validate_output_format('doc')
    
    def test_validate_input_file_not_exists(self):
        """Test validation of non-existent input file"""
        converter = AudioConverter()
        
        with pytest.raises(FileNotFoundError):
            converter.validate_input_file('/nonexistent/file.mp3')
    
    def test_validate_input_file_not_a_file(self, tmp_path):
        """Test validation when path is a directory"""
        converter = AudioConverter()
        
        # Create a directory
        test_dir = tmp_path / "testdir"
        test_dir.mkdir()
        
        with pytest.raises(ValueError, match="Path is not a file"):
            converter.validate_input_file(test_dir)
    
    def test_convert_missing_input_file(self, tmp_path):
        """Test conversion with missing input file"""
        converter = AudioConverter()
        output_file = tmp_path / "output.mp3"
        
        with pytest.raises(FileNotFoundError):
            converter.convert('/nonexistent/input.wav', output_file)
    
    def test_convert_invalid_format(self, tmp_path):
        """Test conversion with invalid output format"""
        converter = AudioConverter()
        
        # Create a dummy input file
        input_file = tmp_path / "input.txt"
        input_file.write_text("dummy")
        output_file = tmp_path / "output.xyz"
        
        with pytest.raises(ValueError, match="Unsupported output format"):
            converter.convert(input_file, output_file)
    
    def test_convert_invalid_channels(self, tmp_path):
        """Test conversion with invalid channel count"""
        converter = AudioConverter()
        
        # Create a dummy input file
        input_file = tmp_path / "input.txt"
        input_file.write_text("dummy")
        output_file = tmp_path / "output.mp3"
        
        with pytest.raises(ValueError, match="Channels must be"):
            converter.convert(input_file, output_file, channels=5)
    
    def test_get_audio_info_missing_file(self):
        """Test getting info from non-existent file"""
        converter = AudioConverter()
        
        with pytest.raises(FileNotFoundError):
            converter.get_audio_info('/nonexistent/file.mp3')


class TestAudioConverterIntegration:
    """Integration tests for audio conversion (requires actual audio files)"""
    
    @pytest.fixture
    def sample_audio_file(self, tmp_path):
        """
        Create a simple test audio file using pydub
        This creates a 1-second tone for testing
        """
        from pydub.generators import Sine
        
        # Generate a 1-second sine wave at 440 Hz (A note)
        tone = Sine(440).to_audio_segment(duration=1000)
        
        # Save as WAV
        audio_file = tmp_path / "test_input.wav"
        tone.export(str(audio_file), format='wav')
        
        return audio_file
    
    def test_convert_wav_to_mp3(self, sample_audio_file, tmp_path):
        """Test converting WAV to MP3"""
        converter = AudioConverter()
        output_file = tmp_path / "output.mp3"
        
        result = converter.convert(sample_audio_file, output_file)
        
        assert result.exists()
        assert result.suffix == '.mp3'
        assert result.stat().st_size > 0
    
    def test_convert_with_bitrate(self, sample_audio_file, tmp_path):
        """Test conversion with specific bitrate"""
        converter = AudioConverter()
        output_file = tmp_path / "output_320k.mp3"
        
        result = converter.convert(
            sample_audio_file,
            output_file,
            bitrate='320k'
        )
        
        assert result.exists()
        assert result.stat().st_size > 0
    
    def test_convert_with_sample_rate(self, sample_audio_file, tmp_path):
        """Test conversion with specific sample rate"""
        converter = AudioConverter()
        output_file = tmp_path / "output_48k.mp3"
        
        result = converter.convert(
            sample_audio_file,
            output_file,
            sample_rate=48000
        )
        
        assert result.exists()
        
        # Verify sample rate was changed
        info = converter.get_audio_info(result)
        assert info['sample_rate'] == 48000
    
    def test_convert_to_mono(self, sample_audio_file, tmp_path):
        """Test conversion to mono"""
        converter = AudioConverter()
        output_file = tmp_path / "output_mono.mp3"
        
        result = converter.convert(
            sample_audio_file,
            output_file,
            channels=1
        )
        
        assert result.exists()
        
        # Verify channel count
        info = converter.get_audio_info(result)
        assert info['channels'] == 1
    
    def test_convert_multiple_formats(self, sample_audio_file, tmp_path):
        """Test converting to multiple formats"""
        converter = AudioConverter()
        
        formats_to_test = ['mp3', 'ogg', 'flac']
        
        for fmt in formats_to_test:
            output_file = tmp_path / f"output.{fmt}"
            result = converter.convert(sample_audio_file, output_file)
            
            assert result.exists()
            assert result.suffix == f'.{fmt}'
            assert result.stat().st_size > 0
    
    def test_get_audio_info(self, sample_audio_file):
        """Test getting audio file information"""
        converter = AudioConverter()
        
        info = converter.get_audio_info(sample_audio_file)
        
        assert 'duration_seconds' in info
        assert 'channels' in info
        assert 'sample_rate' in info
        assert 'file_size' in info
        
        # Check that duration is approximately 1 second (we created 1s tone)
        assert 0.9 <= info['duration_seconds'] <= 1.1
    
    def test_output_directory_creation(self, sample_audio_file, tmp_path):
        """Test that output directories are created automatically"""
        converter = AudioConverter()
        
        # Create path with non-existent directory
        output_file = tmp_path / "subdir" / "nested" / "output.mp3"
        
        result = converter.convert(sample_audio_file, output_file)
        
        assert result.exists()
        assert result.parent.exists()
