# Casting Agency

This API can be used to aid Casting Assistants, Casting Directors, and Executive Producers keep track of a database of **Actors** and **Movies**.

## Accessing the live URL

The Casting Agency can be accessed either directly through the API or using the frontend by navigating to the root URL.

- Root URL: [https://casting-agency-stefan.herokuapp.com/](https://casting-agency-stefan.herokuapp.com/)

The Authorization tokens are stored inside of the `setup.sh` shell file, however, should the tokens expire here are the logins for specific roles:

|Role|Username|Password|
|--|--|--|
|Casting Assistant|casting@assistant.com|password123$%^|
|Casting Director|casting@director.com|password123$%^|
|Executive Producer|executive@producer.com|password123$%^|

## Running the Server

Run the following shell command to load the necessary environment variables from within the project root directory. Then start the flask server

```shell
source ./setup.sh
python app.py
```

## Running Tests Locally

To test the api, complete the following commands.

```shell
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency_test.psql
source ./setup.sh
python test_app.py
```

## Roles

- Casting Assistant
  - Can view actors and movies
- Casting Director
  - All permissions a Casting Assistant has and…
  - Add or delete an actor from the database
  - Modify actors or movies
- Executive Producer
  - All permissions a Casting Director has and…
  - Add or delete a movie from the database

## API endpoints

Endpoints are permission-specific based upon roles (see above).

### Endpoints

- [`GET /actors`](#get-actors)
- [`GET /actors/<movie_id>`](#get-actorsactor_id)
- [`POST /actors`](#post-actors)
- [`PATCH /actors/<actor_id>`](#patch-actorsactor_id)
- [`DELETE /actors/<actor_id>`](#delete-actorsactor_id)
- [`GET /movies`](#get-movies)
- [`GET /movies/<movie_id>`](#get-moviesmovie_id)
- [`POST /movies`](#post-movies)
- [`PATCH /movies/<movie_id>`](#patch-moviesmovie_id)
- [`DELETE /movies/<movie_id>`](#delete-moviesmovie_id)

### Error Handling

Errors are returned as JSON objects in the following format:

```javascript
{
    "success": False,
    "error": 400,
    "message": "Bad Request"
}
```

The API will return the following error types:

- 400: Bad Request
- 401: Unauthorized
- 403: Not Authorized
- 404: Resource Not Found
- 405: Not Allowed
- 422: Unproccessable Entity

#### GET /actors

Get a list of all actors in the database.

- Requires `read:actors`
- Returns `json` object of all actors in the database as well as length of the database
- Sample: `curl http://127.0.0.1:8080/actors -H "Authorization: $CASTING_ASSISTANT"`

```javascript
{
  "actors": [
    {
      "age": 44,
      "birthdate": "1975-08-07 00:00:00",
      "gender": "F",
      "id": 37,
      "name": "Charliz Taryn",
      "seeking_work": true
    },
    {
      "age": 35,
      "birthdate": "1984-11-22 00:00:00",
      "gender": "F",
      "id": 36,
      "name": "Charlotte Johannsen",
      "seeking_work": true
    },
    {
      "age": 46,
      "birthdate": "1973-12-19 00:00:00",
      "gender": "M",
      "id": 34,
      "name": "Christian Boil",
      "seeking_work": true
    },
    {
      "age": 47,
      "birthdate": "1972-11-18 00:00:00",
      "gender": "M",
      "id": 35,
      "name": "Hue Jillman",
      "seeking_work": true
    },
    {
      "age": 62,
      "birthdate": "1958-01-01 00:00:00",
      "gender": "M",
      "id": 33,
      "name": "Tim Honks",
      "seeking_work": true
    },
    {
      "age": 41,
      "birthdate": "1978-06-19 00:00:00",
      "gender": "F",
      "id": 38,
      "name": "Zoe Sildana",
      "seeking_work": true
    }
  ],
  "success": true,
  "total_actors": 6
}
```

#### GET /actors/<actor_id>

Get information about one actor in the database

- Requires `read:actors`
- Returns a formatted `json` object of specified actor in the database
- Sample: `curl http://127.0.0.1:8080/actors/38 -H "Authorization: $CASTING_ASSISTANT"`

```javascript
{
  "actor": {
    "age": 41,
    "birthdate": "1978-06-19 00:00:00",
    "gender": "F",
    "id": 38,
    "name": "Zoe Sildana",
    "seeking_work": true
  },
  "success": true
}
```

#### POST /actors

Add an **Actor** to the database.

- Requires `add:actors`
- Returns a `json` response with the id of the new **Actor**, the number of **Actor**s in the database
- Sample `curl http://127.0.0.1:8080/actors -X POST -H "Authorization: $EXECUTIVE_PRODUCER" -H "Content-Type: application/json" -d '{"name": "Jane Doe", "birthdate": "1970-01-01", "gender": "F", "seeking_work": "true"}'`

```javascript
{
  "id": 39,
  "success": true,
  "total_actors": 7,
  "url": "/home"
}
```

#### PATCH /actors/<actor_id>

Modify an **Actor** in the database.

- Requires permission `edit:actors`
- data passed in request can be any number of **Actor** attributes:
  - name
  - birthdate
  - gender
  - seekingWork
- Returns a `json` object of the updated actor
- Sample: `curl http://127.0.0.1:8080/actors/39 -X PATCH -H "Authorization: $EXECUTIVE_PRODUCER" -H "Content-Type: application/json" -d '{"name": "Jane Dole"}'`

```javascript
{
  "success": true,
  "updated_actor": {
    "age": 50,
    "birthdate": "1970-01-01 00:00:00",
    "gender": "F",
    "id": 39,
    "name": "Jane Dole",
    "seeking_work": false
  }
```

#### DELETE /actors/<actor_id>

Remove an **Actor** from the database.

- Requires permission `delete:actors`
- Returns the name of the deleted actor
- Sample: `curl http://127.0.0.1:8080/actors/39 -X DELETE -H "Authorization: $EXECUTIVE_PRODUCER"`

```javascript
{
  "deleted_name": "Jane Dole",
  "success": true
}
```

#### GET /movies

Get a list of all **Movie**s in the database.

- Requires permission `get:movies`
- Returns a `json` object of all actors in the database as well as total number of movies
- Sample: `curl http://127.0.0.1:8080/movies -H "Authorization: $CASTING_ASSISTANT"`

```javascript
{
  "movies": [
    {
      "genre": "Adventure",
      "id": 8,
      "release_date": "2022-05-17 00:00:00",
      "title": "Indiana Jane"
    },
    {
      "genre": "Fantasy",
      "id": 7,
      "release_date": "2021-06-20 00:00:00",
      "title": "Store Wars"
    },
    {
      "genre": "Horror",
      "id": 9,
      "release_date": "2027-10-31 00:00:00",
      "title": "Saw 31"
    }
  ],
  "success": true,
  "total_movies": 3
}
```

#### GET /movies/<movie_id>

Get information about one **Movie** in the database

- Requires `read:movies`
- Returns a formatted `json` object of specified actor in the database
- Sample: `curl http://127.0.0.1:8080/movies/7 -H "Authorization: $CASTING_ASSISTANT"`

```javascript
{
  "movie": {
    "genre": "Fantasy",
    "id": 7,
    "release_date": "2021-06-20 00:00:00",
    "title": "Store Wars"
  },
  "success": true
}
```

#### POST /movies

Add a **Movie** to the database.

- Requires permission `add:movies`
- Returns the id of the new movie as well as the new number of total movies in the database.
- Sample `curl http://127.0.0.1:8080/movies -X POST -H "Authorization: $EXECUTIVE_PRODUCER" -H "Content-Type: application/json" -d '{"title": "The Time Before Land", "releaseDate": "2021-06-12", "genre": "Family"}'`

```javascript
{
  "id": 10,
  "success": true,
  "total_movies": 4
}
```

#### PATCH /movies/<movie_id>

Modify a **Movie** in the database.

- Requires permission `edit:movies`
- data passed in request can be any number of **Movie** attributes:
  - title
  - releaseDate
  - genre
- Returns a `json` object of the updated **Movie**
- Sample: `curl http://127.0.0.1:8080/movies/10 -X PATCH -H "Authorization: $EXECUTIVE_PRODUCER" -H "Content-Type: application/json" -d '{"genre": "Suspense"}'`

```javascript
{
  "success": true,
  "updated_movie": {
    "genre": "Suspense",
    "id": 10,
    "release_date": "2021-06-12 00:00:00",
    "title": "The Time Before Land"
  }
}
```

#### DELETE /movies/<movie_id>

Remove a **Movie** from the database.

- Requires permission `delete:movies`
- Returns the id of the deleted movie
- Sample: `curl http://127.0.0.1:8080/movies/10 -X DELETE -H "Authorization: $EXECUTIVE_PRODUCER"`

```javascript
{
  "deleted_title": "The Time Before Land",
  "success": true
}
```
