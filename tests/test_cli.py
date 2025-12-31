"""
Tests for CLI interface
"""

import pytest
from click.testing import CliRunner
from pathlib import Path
from audioconvert.cli import cli


class TestCLI:
    """Test cases for CLI commands"""
    
    @pytest.fixture
    def runner(self):
        """Create a CLI test runner"""
        return CliRunner()
    
    @pytest.fixture
    def sample_audio_file(self, tmp_path):
        """Create a simple test audio file"""
        from pydub.generators import Sine
        
        tone = Sine(440).to_audio_segment(duration=1000)
        audio_file = tmp_path / "test.wav"
        tone.export(str(audio_file), format='wav')
        
        return audio_file
    
    def test_cli_help(self, runner):
        """Test that --help works"""
        result = runner.invoke(cli, ['--help'])
        
        assert result.exit_code == 0
        assert 'MyAIPlug Audio Converter' in result.output
    
    def test_cli_version(self, runner):
        """Test that --version works"""
        result = runner.invoke(cli, ['--version'])
        
        assert result.exit_code == 0
        assert '0.1.0' in result.output
    
    def test_convert_help(self, runner):
        """Test convert command help"""
        result = runner.invoke(cli, ['convert', '--help'])
        
        assert result.exit_code == 0
        assert 'Convert an audio file' in result.output
    
    def test_info_help(self, runner):
        """Test info command help"""
        result = runner.invoke(cli, ['info', '--help'])
        
        assert result.exit_code == 0
        assert 'Display information' in result.output
    
    def test_formats_command(self, runner):
        """Test formats command"""
        result = runner.invoke(cli, ['formats'])
        
        assert result.exit_code == 0
        assert 'MP3' in result.output
        assert 'WAV' in result.output
        assert 'FLAC' in result.output
    
    def test_convert_missing_input(self, runner, tmp_path):
        """Test convert with missing input file"""
        result = runner.invoke(cli, [
            'convert',
            str(tmp_path / 'nonexistent.wav'),
            str(tmp_path / 'output.mp3')
        ])
        
        # Click returns exit code 2 for file not found in path validation
        assert result.exit_code in [1, 2]
        assert 'Error' in result.output or 'does not exist' in result.output
    
    def test_convert_success(self, runner, sample_audio_file, tmp_path):
        """Test successful conversion"""
        output_file = tmp_path / 'output.mp3'
        
        result = runner.invoke(cli, [
            'convert',
            str(sample_audio_file),
            str(output_file)
        ])
        
        assert result.exit_code == 0
        assert 'Successfully converted' in result.output
        assert output_file.exists()
    
    def test_convert_with_format_option(self, runner, sample_audio_file, tmp_path):
        """Test conversion with explicit format option"""
        output_file = tmp_path / 'output.audio'
        
        result = runner.invoke(cli, [
            'convert',
            str(sample_audio_file),
            str(output_file),
            '-f', 'mp3'
        ])
        
        assert result.exit_code == 0
        assert output_file.exists()
    
    def test_convert_with_bitrate(self, runner, sample_audio_file, tmp_path):
        """Test conversion with bitrate option"""
        output_file = tmp_path / 'output.mp3'
        
        result = runner.invoke(cli, [
            'convert',
            str(sample_audio_file),
            str(output_file),
            '-b', '320k'
        ])
        
        assert result.exit_code == 0
        assert output_file.exists()
    
    def test_convert_with_sample_rate(self, runner, sample_audio_file, tmp_path):
        """Test conversion with sample rate option"""
        output_file = tmp_path / 'output.mp3'
        
        result = runner.invoke(cli, [
            'convert',
            str(sample_audio_file),
            str(output_file),
            '-r', '48000'
        ])
        
        assert result.exit_code == 0
        assert output_file.exists()
    
    def test_convert_with_channels(self, runner, sample_audio_file, tmp_path):
        """Test conversion with channels option"""
        output_file = tmp_path / 'output.mp3'
        
        result = runner.invoke(cli, [
            'convert',
            str(sample_audio_file),
            str(output_file),
            '-c', '1'
        ])
        
        assert result.exit_code == 0
        assert output_file.exists()
    
    def test_info_missing_file(self, runner, tmp_path):
        """Test info with missing file"""
        result = runner.invoke(cli, [
            'info',
            str(tmp_path / 'nonexistent.mp3')
        ])
        
        # Click returns exit code 2 for file not found in path validation
        assert result.exit_code in [1, 2]
        assert 'Error' in result.output or 'does not exist' in result.output
    
    def test_info_success(self, runner, sample_audio_file):
        """Test successful info command"""
        result = runner.invoke(cli, [
            'info',
            str(sample_audio_file)
        ])
        
        assert result.exit_code == 0
        assert 'Audio File Information' in result.output
        assert 'Duration' in result.output
        assert 'Channels' in result.output
        assert 'Sample Rate' in result.output
