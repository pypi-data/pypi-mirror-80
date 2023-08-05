class CloudControlException(Exception):
    def __init__(self, message, response):
        self.message = message
        self.response = response

    def get_http_code(self):
        return self.response.status_code

    def get_response_code(self):
        if self.response.text:
            return self.response.json()['responseCode']
        return None

    def get_response_message(self):
        if self.response.text:
            return self.response.json()['message']
        return None
