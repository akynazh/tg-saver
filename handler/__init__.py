from handler import base, custom
import common

HandlersMap = {
    common.FileTypes.MEDIA_GROUP: base.MediaGroupHandler,
    common.FileTypes.VIDEO: base.VideoHandler,
    common.FileTypes.PHOTO: base.PhotoHandler,
    common.FileTypes.DOCUMENT: base.DocumentHandler,
    common.FileTypes.AUDIO: base.AudioHandler
}


def all_subclasses(cls):
    return set(cls.__subclasses__()).union(
        [s for c in cls.__subclasses__() for s in all_subclasses(c)])


HandlersMap.update({handler.C_TYPE: handler for handler in
                    list(filter(lambda c: c.C_TYPE != 0, all_subclasses(base.FileHandler)))})
