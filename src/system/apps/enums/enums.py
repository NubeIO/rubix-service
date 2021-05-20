import enum


class Types(enum.Enum):
    INSTALLER = 'Installer'
    FRONTEND_APP = 'FrontendApp'
    PYTHON_APP = 'PythonApp'
    JAVA_APP = 'JavaApp'


class DownloadState(enum.Enum):
    CLEARED = 'Cleared'
    DOWNLOADING = 'Downloading'
    DOWNLOADED = 'Downloaded'
