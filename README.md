# RESTful API for managing photos
## Task
Design and implement a simple backend application for managing photos.

We want to store photo `title`, `album ID`, `width`, `height` and dominant `color` (as a hex code) in local database; the files should be stored in local filesystem.

Functionalities:
- Photos REST resource (list, create, update, delete)
    - Output fields (list): `ID`, `title`, `album ID`, `width`, `height`, `color` (dominant color), `URL` (URL to locally stored file)
    - Input fields (create, update): `title`, `album ID`, `URL`
- Import photos from external API at `https://jsonplaceholder.typicode.com/photos` via both
REST API and a CLI script
- Import photos from JSON file (expecting the same data format as the external API's); via
both REST API and a CLI script

Suggestions:
- Use any frameworks and libraries you'll find useful for the task (we prefer Django)
- Try to follow the best coding practices
- Don't be afraid to write tests

## Start
1) Export environment variables (example in `.env.example`) or use default settings.

2) `pip3 install -r src/requirements.txt`

3) `python3 src/app/manage.py migrate`

4) `python3 src/app/manage.py runserver`

### Docker
1) Override `.env.example` file or create new (in this case you would also need to change environment file in `docker-compose.yml`).

2) `docker-compose up --build`

## Importing photos

To import photos from external API (`https://jsonplaceholder.typicode.com/photos`) or JSON file you can use API or django admin command.

### Import using API

From API: `GET /api/photos/import/from-api`

From JSON: `GET /api/photos/import/from-json`

For slicing use `start` and `limit` parameters.

For example:
```
GET /api/photos/import/from-api?limit=10
GET /api/photos/import/from-api?start=3&limit=10

GET /api/photos/import/from-json?limit=10
GET /api/photos/import/from-json?start=3&limit=10
```

### Import using CLI
`python3 src/app/manage.py import_photos_api`
`python3 src/app/manage.py import_photos_json`

For slicing use `--start` and `--limit` parameters.
