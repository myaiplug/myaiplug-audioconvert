"""
Command-line interface for audio converter
"""

import sys
import click
from pathlib import Path
from .converter import AudioConverter


@click.group()
@click.version_option(version='0.1.0')
def cli():
    """
    MyAIPlug Audio Converter - High quality audio format converter
    
    Convert audio files between different formats with ease.
    """
    pass


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option(
    '-f', '--format',
    type=click.Choice(['mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a'], case_sensitive=False),
    help='Output format (inferred from output filename if not specified)'
)
@click.option(
    '-b', '--bitrate',
    default='192k',
    help='Bitrate for compressed formats (e.g., 192k, 320k). Default: 192k'
)
@click.option(
    '-r', '--sample-rate',
    type=int,
    help='Target sample rate in Hz (e.g., 44100, 48000)'
)
@click.option(
    '-c', '--channels',
    type=click.IntRange(1, 2),
    help='Number of channels (1=mono, 2=stereo)'
)
def convert(input_file, output_file, format, bitrate, sample_rate, channels):
    """
    Convert an audio file to a different format
    
    Example:
        audioconvert convert input.wav output.mp3
        audioconvert convert input.mp3 output.wav -b 320k
        audioconvert convert input.flac output.mp3 -r 44100 -c 2
    """
    try:
        converter = AudioConverter()
        
        click.echo(f"Converting {input_file} to {output_file}...")
        
        result = converter.convert(
            input_file=input_file,
            output_file=output_file,
            output_format=format,
            bitrate=bitrate,
            sample_rate=sample_rate,
            channels=channels,
        )
        
        click.echo(click.style(f"✓ Successfully converted to {result}", fg='green'))
        
    except FileNotFoundError as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)
    except ValueError as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)
    except RuntimeError as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"✗ Unexpected error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
@click.argument('audio_file', type=click.Path(exists=True))
def info(audio_file):
    """
    Display information about an audio file
    
    Example:
        audioconvert info audio.mp3
    """
    try:
        converter = AudioConverter()
        
        click.echo(f"Reading {audio_file}...")
        
        info_data = converter.get_audio_info(audio_file)
        
        click.echo("\n" + click.style("Audio File Information:", fg='cyan', bold=True))
        click.echo(f"  Duration: {info_data['duration_seconds']:.2f} seconds")
        click.echo(f"  Channels: {info_data['channels']} ({'mono' if info_data['channels'] == 1 else 'stereo'})")
        click.echo(f"  Sample Rate: {info_data['sample_rate']} Hz")
        click.echo(f"  Sample Width: {info_data['sample_width']} bytes")
        click.echo(f"  Frame Count: {info_data['frame_count']}")
        click.echo(f"  File Size: {info_data['file_size']:,} bytes ({info_data['file_size'] / 1024 / 1024:.2f} MB)")
        
    except FileNotFoundError as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)
    except RuntimeError as e:
        click.echo(click.style(f"✗ Error: {e}", fg='red'), err=True)
        sys.exit(1)
    except Exception as e:
        click.echo(click.style(f"✗ Unexpected error: {e}", fg='red'), err=True)
        sys.exit(1)


@cli.command()
def formats():
    """
    List all supported audio formats
    """
    converter = AudioConverter()
    
    click.echo(click.style("\nSupported Audio Formats:", fg='cyan', bold=True))
    
    for fmt, info in converter.SUPPORTED_FORMATS.items():
        click.echo(f"  • {fmt.upper()} ({info['extension']})")
    
    click.echo()


def main():
    """Entry point for the CLI"""
    cli()


if __name__ == '__main__':
    main()
