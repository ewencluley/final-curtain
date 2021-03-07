class SearchResult(dict):
    def __init__(self, id, media_type, name, img):
        dict.__init__(self, id=id, media_type=media_type, name=name, img=img)


