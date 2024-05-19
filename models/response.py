class Response:
    def __init__(self, url: str, message: str, lang: str):
        self.url = url
        self.message = message
        self.lang = lang

    def to_dict(self):
        return {
            'url': self.url,
            'message': self.message,
            'lang': self.lang
        }