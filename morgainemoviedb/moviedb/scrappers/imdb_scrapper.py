# this scrapper is not valid
# this are just fragments of the old imdb scraper

def search_movie():
results = imdb.IMDb(accessSystem='http', adultSearch=0).search_movie(query)

def setIMDB(self, imdb_id):
    # this function is obsolete since we take only results from the movie db
    problems = []
    '''set imdb_id and get all the information out of imdb'''
    m=imdb.IMDb(accessSystem='http', adultSearch=0).get_movie(imdb_id)
    self.imdb_id=int(imdb_id)
    self.year=m['year']
    # insert titles
    self.titles.all().delete()
    self.titles.add(Title(text = m['title'], language = u'Original', default=True))
    for aka in m['akas']:
        result=re.match('^(.*?)::(.+) \(([^)]+)\)', aka, re.IGNORECASE)
        if result:
            newTitle = Title(text = result.group(1), country = result.group(2), comment = result.group(3)) #, language = result.group(5))
            newTitle.save()
            self.titles.add(newTitle)

    # insert genres
    self.genres=[]
    for gen in m['genres']:
            self.genres.add(searchOrAddGenre(gen))
    # insert countries
    self.countries=[]
    for country in m['countries']:
        query = Country.objects.filter(name = country)
        if query.count():
            self.countries.add(query[0])
        else:
            newCountry = Country(name = country)
            newCountry.save()
            self.countries.add(newCountry)
    # insert cast
    for actor in self.actors.all():
        actor.delete()
    if 'cast' in m.keys():
        for person in m['cast']:
            newPerson = searchOrAddPerson(person)
            if hasattr(person.currentRole,'__iter__'):
                for role in person.currentRole:
                    # there are multiple roles for the same person
                    newRole = searchOrAddRole(role)
                    Actor.objects.create(role = newRole, person = newPerson, movie = self)
            else:
                # this person only plays one role
                if 'name' in person.currentRole.keys():
                    newRole = searchOrAddRole(person.currentRole)
                    Actor.objects.create(role = newRole, person = newPerson, movie = self)
                else:
                    newRole = Role.objects.create(name = person['name'], imdb_id = 0)
                    Actor.objects.create(role = newRole, person = newPerson, movie = self)

    # insert writers
    self.writers = []
    if hasattr(m['writer'],'__iter__'):
        for person in m['writer']:
            self.writers.add(searchOrAddPerson(person))
    else:
        person = m['writer']
        self.writers.add(searchOrAddPerson(person))
        
    # insert directors
    self.directors=[]
    if hasattr(m['director'],'__iter__'):
        for person in m['director']:
            self.directors.add(searchOrAddPerson(person))
    else:
        person = m['director']
        self.directors.add(searchOrAddPerson(person))

    # get image data from themoviedb
    self.posters=[]
    obj=themoviedb.getImages(self.imdb_id)
    if obj[0] != 'Nothing found.':
        for poster in obj[0]['posters']:
            if poster['image']['size']=='original':
                newPoster = Poster(remote_path = poster['image']['url'], source_type = u'themoviedb')
                try:
                    newPoster.download()
                    newPoster.generate_thumb()
                    self.posters.add(newPoster)
                except:
                    problems.append('Error downloading image')
    return problems
