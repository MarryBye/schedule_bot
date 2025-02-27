import os
import pandas as pd

class MessageHistory(pd.DataFrame):
    def __init__(self, history_file: str):
        super().__init__({
            "author_id": [],
            "author_name": [],
            "author_username": [],
            "creation_date": [],
            "creation_time": [],
            "chat_id": [],
            "chat_type": [],
            "text": [],
            "is_answer": [],
            "answerred_text": [],
            "answerred_author_id": [],
            "answerred_author_name": []
        })
        if not os.path.exists(history_file):
            self.to_csv(history_file, index=False)
        else:
            file_dataset = pd.read_csv(history_file)
            self[file_dataset.columns] = file_dataset
            
    def get_last_page(self, n: int=25) -> int:
        return len(self) // n
    
    def show_page(self, page: int, n: int=25) -> pd.DataFrame:
        last_page = self.get_last_page(n)
        if page < 0 or page > last_page: 
            page = last_page
        start = page * n
        end = start + n
        return self[start:end:1]
