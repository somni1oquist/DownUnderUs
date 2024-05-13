# About No Worries, Neighbour

Welcome to our web application, crafted to fulfill the requirements of the esteemed CITS5505 unit at UWA. Our platform is a testament to the power of web technologies harnessed to serve communities' needs effectively. Designed with a focus on user engagement, our application offers a robust set of features aimed at fostering meaningful interactions within the community. Central to this design are dynamic features such as a post and reply system, providing users with a platform to share thoughts, seek advice, and engage in lively discussions.

At the heart of our application lies a carefully curated incentives mechanism. We believe in recognizing and rewarding valuable contributions, thus, our points system incentivises user interaction and participation. By offering tangible benefits for engagement, we aim to cultivate a vibrant community where users are motivated to actively participate, share knowledge, and collaborate. Whether you're a student looking to engage with peers, a professional seeking insights, or an enthusiast eager to connect with like-minded individuals, our application provides a welcoming space designed to facilitate meaningful interactions and foster community growth.

# Group Members

| Student ID | Full Name        | GitHub Username |
| ---------- | ---------------- | --------------- |
| 23799876   | Lynn Huang       | somni1oquist    |
| 24063952   | Cynthia Chen     | Cynthiachen2023 |
| 24074405   | Yali Ou          | 10Yaly          |
| 23308425   | Raspreet Khanuja | RaspreetK       |

# Summary of Architecture

As per specification of the project, Python Flask framework is adopted for the app, alongside its extensitons e.g., Flask-Login, Flask-SQLAlchemy, Flask-Migrate and WTForms. The main program folder is `flask/`, containing main app files, database, migrations and tests. 

In addition, from the MVC perspective, since it's a mini-mid level size project, we put all models in `app/models.py` and all views in `app/templates/`. For controller part, we separate and name them by functionality and put them right under `flask/app/`.

For testing part, the `tests/` includes all selenium and unit tests.

The basic structure is as follow:
```
DownUnderUs/
├── flask/
│   ├── app/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   ├── images/
│   │   │   └── js/
│   │   ├── templates/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── auth.py
│   │   ├── post.py
│   │   └── ...
│   ├── instance/
│   │   └── duu.db
│   ├── tests/
│   │   ├── selenium_*.py
│   │   ├── ...
│   │   ├── test_*.py
│   │   └── ...
│   ├── migrations/
│   │   ├── versions/
│   │   │   └── ...
│   │   ├── alembic.ini
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── congif.py
│   └── requirements.txt
├── git-hook/
│   └── pre-commit
├── .gitignore
├── CodingRule.md
└── README.md
```

# Instructions for Launching Application

0. Make sure the directory in terminal is correct: in `flask/` folder.
1. Generate virtual environment for app: `python3 -m venv .venv`.
2. Activate virtual environment:
```
source .venv/bin/activate (Linux/Mac)
.venv\Scripts\activate (Windows)
```
3. Install all required packages: `pip install -r requirements.txt`.
4. Check database by `flask db check`, the command will generate database file if there is none.
5. Check if migrations are up-to-date and execuete: `flask db upgrade` to apply all migrations to the database file.
6. Enter shell by `flask shell` and type the following commands. It may take few minutes to generate images, after they're created press `Ctrl+D` to leave.
```
from test_fake_data import create_fake_data
create_fake_data()
```
7. Launch the app: `flask run` (add `--debug` parameter when developing) and access website through designated url.

# Instructions for Testing

## Test Configuration

The project utilizes a dedicated test configuration to ensure a consistent and isolated testing environment. Key features include:

**Testing Mode:** Enabled by setting TESTING to True, which activates testing behavior in the application.
**In-Memory Database:** Utilizes an in-memory SQLite database (sqlite:///:memory:) to avoid writing test data to disk, ensuring fast and efficient testing.
**CSRF Protection Disabled:** Disables CSRF protection (WTF_CSRF_ENABLED = False) to simplify testing of form submissions.

## Unit Tests

The project includes a set of automated unit tests to ensure the correctness of the application routes. To run the tests, please follow these steps:

1. Activate the virtual environmenet and directory under `flask/`.
2. Make sure all the required dependencies are installed.
3. Run the tests using the below commands:

#### Run All Tests

To recursively search the tests directory for any test files and run them, execute the following command:

```
python -m unittest discover -s tests -p 'test_*.py' -v
```

This command will execute all test cases found in the tests directory and its subdirectories.

#### Run a Specific Test File

To run tests from a specific file, use the following command:

```
python -m unittest tests.test_file_name -v
```

Replace test_file_name with the name of the specific test file to run, without the .py extension. For example, to run the tests in test_auth.py, use:

```
python -m unittest tests.test_auth -v
```

The test results will be shown in the terminal.

### Test Coverage

Test coverage tool is used to measure how much of the code is covered by tests. To generate a coverage report, run the following command:

```
coverage run -m unittest discover -s tests && coverage report
```

This command will run the tests and then print the coverage report in the terminal.

To generate and view the html coverage report, run below command:

```
coverage html
```

The generated HTML report is located in the 'htmlcov' directory. The index.html can be opened in the web browser to visualize the code coverage.

### Clean Up After Testing

After running the tests, the test cases automatically handle the clean up and removal of test data and resources.

**Per-Test Cleanup**: Individual test functions use the 'tearDown' method to roll back database transactions and pop the application context, effectively cleaning up any changes made during test.

With these cleanup procedures in place, tests are self-contained and do not leave any residual data or side-effects, ensuring the reliability and repeatability of test suite.

## Selenium Tests

### Run test
There are 3 selenium tests in the `tests/` folder, use the following command to run each selenium test:
```
python -m unittest tests.selenium_signup -v
python -m unittest tests.selenium_post -v
python -m unittest tests.selenium_search_reply -v
```
