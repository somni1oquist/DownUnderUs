# About DownUnderUs

a description of the purpose of the application, explaining the its design and use.

# Group Members
| Student ID | Full Name | GitHub Username |
| ----------- | ----------- | ----------- |
| 23799876 | Lynn Huang | somni1oquist |
| 24063952 | Cynthia Chen | Cynthiachen2023 |
| 24074405 | Yali Ou | 10Yaly |
| 23308425 | Raspreet Khanuja | RaspreetK |

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

0. for Ras to go on