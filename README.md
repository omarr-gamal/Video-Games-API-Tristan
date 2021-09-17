# Video-Games-API-Tristan

This is a video games api that offers information about video games' release statuses, development studios ratings and genres. Please note that the api is for educational purposes only, and so it may contain inaccurate or placeholder data. it is also worth mentioning that this is a work in progress.

Check out the api running live [here](https://tristan-game-api.herokuapp.com)

## Running the app locally

If you want to run the app locally on your machine then follow the instructions below

### Installing Dependencies

#### Python 3.7

The first thing you will need is Python. You can follow these instructions to install the latest version [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

Now you need to install the project dependencies, but before you do it's recommended to use a virtual environment in order to separate dependencies of different projects. Take a look at Python's documentation for virual enviornment here [python docs](https://docs.python.org/3/library/venv.html)

#### Project Dependencies

to install the project dependencies you can run the command

```bash
pip install -r requirements.txt
```

in the project's root directory. This will install all the required packages from `requirements.txt` file.

#### Running the server

Double click `app.py` file to start the server. Make sure it's working correctly by navigating to `http://localhost:5000`

## API Endpoints Documentation

Read the following documentation for the api endpoints if you want to experience with the api.

### Endpoints

```json
GET '/games'
GET '/games/<certain_game_id>'
POST '/games'
PATCH '/games/<certain_game_id>'
DELETE '/games/<certain_game_id>'
```

#### GET '/games'

- Fetches a list of all games in the api
- Request Arguments: None
- Returns: a list of objects each resembling a video game. Response has the following format:

```json
{
    "success": true,
    "games": [
        {
            "id": 1,
            "name": "game_1",
            "description": "game_1_description",
            "release_date": "19/4/22",
            "released": false,
            "rating": 88,
            "critic_rating": 93,
            "PEGI_rating": 13,
            "genres": "action",
            "developer": "developer_1",
            "publisher": "publisher_1",
        },
        {
            "id": 2,
            "name": "game_2",
            "description": "game_2_description",
            "release_date": "19/4/20",
            "released": true,
            "rating": 95,
            "critic_rating": 100,
            "PEGI_rating": 18,
            "genres": "action",
            "developer": "developer_2",
            "publisher": "publisher_2",
        }
    ]
}
```

#### GET '/games/<certain_game_id>'

- Fetches the game with `id = certain_game_id` or 404 if not found.
- Request Arguments: None
- Returns: An object resembling the video game. Response has the following format:

```json
{
    "success": true,
    "games": {
        "id": 1,
        "name": "game_1",
        "description": "game_1_description",
        "release_date": "19/4/22",
        "released": false,
        "rating": 88,
        "critic_rating": 93,
        "PEGI_rating": 13,
        "genres": "action",
        "developer": "developer_1",
        "publisher": "publisher_1",
    }
}
```

#### POST '/games'

- Lets you add a game to the api's list of games.
- Request Arguments: the request must have the following format:

```json
{
    "name": "game_1",
    "description": "game_1_description",
    "release_date": "22/3/21",
    "rating": 88,
    "critic_rating": 93,
    "PEGI_rating": 13,
    "genres": "action",
    "developer": "developer_1",
    "publisher": "publisher_1",
}
```

Please note that `release_date` has the following format `d/m/y`

- Returns: if the game was added successfully, the response will have the following format:

```json
{
    "success": true,
}
```

#### PATCH '/games/<certain_game_id>'

- Lets you edit a game.
- Request Arguments: the request must have the following format:

```json
{
    "name": "game_1",
    "description": "game_1_description",
    "release_date": "22/3/21",
    "rating": 88,
    "critic_rating": 93,
    "PEGI_rating": 13,
    "genres": "action",
    "developer": "developer_1",
    "publisher": "publisher_1",
}
```

Note that all properties in the above request are optional. If you included property `name` in your request, then the game's `name` property will be updated.

- Returns: if the request was processed successfully, the response will have the following format:

```json
{
    "success": true,
}
```

#### DELETE '/games/<certain_game_id>'

- Deletes the game with the id certain_game_id
- Request arqument: None.
- Returns: if the request was processed successfully, the response will have the following format:

```json
{
    "success": true,
}
```

## Authorization

Some of the endpoints in the api require you to have permissions in order to process your requests. The permissions needed for the api endpoints are:

| endpoint                           | permission            |
| ---------------------------------- | --------------------- |
| GET '/games'                       | get:games             |
| GET '/games/<certain_game_id>'     | get:games             |
| POST '/games'                      | post:games            |
| PATCH '/games/<certain_game_id>'   | patch:games           |
| DELETE '/games/<certain_game_id>'  | delete:games          |

these permissions are provided as part of the JWT that you include in your request before sending it. To ensure that the JWT gets processed correctly, in your request's headers include this header `"Authorization": "Bearer JWT"`. Replace `JWT` with the JWT that contains the permissions and do not forget the space.

At the moment the api does not have a front end through which you can create a account and get permissions and JWTs. That's why in `access tokens.txt` you can find two JWTs that have the permissions needed to interact with the api. The first one is for a guest user and has only the permission to view games in the api. The second is for an admin user and has all permissions.

## Testing

If you are running the app locally and would like to run the unittest script that contains tests I wrote for the api endpoints to ensure that it's working correctly, then run the following

```bash
python test_app.py
```
