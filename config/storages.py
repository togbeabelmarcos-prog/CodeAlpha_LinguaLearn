from cloudinary_storage.storage import MediaCloudinaryStorage

AUDIO_EXTENSIONS = {"mp3", "wav", "ogg", "m4a", "aac", "flac", "opus", "wma"}
VIDEO_EXTENSIONS = {"mp4", "webm", "mov", "avi", "mkv", "m4v", "ogv", "3gp"}
RAW_EXTENSIONS = {"pdf", "zip", "txt", "doc", "docx", "xls", "xlsx"}


class MediaStorage(MediaCloudinaryStorage):
    def _get_resource_type(self, name):
        ext = name.rsplit(".", 1)[-1].lower() if "." in name else ""
        if ext in AUDIO_EXTENSIONS | VIDEO_EXTENSIONS:
            return "video"
        if ext in RAW_EXTENSIONS:
            return "raw"
        return "image"
