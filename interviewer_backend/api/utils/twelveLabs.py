from twelvelabs import TwelveLabs
from twelvelabs.indexes import IndexesCreateRequestModelsItem
from twelvelabs.types import ResponseFormat

from api.exceptions import FailToConnectTwelveLabs, IndexCreatingFail, FailToCreateTask
from api.settings import get_settings, Settings
from api.models.db import TwelveLabsIndex

from fastapi import UploadFile

import datetime
import uuid


class VideoAnalysis:
    """
    Video analysis client for TwelveLabs API.
    
    This class handles video upload, indexing, and interview analysis
    using the TwelveLabs API for interview video grading.
    
    Attributes:
        settings: Application settings containing API keys and configuration
        client: TwelveLabs API client instance
        index_id: ID of the current index being used
    """

    settings: Settings = get_settings()

    def __init__(self):
        """
        Initialize the VideoAnalysis client.
        
        Sets up the TwelveLabs API client using the API key from settings.
        Initializes the index_id to None (will be set when an index is created).
        
        Raises:
            FailToConnectTwelveLabs: If API key is not set in settings or
                                    connection to TwelveLabs API fails
        """
        if not self.settings.TWELVE_LABS_API_KEYS:
            raise FailToConnectTwelveLabs("TWELVE_LABS_API_KEYS is not set")
        
        self.client = TwelveLabs(api_key=self.settings.TWELVE_LABS_API_KEYS)
        self.index_id = None


    def create_index(self, index_name: str = None):
        """
        Create an index for video analysis.
        
        An index is a container that organizes and stores video content
        for analysis.
        
        Args:
            index_name: Name for the index. If None, uses TWELVE_LABS_INDEX_NAME
                        from settings. Defaults to None.
        
        Returns:
            The created index object with id and other metadata.
        
        Raises:
            IndexCreatingFail: If index creation fails due to API error
        """
        if index_name is None:
            index_name = self.settings.TWELVE_LABS_INDEX_NAME
        
        try:
            index = self.client.indexes.create(
                index_name=index_name,
                models=[
                    IndexesCreateRequestModelsItem(
                        model_name="pegasus1.2",
                        model_options=["visual", "audio"]
                    )
                ]
            )
            self.index_id = index.id
            return index
        except Exception as e:
            raise IndexCreatingFail(str(e))

    
    def list_indexes(self):
        """
        List all available indexes.
        
        Retrieves all indexes that have been created in the TwelveLabs account.
        
        Returns:
            List of strings, each containing index ID and name in format:
            "Index: {id} - {index_name}"
        """
        indexes = []
        for index in self.client.indexes.list():
            indexes.append(f"Index: {index.id} - {index.index_name}")
        return indexes

    
    def get_or_create_index(self, user_id: int, session):
        existing_index = (
            TwelveLabsIndex.query(session=session).filter(TwelveLabsIndex.user_id == user_id).one_or_none()
        )

        now = datetime.datetime.now(tz=datetime.timezone.utc)
        if existing_index and now < existing_index.expires_at:
            return existing_index.index_id

        index = self.create_index(index_name=f"user_{user_id}_index_{uuid.uuid4().hex}")
        index_id = index.id

        # expires_at = now + lifetime - buffer (no TL retrieve each time; avoid edge cases)
        lifetime_days = self.settings.INDEX_LIFETIME_DAYS - self.settings.INDEX_EXPIRY_BUFFER_DAYS
        expires_at = now + datetime.timedelta(days=lifetime_days)

        if existing_index:
            session.delete(existing_index)
            session.flush()

        TwelveLabsIndex.create(
            session=session,
            user_id=user_id,
            index_id=index_id,
            expires_at=expires_at,
        )

        return index_id

    
    def upload_asset(self, file: UploadFile):
        """
        Upload a video file to TwelveLabs assets.

        Args:
            file: FastAPI UploadFile object containing the video file to upload.

        Returns:
            Asset object containing asset_id and other metadata.
        """
        file.file.seek(0)
        asset = self.client.assets.create(
            method="direct",
            file=file.file
        )
        return asset

        
    def index_asset(self, index_id: str, asset_id: str):
        """
        Index an uploaded asset into an index.
        
        Associates an uploaded video asset with an index, enabling it for
        analysis. The indexing process runs asynchronously.
        
        Args:
            index_id: The unique identifier of the index to add the asset to.
            asset_id: The unique identifier of the uploaded asset.
        
        Returns:
            IndexedAsset object containing indexed_asset_id and status.
        
        Raises:
            Exception: If indexing fails (e.g., invalid index_id or asset_id)
        """
        indexed_asset = self.client.indexes.indexed_assets.create(
            index_id=index_id,
            asset_id=asset_id,
            enable_video_stream=True
        )
        return indexed_asset


    def get_video_transcript(self, index_id: str, video_id: str):
        """
        Retrieve transcript for an indexed video.
        
        Args:
            index_id: The unique identifier of the index
            video_id: The unique identifier of the indexed video (indexed_asset_id)
        
        Returns:
            String containing the full transcript, or None if not available
        """
        try:
            response = self.client.indexes.videos.retrieve(
                index_id=index_id,
                video_id=video_id,
                transcription=True
            )
            
            if hasattr(response, 'transcription') and response.transcription:
                transcript_parts = [item.value for item in response.transcription if hasattr(item, 'value')]
                return " ".join(transcript_parts) if transcript_parts else None
            
            return None
        except Exception:
            return None


    def list_indexed_assets(self, index_id: str):
        """
        List all indexed assets in an index.
        
        Retrieves all video assets that have been indexed in the specified index.
        
        Args:
            index_id: The unique identifier of the index to list assets from.
        
        Returns:
            Response object containing list of indexed assets with their metadata.
        """
        response = self.client.indexes.indexed_assets.list(
            index_id=index_id,
        )
        return response


    def generate_interview_analysis(self, video_id: str, question: str):
        try:
            prompt = f"""You are a senior technical interviewer and communication coach.

The video contains an answer to an interview question.
Analyze the candidate's response.

QUESTION:
{question}

CRITICAL RULES (DO NOT VIOLATE):
- Return ONE valid JSON object only — no markdown fences, no explanations, no extra text
- The response must start with {{ and end with }}
- Scores must be integers from 1 to 10
- If a visible face is NOT present, all scores MUST be below 5
- Feedback must be grounded in what the candidate actually said
- Wrap the response in a "question_responses" array

Return EXACTLY this JSON structure:
{{"question_responses": [{{"question": "<the interview question>", "body_language_score": <1-10>, "speech_score": <1-10>, "brevity_score": <1-10>, "material_score": <1-10>, "feedback": {{"points": ["<problem 1>", "<problem 2>", "<problem 3>"], "ways_to_improve": ["<improvement 1>", "<improvement 2>", "<improvement 3>"]}}, "improved_answer": {{"version": "<one polished answer paragraph>"}}}}]}}

SCORING GUIDE:
- body_language_score: posture, gestures, eye contact, facial expressions
- speech_score: clarity, pace, filler words, articulation
- brevity_score: conciseness, staying on topic, not rambling
- material_score: how well the candidate used relevant content/examples to answer the question

feedback.points: EXACTLY 3 specific problems identified
feedback.ways_to_improve: EXACTLY 3 actionable improvements addressing the problems
improved_answer.version: ONE polished, natural, professional answer paragraph"""

            result = self.client.analyze(
                video_id=video_id,
                prompt=prompt,
                temperature=0.2,
                max_tokens=2500,
                response_format=ResponseFormat(
                    type="json_schema",
                    json_schema={
                        "type": "object",
                        "properties": {
                            "question_responses": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "question": {"type": "string"},
                                        "body_language_score": {
                                            "type": "integer",
                                            "minimum": 1,
                                            "maximum": 10
                                        },
                                        "speech_score": {
                                            "type": "integer",
                                            "minimum": 1,
                                            "maximum": 10
                                        },
                                        "brevity_score": {
                                            "type": "integer",
                                            "minimum": 1,
                                            "maximum": 10
                                        },
                                        "material_score": {
                                            "type": "integer",
                                            "minimum": 1,
                                            "maximum": 10
                                        },
                                        "feedback": {
                                            "type": "object",
                                            "properties": {
                                                "points": {
                                                    "type": "array",
                                                    "items": {"type": "string"}
                                                },
                                                "ways_to_improve": {
                                                    "type": "array",
                                                    "items": {"type": "string"}
                                                }
                                            },
                                            "required": ["points", "ways_to_improve"]
                                        },
                                        "improved_answer": {
                                            "type": "object",
                                            "properties": {
                                                "version": {"type": "string"}
                                            },
                                            "required": ["version"]
                                        }
                                    },
                                    "required": [
                                        "question",
                                        "body_language_score",
                                        "speech_score",
                                        "brevity_score",
                                        "material_score",
                                        "feedback",
                                        "improved_answer"
                                    ]
                                }
                            }
                        },
                        "required": ["question_responses"]
                    }
                )
            )

            return result

        except Exception as e:
            raise FailToCreateTask(str(e))
