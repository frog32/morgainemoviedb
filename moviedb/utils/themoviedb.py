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

