class SearchResult(dict):
    id: int
    media_type: str

    def __init__(self, id, media_type):
        dict.__init__(self, id=id, media_type=media_type)


