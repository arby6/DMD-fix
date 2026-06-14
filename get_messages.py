import requests
import json
import re
import ast

class FetchRunner:
    def __init__(self, fetch_content):
        self.fetch_content = fetch_content
        self.url = None
        self.options = {}

    def run(self, offset=None):
        if not self.fetch_content:
            print("Error: No fetch content provided.")
            return None

        if not self._parse_fetch_command(self.fetch_content):
            return None

        if offset is not None and "search?" in self.url:
            self.url = re.sub(r'offset=\d+', f'offset={offset}', self.url)
            if "offset=" not in self.url:
                self.url += f"&offset={offset}"

        return self._execute_request()

    def _parse_fetch_command(self, content):
        url_match = re.search(r"fetch\(['\"](.*?)['\"]", content)
        if not url_match:
            print("Error: Could not find a URL in the fetch command.")
            return False
        self.url = url_match.group(1)

        start_index = content.find('{')
        end_index = content.rfind('}')

        if start_index == -1 or end_index == -1:
            self.options = {'method': 'GET', 'headers': {}}
            return True

        config_str = content[start_index: end_index + 1]
        config_str = re.sub(r'\bnull\b', 'None', config_str)
        config_str = re.sub(r'\btrue\b', 'True', config_str)
        config_str = re.sub(r'\bfalse\b', 'False', config_str)
        config_str = re.sub(r'(?m)^\s*([a-zA-Z_]\w*)\s*:', r'"\1":', config_str)

        try:
            self.options = ast.literal_eval(config_str)
            return True
        except Exception as e:
            print(f"Error parsing config: {e}")
            return False

    def _execute_request(self):
        method = self.options.get('method', 'GET')
        headers = self.options.get('headers', {})
        body_raw = self.options.get('body')

        json_payload = None
        if isinstance(body_raw, str):
            try:
                json_payload = json.loads(body_raw)
                body_raw = None
            except:
                pass

        print(f"Running API Request -> {self.url}")

        try:
            response = requests.request(
                method=method,
                url=self.url,
                headers=headers,
                data=body_raw,
                json=json_payload
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Request failed with status: {response.status_code}")
                return None
        except Exception as e:
            print(f"Execution failed: {e}")
            return None
