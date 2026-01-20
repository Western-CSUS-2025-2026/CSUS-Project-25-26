import json
import logging
import re
import tempfile
from typing import BinaryIO

from retrying import retry
from twelvelabs import TwelveLabs
from twelvelabs.models.task import Task

from api.exceptions import AnalysisFailed, VideoProcessingFailed
from api.settings import Settings, get_settings


logger = logging.getLogger(__name__)
settings: Settings = get_settings()


class TwelveLabsClient:
    """Client for interacting with Twelve Labs API for video analysis."""

    _client: TwelveLabs | None = None

    @classmethod
    def get_client(cls) -> TwelveLabs:
        """Get or create Twelve Labs client instance."""
        if cls._client is None:
            if not settings.TWELVE_LABS_API_KEY:
                raise VideoProcessingFailed("Twelve Labs API key not configured")
            cls._client = TwelveLabs(api_key=settings.TWELVE_LABS_API_KEY)
        return cls._client

    @classmethod
    @retry(
        stop_max_attempt_number=settings.MAX_RETRIES,
        stop_max_delay=settings.STOP_MAX_DELAY,
        wait_random_min=settings.WAIT_MIN,
        wait_random_max=settings.WAIT_MAX,
        retry_on_exception=lambda exc: not isinstance(exc, VideoProcessingFailed),
    )
    def upload_video(cls, file: BinaryIO, filename: str) -> Task:
        """
        Upload a video file to Twelve Labs for indexing.

        Args:
            file: File-like object containing video data
            filename: Original filename

        Returns:
            Task object with task_id for tracking indexing progress
        """
        client = cls.get_client()

        if not settings.TWELVE_LABS_INDEX_ID:
            raise VideoProcessingFailed("Twelve Labs index ID not configured")

        # Write to temp file since twelvelabs SDK expects file path
        with tempfile.NamedTemporaryFile(suffix=f"_{filename}", delete=False) as tmp:
            tmp.write(file.read())
            tmp_path = tmp.name

        try:
            task = client.task.create(
                index_id=settings.TWELVE_LABS_INDEX_ID,
                file=tmp_path,
            )
            logger.info(f"Video upload task created: {task.id}")
            return task
        except Exception as e:
            logger.error(f"Failed to upload video: {e}")
            raise VideoProcessingFailed(f"Failed to upload video: {str(e)}")

    @classmethod
    def check_task_status(cls, task_id: str) -> Task:
        """
        Check the status of a video indexing task.

        Args:
            task_id: The Twelve Labs task ID

        Returns:
            Task object with current status
        """
        client = cls.get_client()
        try:
            task = client.task.retrieve(task_id)
            logger.info(f"Task {task_id} status: {task.status}")
            return task
        except Exception as e:
            logger.error(f"Failed to check task status: {e}")
            raise VideoProcessingFailed(f"Failed to check task status: {str(e)}")

    @classmethod
    def wait_for_task(cls, task_id: str) -> str:
        """
        Wait for a video indexing task to complete.

        Args:
            task_id: The Twelve Labs task ID

        Returns:
            video_id once indexing is complete
        """
        client = cls.get_client()
        try:
            task = client.task.retrieve(task_id)

            # Poll until complete
            task.wait_for_done(sleep_interval=5)

            if task.status == "failed":
                raise VideoProcessingFailed(f"Video indexing failed: {task_id}")

            logger.info(f"Task {task_id} completed, video_id: {task.video_id}")
            return task.video_id
        except VideoProcessingFailed:
            raise
        except Exception as e:
            logger.error(f"Failed waiting for task: {e}")
            raise VideoProcessingFailed(f"Failed waiting for task: {str(e)}")

    @classmethod
    @retry(
        stop_max_attempt_number=3,
        stop_max_delay=30000,
        wait_random_min=1000,
        wait_random_max=3000,
        retry_on_exception=lambda exc: not isinstance(exc, AnalysisFailed),
    )
    def analyze_interview(cls, video_id: str, question: str) -> dict:
        """
        Analyze an interview video for communication skills.

        Args:
            video_id: The Twelve Labs video ID
            question: The interview question that was asked

        Returns:
            Dictionary containing analysis results with scores and feedback
        """
        client = cls.get_client()

        prompt = f"""Analyze this interview response video where the candidate is answering the following question:
"{question}"

Evaluate the candidate's communication skills and provide a JSON response with the following structure:
{{
    "overall_score": <float 1-10>,
    "clarity_score": <float 1-10 rating speech clarity>,
    "pace_score": <float 1-10 rating speaking pace - not too fast or slow>,
    "filler_word_count": <integer count of filler words like um, uh, like, you know>,
    "confidence_score": <float 1-10 rating confidence level based on voice and body language>,
    "eye_contact_score": <float 1-10 rating eye contact with camera>,
    "summary": "<2-3 sentence summary of overall performance>",
    "suggestions": "<3-5 specific actionable suggestions for improvement>"
}}

Return ONLY the JSON object, no other text."""

        try:
            response = client.generate.text(
                video_id=video_id,
                prompt=prompt,
            )

            # Parse the response
            result_text = response.data
            logger.info(f"Analysis response for video {video_id}: {result_text[:200]}...")

            # Extract JSON from response
            try:
                # Try to find JSON in the response
                json_match = re.search(r'\{[\s\S]*\}', result_text)
                if json_match:
                    result = json.loads(json_match.group())
                else:
                    result = json.loads(result_text)
            except json.JSONDecodeError:
                logger.warning(f"Could not parse JSON from response: {result_text}")
                # Return a default structure if parsing fails
                result = {
                    "overall_score": None,
                    "clarity_score": None,
                    "pace_score": None,
                    "filler_word_count": None,
                    "confidence_score": None,
                    "eye_contact_score": None,
                    "summary": result_text[:500] if result_text else "Analysis completed but could not be parsed.",
                    "suggestions": "Please try again or contact support if the issue persists.",
                }

            return result

        except Exception as e:
            logger.error(f"Failed to analyze interview: {e}")
            raise AnalysisFailed(f"Failed to analyze interview: {str(e)}")
