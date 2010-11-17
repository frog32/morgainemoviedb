# coding=utf-8
import sys

class Singleton(object):
    def __new__(type, *args):
        # Falls es noch keine Instanz dieser Klasse gibt, wird eine erstellt und in _the_instance abgelegt.
        # Diese wird dann jedes mal zurückgegeben.
        if not '_the_instance' in type.__dict__:
            type._the_instance = object.__new__(type)
        return type._the_instance

    def __init__(self):
        if not '_ready' in dir(self):
            # Der Konstruktor wird bei jeder Instanziierung aufgerufen.
            # Einmalige Dinge wie zum Beispiel die Initialisierung von Klassenvariablen müssen also in diesen Block.
            self._ready = True



class ScrapperClient(Singleton):
    scrapper = None
    
    def set_scrapper(self,scrapper_name):
        modname = 'moviedb.scrappers.' + scrapper_name
        __import__(modname)
        self.scrapper = sys.modules[modname]
    
    def search_movies(self, query):
        """
        returns a collection of search results
        """
        if(not self.scrapper):
            raise Exception("You have to select a scrapper first")
        return self.scrapper.search_movies(query)
    
    def set_movie(self, movie, movie_id):
        """
        Set movie to the specified movie_id. movie_id has to correspond to the
        movie id received from the same scrapper
        """
        if(not self.scrapper):
            raise Exception("You have to select a scrapper first")
        return self.scrapper.set_movie(movie, movie_id)
    
    def lookup_hash(self, movie):
        """
        searches for the movie hash of every movie file contained in movie
        sets the movie if only one result matches
        """
        if(not self.scrapper):
            raise Exception("You have to select a scrapper first")
        return self.scrapper.lookup_hash(movie)

        

        