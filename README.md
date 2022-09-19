# Friendship Test Web App

## Setting up a local build
In order to run this on your local, follow these steps
```
1. Rename template.env on project root to .env
2. In .env, add database credentials
3. run "python manage.py migrate" in shell.
4. run "python manage.py load_sample_questions" in shell to load sample data.
5. Finally, run the server. "python manage.py runserver"
```
## Usage
The homepage contains link to create a quiz.

1. User can click on that to start creating a quiz.
2. Backend will select 10 random questions from database
3. After a successful submission, user will get a unique link
4. Friends can open user's unique quiz link and answer the questions
5. After successful submission, app will show the percentage of answers got matched with the quiz owner's answer

## Running Tests
To run test cases, use the following in shell
```bash
python3 manage.py test ftest.tests --settings=app.test_settings
```

## Notes

#### Questions mapping
I've added question template mapping as well where user and friends will see same question in different way.
for example:
```
User: What is your favorite color?
Friends: What is John's favorite color?
```

#### Sample Data
Since we have all the necessary information, this can be further extended to show user his friend/s submissions as well.

I've also added a migration script with sample json file to get 20 sample questions
```bash
python manage.py load_sample_questions
```

#### SCSS
I've added gulp configuration `./fe_compilers/gulp` to compile scss files and compress the main stylesheet.
