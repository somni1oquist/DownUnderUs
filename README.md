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
3. Install all packages: `pip install -r requirememts.txt`.
4. Create databse if first time: `flask db init`. This should create the database file.
5. Check if all migrations are there and execuete: `flask db upgrade`. It will apply all migrations to the database file.
6. Launch the app: `flask run`.

# Instructions for Testing