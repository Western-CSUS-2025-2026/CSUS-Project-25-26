from twelvelabs import TwelveLabs
from twelvelabs.indexes import IndexesCreateRequestModelsItem
from twelvelabs.tasks import TasksRetrieveResponse

from api.exceptions import FailToConnectTwelveLabs, IndexCreatingFail, FailToCreateTask
from api.settings import get_settings, Settings


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
            The created index id and other metadata.
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


    def create_task(self, video_file_path: str = None, video_url: str = None, index_id: str = None):
        """"
        Create a task to upload and index a video.
        
        This method creates a task that will upload the video to TwelveLabs
        and index it for analysis. Can accept either a local file path or
        a video URL.
        
        Args:
            video_file_path: Path to local video file to upload. Defaults to None.
            video_url: URL of the video to index. Defaults to None.
            index_id: Get it from create_index() method.
        
        Returns:
            Task object containing task_id and other metadata.
        """
        if index_id is None:
            if self.index_id is None:
                self.create_index()
            index_id = self.index_id
        
        try:
            # SDK handles both URL and file uploads
            if video_file_path:
                with open(video_file_path, "rb") as video_file:
                    task = self.client.tasks.create(
                        index_id=index_id,
                        video_file=video_file
                    )
            elif video_url:
                task = self.client.tasks.create(
                    index_id=index_id,
                    video_url=video_url
                )
            else:
                raise FailToCreateTask("Either video_file_path or video_url must be provided")

            return task
        except Exception as e:
            raise FailToCreateTask(str(e))


    def wait_for_task(self, task, sleep_interval: int = 5):
        """
        Wait for a task to complete and return the result.
        
        Polls the task status until it completes (ready) or fails.
        Uses the task's wait_for_done method with a callback for status updates.
        
        Args:
            task: Task object to wait for (from create_task).
            sleep_interval: Seconds to wait between status checks. Defaults to 5.
        
        Returns:
            Completed task object with video_id and status.
        """
        try:
            def on_task_update(task: TasksRetrieveResponse):
                print(f"Status={task.status}")
            
            # Use task.wait_for_done() directly on the task object
            task.wait_for_done(sleep_interval=sleep_interval)
            
            if task.status != "ready":
                raise RuntimeError(f"Indexing failed with status {task.status}")
            
            return task
        except Exception as e:
            raise FailToCreateTask(str(e))


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
        """
        try:
            prompt = f"""You're an Interviewer, Analyze the video clip of the interview answer for the question - {question}.

If the face is not present in the video then do provide the lower points in all categories, Do provide less than 5 for all the other categories if the face is not visible in the video.

Do provide the response in the json format with the number assigned as the value. 

After analyzing from 1-10. The keys of the json as confidence, clarity, speech_rate, eye_contact, body_language, voice_tone, relevant_to_question, imp_points.

The imp_points will contain the exact sentence in a summarized points by the speaker, also do remove the filler words and provide it in a list format which is important from video."""
            
            result = self.client.generate.text(
                video_id=video_id,
                prompt=prompt
            )
            
            return result
        except Exception as e:
            raise FailToCreateTask(str(e))