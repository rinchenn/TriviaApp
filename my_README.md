## Local Development
The instruction below are meant for the local development setup.
## Backend
### Pre-requisites
* Python3, pip/pip3 and node should be already installed on the local machine

* **Start your virtual environment**
From the backend folder run
```
# Mac users
python3 -m venv venv
source venv/bin/activate

# Windows users
python -3 -m venv venv
venv\Scripts\activate
```

* **Install dependencies**<br>
From the backend folder run
```
# All required packages are included in the requirements.txt file.
pip3 install -r requirements.txt
```

##Database setup
### Step 0: Start/Stop the PostgreSQL server
Mac users can follow the commands below:
```bash
which postgres
postgres --version
# Start/stop
pg_ctl -D /usr/local/var/postgres start
pg_ctl -D /usr/local/var/postgres stop 
```
Windows users can follow the commands below:
- Find the database directory, it should be something like that: *C:\Program Files\PostgreSQL\13.2\data*
- Then, in the command line, execute the folllowing command: 
```bash
# Start the server
pg_ctl -D "C:\Program Files\PostgreSQL\13.2\data" start
# Stop the server
pg_ctl -D "C:\Program Files\PostgreSQL\13.2\data" stop
```
If it shows that the *port already occupied* error, run:
```bash
sudo su - 
ps -ef | grep postmaster | awk '{print $2}'
kill <PID> 
```

### Step 1 - Create and Populate the database
1. **Verify the database username**<br>
Verify that the database user in the `/backend/trivia.psql`, `/backend/models.py`, and `/backend/test_flaskr.py` files must be `postgres` (default username).
2. **Create the database, tables and apply constraints**<br>
In your terminal, navigate to the */TriviaApp/backend* directory, and run the following:
```bash
cd TriviaApp/backend
# Connect to the PostgreSQL
psql postgres
#View all databases
\l
# Create the database, create a user - `student`, grant all privileges to the student
\i trivia.sql
# Exit the PostgreSQL prompt
\q
```
### Run the Backend Server
Navigate to the `/backend` folder run the following commands.
```
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run --host=0.0.0.0
```
These commands put the application in development and directs our application 
to use the `__init__.py` file in our flaskr folder. Working in development mode shows an 
interactive debugger in the console and restarts the server whenever changes are made. 

##FrontEnd 

### Navigate to the `/frontend` folder and run the following commands 
```
npm install // only once to install dependencies
npm start 
```
By default, the frontend will run on `localhost:3000`. 

## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```
The APIs will return four error types when reqeusts fail:
- 400: Bad request
- 404: Resource not Found
- 405: Method not Found
- 422: Not Processable

## Endpoints
#### GET /categories
- General:
    - Returns a list of trivia categories, success value and total number of categories
- Sample: `curl http://127.0.0.1:5000/categories`
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
  "success": true,
  "total_categories": 6
}
```
#### GET /questions
- General:
    - Returns a list of questions, success value, list of categories and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose a page number, starting from 1.
- Sample: `curl http://127.0.0.1:5000/questions?page=2`
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
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
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
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
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
    {
      "answer": "Asia",
      "category": 3,
      "difficulty": 1,
      "id": 29,
      "question": "Which continent Bhutan is in?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```
#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question and the success value.
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/1`
```
{
    "success": true,
    "delete_question_id": 1
}
```
#### POST /questions
- General:
    - Create a new question using the submitted question, answer, category ID and difficulty level. Returns the id of the 
    created question, question category, success value and the total questions. 
- Sample: `curl http://127.0.0.1:5000 -X POST -H "Content-Type: application/json" -d '{"questio":"", "answer":"","category id":3, "difficulty": 1 }'`
```
{
    "success": true,
    "created": 20,
    "current_category": 3,
    "total_questions": 20
}
```
#### POST /search/questions
- General:
    - Get all the questions based on the search term. Returns all the questions which is the search term is 
    a substring of the question.
    - Results are paginated in groups of 10.
- Sample: `curl http://127.0.0.1:5000/search/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}`
```
{
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```
#### GET /categories/{category_id}/questions
- General:
    - Returns a list of questions based of category, success value and total question in the selected category
- Sample: `curl http://127.0.0.1:5000/categories/1/questions`
```
{
  "questions": [
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
    }
  ],
  "success": true,
  "total_questions": 3
}

```
#### POST /quizzes
- General:
    - Returns a random question, success value and list of previous questions
    - The previous questions list is not included in the random selection
- Sample: ` curl http://127.0.0.1:5000/quizzes -X POST -H 'Content-Type: application/json' -d '{"previous_questions": ["1"], "quiz_category": {"id": 0}}'`
```
{
  "previous_questions": [
    "1"
  ],
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
}
```

## Additional information
#### Running Tests
Navigate to the `/backend` folder and run the following commands: 
```bash
psql postgres
dropdb trivai_test
createdb trivia_test
\q
psql trivia_test < trivia.psql
python test_flaskr.py
```