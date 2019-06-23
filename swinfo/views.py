from django.shortcuts import render
from django.http import HttpResponse
import requests

#
# def index(request):
#     return HttpResponse("Hello World! Welcome to the poll index :D")
url = 'https://swapi-graphql-integracion-t3.herokuapp.com/'
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        print("returning FORWARDED_FOR")
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        print("returning REAL_IP")
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        print("returning REMOTE_ADDR")
        ip = request.META.get('REMOTE_ADDR')
    return ip

def index(request):


    query = {"query":
                """
                {
                  allFilms {
                    edges {
                      node {
                        episodeID
                        id
                        title
                        director
                        producers
                        releaseDate
                      }
                    }
                  }
                }
                """
                }

    response = requests.post(url = url, json = query)

    movies = response.json()

    return render(request, 'swinfo/home.html', {
        'movies': movies["data"]["allFilms"]["edges"],
        'ip':get_client_ip(request),
    })

def detail(request, movie_id):
    query = {"query":
                """
                {
                  allFilms {
                    edges {
                      node {
                        id
                        episodeID
                        openingCrawl
                        title
                        director
                        producers
                        releaseDate
                        episodeID
                        title
                        director
                        producers
                        releaseDate
                        planetConnection {
                            planets {
                                name
                                id
                            }
                        }
                        starshipConnection {
                            starships {
                                name
                                id
                            }
                        }
                        characterConnection {
                            characters {
                                name
                                id
                            }
                        }



                      }
                    }
                  }
                }
                """
                }
    response = requests.post(url = url, json = query)
    movies = response.json()["data"]["allFilms"]["edges"]
    characters = {}
    starships = {}
    planets = {}

    for movie in movies:
        if movie["node"]['id'] == movie_id:
            correct_movie = movie
    for character in correct_movie['node']['characterConnection']['characters']:
        characters.update({character["name"]: character["id"]})

    for starship in correct_movie['node']['starshipConnection']['starships']:
        starships.update({starship['name']:starship['id']})

    for planet in correct_movie['node']['planetConnection']['planets']:
        planets.update({planet['name']:planet['id']})



    return render(request, 'swinfo/detail.html', {
        'movie': correct_movie["node"],
        'characters':characters,
        'starships':starships,
        'planets':planets,
    })

def character_detail(request, character_id):

    query = {"query":
    """
    {
      allPeople {
        edges
        {
          node {
           name
            id
            height
            mass
            eyeColor
            hairColor
            skinColor
            birthYear
            gender
            filmConnection {
              films {
                title
                id
              }
            }
            starshipConnection{
              starships
              {
                name
                id
              }
            }
            homeworld{
              name
              id

            }
          }

        }
      }
    }
    """
 }
    response = requests.post(url = url, json = query)
    characters = response.json()["data"]["allPeople"]["edges"]
    for character in characters:
        if character["node"]["id"] == character_id:
            true_character = character["node"]

    films = {}
    starships = {}

    for film in true_character['filmConnection']['films']:
        films.update({film["title"]:film["id"]})

    for starship in true_character['starshipConnection']['starships']:
        starships.update({starship['name']:starship['id']})

    return render(request, 'swinfo/character_detail.html',{
        'character':true_character,
        'films':films,
        'starships':starships,
    })

def ship_detail(request, starship_id):
    query = {"query":
    """
    {
  allStarships {

    edges
    {
      node
      {
        name
        id
        model
        manufacturers
        costInCredits
        length
        maxAtmospheringSpeed
        crew
        passengers
        cargoCapacity
        consumables
        hyperdriveRating
        MGLT
        starshipClass
        filmConnection {
            films {
                title
                id
          }

        }
        pilotConnection {
        	pilots {
                name
                id
          }
        }
      }
    }
  }
	}
"""
}
    response = requests.post(url = url, json = query)
    ships = response.json()["data"]["allStarships"]["edges"]
    for ship in ships:
        if ship["node"]["id"] == starship_id:
            true_ship = ship["node"]
    films = {}
    pilots = {}

    for film in true_ship['filmConnection']['films']:
        films.update({film["title"]:film["id"]})

    for pilot in true_ship['pilotConnection']['pilots']:
        pilots.update({pilot['name']:pilot['id']})


    return render(request, 'swinfo/ship_detail.html',{
        'ship':true_ship,
        'films':films,
        'pilots':pilots,
    })

def planet_detail(request, planet_id):
    query = {"query":
    """
    {
	allPlanets {
    edges {
      node {
        name
        id
        rotationPeriod
        orbitalPeriod
        diameter
        climates
        gravity
        terrains
        surfaceWater
        population
        filmConnection {
          films {
            title
            id
          }
        }
        residentConnection {
          residents {
            name
            id
          }
        }
      }
    }
  }
}
"""
}
    response = requests.post(url = url, json = query)
    planets = response.json()["data"]["allPlanets"]["edges"]

    for planet in planets:
        if planet["node"]["id"] == planet_id:
            true_planet = planet["node"]

    films = {}
    residents = {}

    for film in true_planet['filmConnection']['films']:
        films.update({film["title"] : film["id"]})

    for resident in true_planet['residentConnection']['residents']:
        residents.update({resident['name']:resident['id']})

    return render(request, 'swinfo/planet_detail.html',{
        'planet':true_planet,
        'films':films,
        'residents':residents,
    })


def search(request):
    if 'q' in request.GET:
        q = request.GET['q']
        movies_result = requests.get('https://swapi.co/api/films/'+'?search='+q)
        movies = movies_result.json()
        movies_sources = []

        for pelicula in movies["results"]:
            movies_sources.append(pelicula)

        while movies["next"]:
            movies = requests.get(movies["next"]).json()
            for pelicula in movies["results"]:
                movies_sources.append(pelicula)

        character_result = requests.get('https://swapi.co/api/people/'+'?search='+q)
        characters = character_result.json()
        characters_sources = []
        for personaje in characters["results"]:
            head, partition, tail = personaje["url"].partition("people/")
            character_id = tail[:-1]
            personaje.update({"id":character_id})
            characters_sources.append(personaje)
        while characters["next"]:
            characters = requests.get(characters["next"]).json()
            for personaje in characters["results"]:
                head, partition, tail = personaje["url"].partition("people/")
                character_id = tail[:-1]
                personaje.update({"id":character_id})
                characters_sources.append(personaje)


        planet_result = requests.get('https://swapi.co/api/planets/'+'?search='+q)
        planets = planet_result.json()
        planets_sources = []
        for planeta in planets["results"]:
            head, partition, tail = planeta["url"].partition("planets/")
            planet_id = tail[:-1]
            planeta.update({"id":planet_id})
            planets_sources.append(planeta)
        while planets["next"]:
            planets = requests.get(planets["next"]).json()
            for planeta in planets["results"]:
                head, partition, tail = planeta["url"].partition("planets/")
                planet_id = tail[:-1]
                planeta.update({"id":planet_id})
                planets_sources.append(planeta)


        ship_result = requests.get('https://swapi.co/api/starships/'+'?search='+q)
        ships = ship_result.json()
        ships_sources = []
        for nave in ships["results"]:
            head, partition, tail = nave["url"].partition("starships/")
            ship_id = tail[:-1]
            nave.update({"id":ship_id})
            ships_sources.append(nave)
        while ships["next"]:
            ships = requests.get(ships["next"]).json()
            for nave in ships["results"]:
                head, partition, tail = nave["url"].partition("starships/")
                ship_id = tail[:-1]
                nave.update({"id":ship_id})
                ships_sources.append(nave)


        return render(request, 'swinfo/search.html', {
            'movies' : movies_sources,
            'characters' : characters_sources,
            'planets' : planets_sources,
            'ships' : ships_sources,
        })


    else:
        return HttpResponse("Por favor ingresa un término para buscar.")
