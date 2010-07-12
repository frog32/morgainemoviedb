import urllib2, json, os

lang='en'
apikey='a470dddae9a3fb7db6791108133cea05'

def lookupOSHash(hash):
    '''Sends the OS Hash to the movie DB'''
    req = urllib2.Request('http://api.themoviedb.org/2.1/Hash.getInfo/en/json/%s/%s' % (apikey,hash))
    req.add_header('User-Agent', 'Mozilla/5.0 (%s; en-GB; rv:1.9.0.3) urllib2 python' % (os.name))
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    obj=json.loads(link)
    return obj
    
def imdbLookup(imdbID):
    '''looks up a move with the imdbID'''
    req = urllib2.Request('http://api.themoviedb.org/2.1/Movie.imdbLookup/en/json/%s/tt%07d' % (apikey,imdbID))
    req.add_header('User-Agent', 'Mozilla/5.0 (%s; en-GB; rv:1.9.0.3) urllib2 python' % (os.name))
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    obj=json.loads(link)
    return obj
    
def getImages(imdbID):
    '''gets all the images with the imdbID'''
    req = urllib2.Request('http://api.themoviedb.org/2.1/Movie.getImages/en/json/%s/tt%07d' % (apikey,imdbID))
    req.add_header('User-Agent', 'Mozilla/5.0 (%s; en-GB; rv:1.9.0.3) urllib2 python' % (os.name))
    response = urllib2.urlopen(req)
    link=response.read()
    response.close()
    obj=json.loads(link)
    return obj

