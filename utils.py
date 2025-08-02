def get_supported_formats():
    """
    Returns a dictionary of supported file formats, grouped by category.
    Uses lowercase extensions for consistency.
    """
    return {
        "Documents": {
            ".docx": [".pdf"],
            ".pdf": [".docx"],
            ".txt": [".pdf", ".docx"],
            ".py": [".txt", ".pdf"],
            ".json": [".txt", ".pdf"],
        },
        "Images": {
            ".png": [".jpg", ".jpeg", ".bmp", ".gif", ".tiff"],
            ".jpg": [".png", ".bmp", ".gif", ".tiff"],
            ".jpeg": [".png", ".bmp", ".gif", ".tiff"],
            ".bmp": [".png", ".jpg", ".jpeg", ".gif", ".tiff"],
            ".gif": [".png", ".jpg", ".jpeg", ".bmp", ".tiff"],
            ".tiff": [".png", ".jpg", ".jpeg", ".bmp", ".gif"],
        },
        "Audio": {
            ".mp3": [".wav", ".ogg", ".flac"],
            ".wav": [".mp3", ".ogg", ".flac"],
            ".ogg": [".mp3", ".wav", ".flac"],
            ".flac": [".mp3", ".wav", ".ogg"],
        },
        "Video": {
            ".mp4": [".avi", ".mov", ".mkv"],
            ".avi": [".mp4", ".mov", ".mkv"],
            ".mov": [".mp4", ".avi", ".mkv"],
            ".mkv": [".mp4", ".avi", ".mov"],
        }
    }
