# Full Stack Trivia API Backend
[![Build Status](https://travis-ci.com/arthurarty/trivia.svg?branch=dev)](https://travis-ci.com/arthurarty/trivia)

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## API Documentation

### Get '/categories' 
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

### Get '/questions'
- Fetches a list of questions. Each formated as a dictionary. Also fetches all categories.
- Request Arguments: `page` (/questions/page=2)
- Example of output.
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract?"
    },
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
  ],
  "success": true,
  "total_questions": 21
}
```

### POST '/questions'
- Creates a new question or returns a question matching the search term.
- Required fields for creating a question: question - string, answer - string, category - int, difficult - int.

#### Creating a question.

Example of data to send.
```
{
	"question": "Who is Jim married to?",
	"answer": "Jim Herbert",
	"category": 2,
	"difficulty": 2
}
```
Curl example.
```
curl -X POST \
  http://127.0.0.1:5000/questions \
  -H 'Content-Type: application/json' \
  -d '{
	"question": "Who is Jim married to?",
	"answer": "Jim Herbert",
	"category": 2,
	"difficulty": 2
}'
```

Example of output
```
{
  "created": 30,
  "questions": [
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
  ],
  "success": true,
  "total_questions": 21
}
```

Possible errors.
```
1. 400 Bad request - Missing required field.
2. 422 Unprocessible - Data types for required fields.
``` 

#### Searching for questions
- Required field: searchTerm.
- Returns questions matching the search term or containing the search term.

Example of data to send.
```
{
	"searchTerm": "Jim"
}
```

Example of curl request.
```
curl -X POST \
  http://127.0.0.1:5000/questions \
  -H 'Content-Type: application/json' \
  -d '{
	"searchTerm": "Jim"
}'
```

Example of response.
```
{
  "questions": [
    {
      "answer": "Jim Herbert",
      "category": 3,
      "difficulty": 2,
      "id": 25,
      "question": "Who is Jim married to?"
    },
    {
      "answer": "Jim Herbert",
      "category": null,
      "difficulty": 2,
      "id": 27,
      "question": "Who is Jim married to?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

### Delete /questions/<int:question_id>
- Deletes a question with the id of question_id from the database. 

Curl example.
```
curl -X DELETE http://127.0.0.1:5000/questions/30
```
Example of output.
```
{
  "deleted": 30,
  "questions": [
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```

### Get /categories/<int:category_id>/questions
- Returns all questions in a given category.

Curl example. 
```
curl -X GET http://127.0.0.1:5000/categories/2/questions
```
Example of expected output.
```
{
  "current_category": 2,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism"
    },
    {
      "answer": "Micheal Scott",
      "category": 2,
      "difficulty": 1,
      "id": 24,
      "question": "Who was their first boss?"
    },
    {
      "answer": "Jim Herbert",
      "category": 2,
      "difficulty": 2,
      "id": 28,
      "question": "Who is Jim married to?"
    }
  ],
  "success": true,
  "total_questions": 6
}
```

### POST /quizzes 
- Returns questions in a random order.
- Required fields: quiz_category(dict), previous_questions(list of int)

Example of data to send
```
{
	"quiz_category": {"id": 1},
	"previous_questions": [21, 22, 20, 26]
}
```
Curl example
```
curl -X POST \
  http://127.0.0.1:5000/quizzes \
  -H 'Content-Type: application/json' \
  -d '{
	"quiz_category": {"id": 1},
	"previous_questions": [21, 22, 20, 26]
}'
```
Example of output
```
{
  "question": {
    "answer": "The office.",
    "category": 1,
    "difficulty": 1,
    "id": 26,
    "question": "Best comedy show?"
  },
  "success": true
}
```

### Possible errors
1. 400 - Bad request. Request missing a required field.
2. 404 - Resource not found. Question or category not found.
3. 405 - Method not allowed on given endpoint.
4. 422 -  Request unprocessable. 
5. 500 - Internal server error.

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```