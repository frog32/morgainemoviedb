from django.db import models
from django.db.models.fields import FieldDoesNotExist

class FileManager(models.Manager):
    def media_search(self, hash, size):
        """
        Searches the media by hash and size
        """
        if hash == 'SizeError':
            return self.filter(pk=0)
        return self.filter(hash=hash).filter(size=size).filter(movie__isnull=False)