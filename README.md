# Spaced Repetition API: Proof of Concept

Created as part of an EdTech Fellowship with Menon Labs. Our team worked on building an e-learning chatbot for underprivileged students with Rising Academies: https://www.risingacademies.com/
Interested in what spaced repetition is? See here: https://ncase.me/remember/
The API is deployed at https://rori-api.herokuapp.com/.

Endpoints:
- /user [GET]: Retrieve details of all users from the database.

- /user [POST]: Add a new user to the database.
Body:
{
  name: String, user's name
}

- /getquestion [GET]: Retrieve a question from the database to ask to the user.

- /answer [POST]: Answer the question retrieved previously with /getquestion.
Body:
{
  answer: String, user's answer
}

- /checkuser [POST]: Check if a user is playing with Rori for the first time. Redirect to the diagnostic test if so, and the main activity if not.
{
  name: String, user's name
}

**How it works:**
- Each question has a "time" attached to it, which is a number. Every time /getquestion is called, the bot decreases the current time of every question the user has answered by 1. It then checks if a) there are either any questions the user has not answered yet or b) there are any questions the user has answered whose time is 0. If no questions fit this criteria, the bot will mention that there are no questions left for today. The user can come back tomorrow and get another question. 
- When a user answers a question correctly, the time it will take before the question is asked again (which we call the "interval") doubles. For example, if it took 2 GET requests to /getquestion before a certain question's time is 0, it will now take 4 requests for that same question's time to be 0.
- When a user answers a question incorrectly, the question's current time and interval is automatically set to 1, so the question is prioritized for future sessions. 
