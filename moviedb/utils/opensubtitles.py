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

import struct, os

def hashFile(name): 
  try: 
     
    longlongformat = 'q'  # long long 
    bytesize = struct.calcsize(longlongformat) 
        
    f = open(name, "rb") 
        
    filesize = os.path.getsize(name) 
    hash = filesize 
        
    if filesize < 65536 * 2: 
      return "SizeError" 
     
    for x in range(65536/bytesize): 
      buffer = f.read(bytesize) 
      (l_value,)= struct.unpack(longlongformat, buffer)  
      hash += l_value 
      hash = hash & 0xFFFFFFFFFFFFFFFF #to remain as 64bit number  
             

    f.seek(max(0,filesize-65536),0) 
    for x in range(65536/bytesize): 
      buffer = f.read(bytesize) 
      (l_value,)= struct.unpack(longlongformat, buffer)  
      hash += l_value 
      hash = hash & 0xFFFFFFFFFFFFFFFF 
 
    f.close() 
    returnedhash =  "%016x" % hash 
    return returnedhash 

  except(IOError): 
    return "IOError"
