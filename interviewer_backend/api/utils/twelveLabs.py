from twelvelabs import TwelveLabs
from twelvelabs.indexes import IndexesCreateRequestModelsItem
from twelvelabs.tasks import TasksRetrieveResponse

from api.exceptions import FailToConnectTwelveLabs, IndexCreatingFail, FailToCreateTask

from api.settings import get_settings, Settings


class videoAnalysis:
    settings: Settings = get_settings()

    def __init__(self):
        try:
            self.client = TwelveLabs(api_key=self.settings.TWELVE_LABS_API_KEYS)
            self.index_id = None
        except Exception as e:
            raise FailToConnectTwelveLabs(str(e))


    def create_index(self, index_name: str = None):
        if index_name is None:
            index_name = self.settings.TWELVE_LABS_INDEX_NAME
        try:
            index = self.client.indexes.create(
                index_name=index_name,
                models=[
                    IndexesCreateRequestModelsItem(
                        model_name="Pegasus1.2",
                        model_options=["visual", "audio"]
                    )
                ]
            )
            self.index_id = index.id
            return index
        except Exception as e:
            raise IndexCreatingFail(str(e))

    
    def create_task(self, video_url: str, index_id: str = None):
        if index_id is None:
            if self.index_id is None:
                # Create index if none exists
                self.create_index()
            index_id = self.index_id
        
        try:
            task = self.client.tasks.create(
                index_id=index_id,
                video_url=video_url
            )
            return task
        except Exception as e:
            raise FailToCreateTask(str(e))

    
    def wait_for_task(self, task_id: str):
        """
            Wait for task to complete and return the result
        """
        try:
            def on_task_update(task: TasksRetrieveResponse):
                print(f"Status={task.status}")
            
            # Get the task id from create_task(); task.id
            task = self.client.tasks.wait_for_done(task_id=task_id, callback=on_task_update)
            
            if task.status != "ready":
                raise RuntimeError(f"Indexing failed with status {task.status}")
            
            return task
        except Exception as e:
            raise FailToCreateTask(str(e))


    def search(self, query_text: str, index_id: str = None, search_options: list[str] = None):
        """
            Search for video clips matching query
        """
        if index_id is None:
            if self.index_id is None:
                raise ValueError("No index_id provided and no index created")
            index_id = self.index_id
        
        if search_options is None:
            search_options = ["visual", "audio"]
        
        try:
            search_pager = self.client.search.query(
                index_id=index_id,
                query_text=query_text,
                search_options=search_options
            )
            return list(search_pager)
        except Exception as e:
            raise FailToCreateTask(str(e))