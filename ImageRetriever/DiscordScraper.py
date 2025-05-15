import json

import requests
from dotenv import load_dotenv
import os
class DiscordScraper:
    def __init__(self):
        load_dotenv()
        channel_id = os.getenv("channel_id")
        auth_token = os.getenv("auth_token")
        channel_url = os.getenv("channel_url")
        self.headers = {
			"Authorization": auth_token,
			"Referer": channel_url
		}
        self.channel_id = channel_id
        self.extracted_data = []
        self.base_url = f"https://discord.com/api/v9/channels/{self.channel_id}/messages"

    def get_first_n_messages(self,n):
        url = self.base_url + "?limit=" + str(n)
        try:
            response = requests.get(url, headers=self.headers, timeout=86400)
        except:
            print(f"[ERROR]: Failed to scrape URL: {url}")
            return None
        return response
    def extract_messages(self, obj):
        data = json.loads(obj.text)
        for message in data:
            message = {
                "content": message["content"],
                "author": {
                    "id": message["author"]["id"],
                    "user_name": message["author"]["username"]
                },
                "channel": message["channel_id"],
                "timestamp": message["timestamp"],
                "attachments_url": message["attachments"][0]["url"] if len(message["attachments"]) > 0 else [],
                "pinned": message["pinned"]
            }
            self.extracted_data.append(message)

        return self.extracted_data
    def get_images(self, messages):
        images = []
        for message in messages:
            if(len(message["attachments_url"]) > 0):
                images.append(message["attachments_url"])
        return images
    def get_images_from_last_n_messages(self, n):
        messages = self.get_first_n_messages(n)
        messages = self.extract_messages(messages)
        return self.get_images(messages)

extractor = DiscordScraper()
print(extractor.get_images_from_last_n_messages(3))


