"""
Core audio conversion functionality
"""

import os
import logging
from pathlib import Path
from typing import Optional, Union
from pydub import AudioSegment

# Get logger without configuring it (let applications configure logging)
logger = logging.getLogger(__name__)


class AudioConverter:
    """
    High-quality audio converter supporting multiple formats
    """
    
    SUPPORTED_FORMATS = {
        'mp3': {'extension': '.mp3', 'codec': 'libmp3lame', 'format': 'mp3'},
        'wav': {'extension': '.wav', 'codec': 'pcm_s16le', 'format': 'wav'},
        'ogg': {'extension': '.ogg', 'codec': 'libvorbis', 'format': 'ogg'},
        'flac': {'extension': '.flac', 'codec': 'flac', 'format': 'flac'},
        'm4a': {'extension': '.m4a', 'codec': 'aac', 'format': 'ipod'},  # ipod is the m4a/mp4 muxer
    }
    
    def __init__(self):
        """Initialize the audio converter"""
        self.logger = logger
    
    def validate_input_file(self, input_file: Union[str, Path]) -> Path:
        """
        Validate that the input file exists and is readable
        
        Args:
            input_file: Path to input audio file
            
        Returns:
            Path object of validated input file
            
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file is not accessible
        """
        input_path = Path(input_file)
        
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_file}")
        
        if not input_path.is_file():
            raise ValueError(f"Path is not a file: {input_file}")
        
        if not os.access(input_path, os.R_OK):
            raise ValueError(f"File is not readable: {input_file}")
        
        return input_path
    
    def validate_output_format(self, output_format: str) -> str:
        """
        Validate that the output format is supported
        
        Args:
            output_format: Target audio format (e.g., 'mp3', 'wav')
            
        Returns:
            Normalized format string
            
        Raises:
            ValueError: If format is not supported
        """
        format_lower = output_format.lower().strip('.')
        
        if format_lower not in self.SUPPORTED_FORMATS:
            supported = ', '.join(self.SUPPORTED_FORMATS.keys())
            raise ValueError(
                f"Unsupported output format: {output_format}. "
                f"Supported formats: {supported}"
            )
        
        return format_lower
    
    def convert(
        self,
        input_file: Union[str, Path],
        output_file: Union[str, Path],
        output_format: Optional[str] = None,
        bitrate: str = "192k",
        sample_rate: Optional[int] = None,
        channels: Optional[int] = None,
    ) -> Path:
        """
        Convert audio file to specified format
        
        Args:
            input_file: Path to input audio file
            output_file: Path to output audio file
            output_format: Target format (e.g., 'mp3', 'wav'). 
                         If None, inferred from output_file extension
            bitrate: Target bitrate (e.g., '192k', '320k'). 
                    Only applies to compressed formats like MP3, OGG, AAC
            sample_rate: Target sample rate in Hz (e.g., 44100, 48000).
                        If None, keeps original sample rate
            channels: Number of audio channels (1=mono, 2=stereo).
                     If None, keeps original channels
        
        Returns:
            Path to the converted output file
            
        Raises:
            FileNotFoundError: If input file doesn't exist
            ValueError: If format is unsupported or parameters are invalid
            RuntimeError: If conversion fails
        """
        try:
            # Validate input
            input_path = self.validate_input_file(input_file)
            output_path = Path(output_file)
            
            # Determine output format
            if output_format is None:
                output_format = output_path.suffix.lower().strip('.')
            
            output_format = self.validate_output_format(output_format)
            
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            self.logger.info(f"Converting {input_path} to {output_format} format...")
            
            # Load audio file
            audio = AudioSegment.from_file(str(input_path))
            
            # Apply transformations
            if sample_rate:
                self.logger.info(f"Setting sample rate to {sample_rate} Hz")
                audio = audio.set_frame_rate(sample_rate)
            
            if channels:
                if channels not in [1, 2]:
                    raise ValueError("Channels must be 1 (mono) or 2 (stereo)")
                self.logger.info(f"Setting channels to {channels}")
                audio = audio.set_channels(channels)
            
            # Export with format-specific parameters
            export_params = {}
            
            # Use custom format name if specified (e.g., 'ipod' for m4a)
            if output_format in self.SUPPORTED_FORMATS:
                format_name = self.SUPPORTED_FORMATS[output_format].get('format', output_format)
                export_params['format'] = format_name
            else:
                export_params['format'] = output_format
            
            # Add bitrate for compressed formats
            if output_format in ['mp3', 'ogg', 'm4a']:
                export_params['bitrate'] = bitrate
            
            # Add codec if available
            if output_format in self.SUPPORTED_FORMATS:
                codec = self.SUPPORTED_FORMATS[output_format].get('codec')
                if codec:
                    export_params['codec'] = codec
            
            # Perform conversion
            audio.export(str(output_path), **export_params)
            
            self.logger.info(f"Successfully converted to {output_path}")
            
            return output_path
            
        except FileNotFoundError:
            raise
        except ValueError:
            raise
        except Exception as e:
            error_msg = f"Error converting audio file: {str(e)}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg) from e
    
    def get_audio_info(self, audio_file: Union[str, Path]) -> dict:
        """
        Get information about an audio file
        
        Args:
            audio_file: Path to audio file
            
        Returns:
            Dictionary containing audio file information
            
        Raises:
            FileNotFoundError: If file doesn't exist
            RuntimeError: If file cannot be read
        """
        try:
            file_path = self.validate_input_file(audio_file)
            audio = AudioSegment.from_file(str(file_path))
            
            return {
                'duration_seconds': len(audio) / 1000.0,
                'duration_ms': len(audio),
                'channels': audio.channels,
                'sample_rate': audio.frame_rate,
                'sample_width': audio.sample_width,
                'frame_count': audio.frame_count(),
                'frame_width': audio.frame_width,
                'file_size': file_path.stat().st_size,
            }
        except FileNotFoundError:
            raise
        except Exception as e:
            error_msg = f"Error reading audio file info: {str(e)}"
            self.logger.error(error_msg)
            raise RuntimeError(error_msg) from e
