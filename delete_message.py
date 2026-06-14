import requests
import json
import re
import ast
import time
import random

class MessageDeleter:
    def __init__(self, fetch_content, messages_data):
        """
        fetch_content: The raw string of the fetch command (from RAM).
        messages_data: The list/dict of messages returned by FetchRunner.
        """
        self.fetch_content = fetch_content
        self.raw_data = messages_data
        self.headers = {}
        self.messages_to_delete = []

    def run(self):
        """Main execution method."""
        print("--- Starting Message Deletion Process ---")

        if not self._parse_fetch_headers():
            return

        self._load_messages_from_memory()
        self._process_deletions()

    def _parse_fetch_headers(self):
        """Parses headers and auth token from the provided fetch string."""
        if not self.fetch_content:
            print("Error: No fetch content provided.")
            return False

        content = self.fetch_content
        start_index = content.find('{')
        end_index = content.rfind('}')

        if start_index == -1 or end_index == -1:
            print("Error: Could not find config object in fetch command.")
            return False

        config_str = content[start_index: end_index + 1]
        config_str = re.sub(r'\bnull\b', 'None', config_str)
        config_str = re.sub(r'\btrue\b', 'True', config_str)
        config_str = re.sub(r'\bfalse\b', 'False', config_str)
        config_str = re.sub(r'(?m)^\s*([a-zA-Z_]\w*)\s*:', r'"\1":', config_str)

        try:
            options = ast.literal_eval(config_str)
            self.headers = options.get('headers', {})
            return True
        except Exception as e:
            print(f"Error parsing fetch headers: {e}")
            return False

    def _load_messages_from_memory(self):
        """Flattens and filters out non-deletable system messages."""
        if not self.raw_data:
            print("No data provided to deleter.")
            return

        if isinstance(self.raw_data, dict):
            raw_messages = self.raw_data.get('messages', [])
        elif isinstance(self.raw_data, list):
            raw_messages = self.raw_data
        else:
            raw_messages = []

        temp_list = []
        for item in raw_messages:
            if isinstance(item, list):
                temp_list.extend(item)
            else:
                temp_list.append(item)

        self.messages_to_delete = []
        for msg in temp_list:
                        msg_type = msg.get('type', 0)
            
            if msg_type not in [0, 19]:
                continue
            
            self.messages_to_delete.append(msg)

        print(f"Filtered out system messages. Found {len(self.messages_to_delete)} deletable messages.")

    def _process_deletions(self):
        """Loops through messages and sends DELETE requests with dynamic pacing."""
        total = len(self.messages_to_delete)

        for index, msg in enumerate(self.messages_to_delete):
            try:
                message_id = msg.get('id')
                channel_id = msg.get('channel_id')
                content = msg.get('content', '[No Content]')

                if not message_id or not channel_id:
                    print(f"Skipping item {index}: Missing ID or Channel ID")
                    continue

                url = f"https://discord.com/api/v9/channels/{channel_id}/messages/{message_id}"
                print(f"[{index + 1}/{total}] Deleting: {content[:40]}...")

                response = requests.delete(url, headers=self.headers)

                if response.status_code in [200, 204]:
                    print("   -> Success")
                elif response.status_code == 429:
                    retry_after = response.json().get('retry_after', 5)
                    print(f"   -> Rate Limited! Sleeping for exact requested penalty: {retry_after}s")
                    time.sleep(retry_after)
                    response = requests.delete(url, headers=self.headers)
                else:
                    print(f"   -> Failed: {response.status_code} - {response.text}")

                sleep_time = random.uniform(2.5, 4.5)
                print(f"   -> Pacing for {sleep_time:.2f} seconds...")
                time.sleep(sleep_time)

            except Exception as e:
                print(f"Error processing message {index}: {e}")
