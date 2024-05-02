# About DownUnderUs

a description of the purpose of the application, explaining the its design and use.

# Group Members

| Student ID | Full Name        | GitHub Username |
| ---------- | ---------------- | --------------- |
| 23799876   | Lynn Huang       | somni1oquist    |
| 24063952   | Cynthia Chen     | Cynthiachen2023 |
| 24074405   | Yali Ou          | 10Yaly          |
| 23308425   | Raspreet Khanuja | RaspreetK       |

# Summary of Architecture

# Instructions for Launching Application

0. Make sure the directory in terminal is correct: in `flask` folder.
1. Generate virtual environment for app: `python3 -m venv .venv`.
2. Activate virtual environment: `. .venv/bin/activate`.
3. Install all required packages: `pip install -r requirements.txt`.
4. Check database by `flask db check`, the command will generate database file if there is none.
5. Check if migrations are up-to-date and execuete: `flask db upgrade` to apply all migrations to the database file.
6. Launch the app: `flask run` (add `--debug` parameter when developing) and access website through desinated url.

# Instructions for Testing

## Test Configuration

The project utilizes a dedicated test configuration to ensure a consistent and isolated testing environment. Key features include:

**Testing Mode:** Enabled by setting TESTING to True, which activates testing behavior in the application.
**In-Memory Database:** Utilizes an in-memory SQLite database (sqlite:///:memory:) to avoid writing test data to disk, ensuring fast and efficient testing.
**CSRF Protection Disabled:** Disables CSRF protection (WTF_CSRF_ENABLED = False) to simplify testing of form submissions.

## Unit Tests

The project includes a set of automated unit tests to ensure the correctness of the application routes. To run the tests, please follow these steps:

1. Activate the virtual environmenet.
2. Make sure all the required dependencies are installed.
3. Run the tests using the below commands:

#### Run All Tests

To recursively search the tests directory for any test files and run them, execute the following command:

```
python -m unittest discover -s tests -v
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

---
