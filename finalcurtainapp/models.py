class SearchResult(dict):
    def __init__(self, id, media_type, name, img):
        dict.__init__(self, id=id, media_type=media_type, name=name, img=img)


class CastResult(dict):
    def __init__(self, id, character, name, birthday=None, deathday=None, has_detail=False):
        dict.__init__(self, id=id, character=character, name=name, birthday=birthday, deathday=deathday, has_detail=has_detail)

    def add_detail(self, birthday, deathday):
        self['has_detail'] = True
        self['birthday'] = birthday
        self['deathday'] = deathday
        return self


