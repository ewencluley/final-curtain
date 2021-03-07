class SearchResult(dict):
    def __init__(self, id, media_type, name, img):
        dict.__init__(self, id=id, media_type=media_type, name=name, img=img)


class CastResult(dict):
    def __init__(self, id, character, name):
        dict.__init__(self, id=id, character=character, name=name)