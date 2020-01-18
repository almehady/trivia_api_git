# A RESTful API for a trivia game. 

## Deploy the REACT front-end, test using Python unittest and complete full documentation, including API


Goal: Build a RESTful API and ensure that it connects and responds successfully to the REACT front-end. Test the API using Python Unittest and fully document the API in the project readme file.

Tasks Completed:
1. Build RESTful API using Python, Flask & SQLAlchemy. API contains GET, POST, PATCH and DELETE endpoints and is complete with appropriate error handlers.
2. Build test script using unittest. Deploy a test database and ensure all endpoints and error handlers are behaving as expected.
3. Complete full documentation of the API and post on the repo's README.
4. Deploy REACT front-end and test the web application works as expected.

# How to run the app | please find the respective document in README.md folder. i.e. frontend/README.md or backend/README.md

API Documentation:
```
Endpoints
GET '/categories'
GET '/questions'
GET '/categories/{id}/questions'
POST '/questions'
POST '/quizzes'
DELETE '/questions/{id}'


GET '/categories'
curl http://apiurl.com/categories
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

----------------------------------------------------------------------------------------------------------------------------------------------------------

GET '/questions'
curl http://apiurl.com/questions
- Fetches a list of all questions stored in the database, ordered by id.
- Request Arguments: page
- Returns: An object containing a list of categories, the category currently filtered on (all), a list of up to 10 questions (containing question id, question, answer, category and difficulty), and the total number of questions in the database will be returned. The request argument "page" can be used to choose which page of 10 questions to retrieve. For example /questions?page=2 will retrieve questions 11-20.
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "all",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
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
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
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
    }
  ],
  "success": true,
  "total_questions": 41
}


----------------------------------------------------------------------------------------------------------------------------------------------------------


GET '/categories/{id}/questions'
curl http://apiurl.com/categories/6/questions
- Similar to GET '/questions', but fetches a list of all questions filtered by category, ordered by question_id. The id of the category required must be used to filter the questions.
- Request Arguments: page
- Returns: An object containing a list of categories, the category currently filtered on (all), a list of up to 10 questions (containing question id, question, answer, category and difficulty), and the total number of questions in the category will be returned. The request argument "page" can be used to choose which page of 10 questions to retrieve. For example /categories/6/questions?page=1 will retrieve questions 1-10 for question category 'Sports' only.
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": 6,
  "questions": [
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
      "answer": "TEST",
      "category": 6,
      "difficulty": 1,
      "id": 55,
      "question": "TEST SPORT"
    },
    {
      "answer": "TEST",
      "category": 6,
      "difficulty": 1,
      "id": 58,
      "question": "TEST SPORTSES"
    }
  ],
  "success": true,
  "total_questions": 4
}


----------------------------------------------------------------------------------------------------------------------------------------------------------


POST '/questions' (No search term provided)
curl -X POST -H "Content-Type: application/json" -d '{"question": "whats the time?", "answer":"its time to get ill", "category":5, "difficulty":1}' http://apiurl.com/questions?page=2
- Uses json data provided in the request to create a new question in the database.
- Data format required:
{
  "question": <str>,
  "answer": <str>,
  "category": <int> 1-6
  "difficulty": <int> 1-5
}
- Request Arguments: page
- Returns: After creating the new question, an object containing the text of the newly created question, a list of up to 10 questions (containing question id, question, answer, category and difficulty), and the total number of questions in the database will be returned. The request argument "page" can be used to choose which page of 10 questions to retrieve. For example /questions?page=2 will retrieve questions 11-20.
{
  "created": "whats the time?",
  "questions": [
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
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
      "answer": "its time to get ill",
      "category": 3,
      "difficulty": 1,
      "id": 28,
      "question": "whats the time?"
    }
  ],
  "success": true,
  "total_questions": 44
}


----------------------------------------------------------------------------------------------------------------------------------------------------------


POST '/questions' (Search term provided)
curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"occe"}' http://apiurl.com/questions?page=1
- Uses the searchTerm data provided in the request to filter the questions by question text. Returns all questions where the search term is included in the question text (case insensitive).
- Data format required:
{
  "searchTerm": <str>
}
- Request Arguments: page
- Returns: An object containing the list of questions where a match was found (containing question id, question, answer, category and difficulty), and the total number of matching questions will be returned. The request argument "page" can be used to choose which page of 10 questions to retrieve. For example /questions?page=2 will retrieve numbers 11-20 of matching questions.
{
  "questions": [
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
  "total_questions": 2
}


----------------------------------------------------------------------------------------------------------------------------------------------------------


POST '/quizzes'
curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[38,52],"quiz_category":{"type":"Science","id":"1"}}' http://apiurl.com/quizzes
- Uses json data provided in the request to fetch a randomly selected question of a given category, which is not included in the list of previously returned questions.
- Data format required:
{
  'previous_questions':[<int>,<int>],
  'quiz_category':{
    'type': <str>,
    'id': <int> 0-6
  }
}
- Request Arguments: None
- Returns: An object containing details of the "next" question in the quiz game (containing question id, question, answer, category and difficulty).
{
  "question": {
    "answer": "Alexander Fleming",
    "category": 1,
    "difficulty": 3,
    "id": 21,
    "question": "Who discovered penicillin?"
  },
  "success": true
}


----------------------------------------------------------------------------------------------------------------------------------------------------------


DELETE '/questions/{id}'
curl -X DELETE http://apiurl.com/questions/21?page=2
- Takes the question_id provided in the request and deletes the object from the database.
- Request Arguments: page
- Returns: As well as the id of the deleted question, the request will return a list of up to 10 questions (containing question id, question, answer, category and difficulty), and the total number of questions in the database. The request argument "page" can be used to choose which page of 10 questions to retrieve. For example /questions/42?page=2 will retrieve questions 11-20.
{
  "deleted": 42, 
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
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
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
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
    }
  ],
  "success": true,
  "total_questions": 39
}

```