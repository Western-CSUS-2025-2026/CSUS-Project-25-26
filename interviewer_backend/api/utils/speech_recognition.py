import logging
import os
import tempfile
from pathlib import Path

import speech_recognition as sr
from pydub import AudioSegment


logger = logging.getLogger(__name__)


class SpeechRecognitionWrapper:
    """Wrapper for SpeechRecognition library to convert interview videos/audio to text"""

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def video_to_text(
        self,
        video_path: str,
        language: str = "en-US",
        audio_format: str = "wav",
    ) -> str:
        """
        Convert video file to text using speech recognition.

        Args:
            video_path: Path to the video file
            language: Language code for recognition (default: en-US)
            audio_format: Audio format for extraction (default: wav)

        Returns:
            Transcribed text from the video

        Raises:
            FileNotFoundError: If video file doesn't exist
            Exception: If recognition fails
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # Extract audio from video
        audio_path = self._extract_audio_from_video(video_path, audio_format)

        try:
            # Convert audio to text
            text = self.audio_to_text(audio_path, language)
            return text
        finally:
            # Clean up temporary audio file
            if os.path.exists(audio_path):
                os.remove(audio_path)

    def audio_to_text(self, audio_path: str, language: str = "en-US") -> str:
        """
        Convert audio file to text using speech recognition.

        Args:
            audio_path: Path to the audio file
            language: Language code for recognition (default: en-US)

        Returns:
            Transcribed text from the audio

        Raises:
            FileNotFoundError: If audio file doesn't exist
            Exception: If recognition fails
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        with sr.AudioFile(audio_path) as source:
            audio_data = self.recognizer.record(source)

        try:
            text = self.recognizer.recognize_google(audio_data, language=language)
            logger.info(f"Successfully transcribed audio from {audio_path}")
            return text
        except sr.UnknownValueError:
            logger.warning("Speech recognition could not understand audio")
            return ""
        except sr.RequestError as e:
            logger.error(f"Speech recognition service error: {e}")
            raise Exception(f"Speech recognition service error: {e}")

    def _extract_audio_from_video(self, video_path: str, audio_format: str = "wav") -> str:
        """
        Extract audio from video file and save as temporary file.

        Args:
            video_path: Path to the video file
            audio_format: Output audio format (default: wav)

        Returns:
            Path to the extracted audio file
        """
        video = AudioSegment.from_file(video_path)

        # Create temporary file for audio
        temp_dir = tempfile.gettempdir()
        video_name = Path(video_path).stem
        audio_path = os.path.join(temp_dir, f"{video_name}_audio.{audio_format}")

        # Export audio
        video.export(audio_path, format=audio_format)
        logger.info(f"Extracted audio from {video_path} to {audio_path}")

        return audio_path


def transcribe_video(video_path: str, language: str = "en-US") -> str:
    """
    Convenience function to transcribe video to text.

    Args:
        video_path: Path to the video file
        language: Language code for recognition (default: en-US)

    Returns:
        Transcribed text from the video
    """
    wrapper = SpeechRecognitionWrapper()
    return wrapper.video_to_text(video_path, language)


def transcribe_audio(audio_path: str, language: str = "en-US") -> str:
    """
    Convenience function to transcribe audio to text.

    Args:
        audio_path: Path to the audio file
        language: Language code for recognition (default: en-US)

    Returns:
        Transcribed text from the audio
    """
    wrapper = SpeechRecognitionWrapper()
    return wrapper.audio_to_text(audio_path, language)
