from twelvelabs import TwelveLabs
from twelvelabs.indexes import IndexesCreateRequestModelsItem
from twelvelabs.tasks import TasksRetrieveResponse

from api.exceptions import FailToConnectTwelveLabs, IndexCreatingFail, FailToCreateTask
from api.settings import get_settings, Settings

from fastapi import UploadFile


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
        
        try:
            self.client = TwelveLabs(api_key=self.settings.TWELVE_LABS_API_KEYS)
            self.index_id = None
        except Exception as e:
            raise FailToConnectTwelveLabs(str(e))


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

    
    def upload_asset(self, file: UploadFile):
        """
        Upload a video file to TwelveLabs assets.
        
        Uploads a video file directly to TwelveLabs using the direct upload method.
        This is the first step before indexing a video for analysis.
        
        Args:
            file: FastAPI UploadFile object containing the video file to upload.
        
        Returns:
            Asset object containing asset_id and other metadata.
        
        Raises:
            Exception: If asset upload fails (e.g., file too large, invalid format)
        """
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
        """
        Generate custom interview analysis for a video.
        
        Uses TwelveLabs generate.text() to analyze an interview video
        and provide scores for various interview metrics. The analysis
        includes confidence, clarity, speech rate, eye contact, body language,
        voice tone, relevance to question, and important points.
        
        Args:
            video_id: The unique identifier of the video to analyze.
            question: The interview question that was asked in the video.
        
        Returns:
            Analysis result object containing:
            - confidence: Score 1-10 for confidence level
            - clarity: Score 1-10 for answer clarity
            - speech_rate: Score 1-10 for speech rate appropriateness
            - eye_contact: Score 1-10 for eye contact quality
            - body_language: Score 1-10 for body language
            - voice_tone: Score 1-10 for voice tone
            - relevant_to_question: Score 1-10 for answer relevance
            - imp_points: List of important points from the answer
        
        Raises:
            FailToCreateTask: If analysis generation fails
        """
        try:
            prompt = f"""You are an Interviewer and a professional communication analyst. Your task is to analyze the video clip of the interview answer provided for the question: "{question}".

Your response must be a single JSON object.

### Scoring Criteria:
Analyze and score the candidate on the following categories from 1 (Needs significant improvement) to 10 (Excellent).

### Conditional Logic (CRITICAL):
If a visible face is **not** present in the video, you **must** assign a score of less than 5 (e.g., 1, 2, 3, or 4) for ALL numerical categories (confidence, clarity, speech_rate, eye_contact, body_language, voice_tone, relevant_to_question, imp_points).

### JSON Output Keys:
The final JSON object must contain the following keys:
1.  **confidence** (Number 1-10)
2.  **clarity** (Number 1-10)
3.  **speech_rate** (Number 1-10)
4.  **eye_contact** (Number 1-10)
5.  **body_language** (Number 1-10)
6.  **voice_tone** (Number 1-10)
7.  **relevant_to_question** (Number 1-10)
8.  **imp_points** (List of Strings): A list containing the exact, summarized sentences spoken by the speaker. **Remove all filler words** ("um," "like," "you know," etc.) from these sentences.
9.  **overall_summary** (String): A one-paragraph, high-level assessment of the answer, including its key strengths and weaknesses.
10. **actionable_feedback** (String): Specific, constructive advice pointing out areas for improvement (e.g., "Increase vocal projection," "Maintain steady eye contact," or "Structure the answer using the STAR method").
"""
            result = self.client.analyze(
                video_id=video_id,
                prompt=prompt
            )
            
            return result
        except Exception as e:
            raise FailToCreateTask(str(e))
