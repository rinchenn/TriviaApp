### Error Handling
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

### Endpoints
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
