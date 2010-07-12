# morgainemoviedb -- a tool to organize your local movies
# Copyright 2010 Marc Egli
#
# This file is part of morgainemoviedb.
# 
# morgainemoviedb is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# morgainemoviedb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with morgainemoviedb.  If not, see <http://www.gnu.org/licenses/>.

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


