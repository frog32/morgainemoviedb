from django.conf import settings

MOVIE_BASE_DIR = getattr(settings, 'MDB_MOVIE_BASE_DIR', '/filme')

FOLDER_TYPE_CHOICES =  getattr(settings, 'MDB_FOLDER_TYPE_CHOICES',(
    (1,'Movies'),
    (2,'Series'),
))

FOLDER_SCAN_MODE = getattr(settings, 'MDB_FOLDER_SCAN_MODE',(
    (1,'Flat'),
    (2,'Recursive'),
    (3,'Don\'t add Movies'),
))

SCAN_EXCLUDE_FILES = getattr(settings, 'MDB_EXCLUDE_FILES',(
    '^\.',
))

MOVIE_FILE_SUFFIXES = getattr(settings, 'MDB_MOVIE_FILE_SUFFIXES',{\
    '.avi':'movie',
    '.mkv':'movie',
    '.mov':'movie',
    '.mp3':'sound',
})


