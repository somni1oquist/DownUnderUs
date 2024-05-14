# Instructions for Launching Scenario_data_post

Follow these steps to prepare and execute Scenario_data_post effectively:

## Step 0: Activate the Virtual Environment
Ensure that the Python virtual environment for your Flask project is activated before you start.

## Step 1: Generate fake data
Enter shell by `flask shell` and type the following commands. After that press `Ctrl+D` to leave.
```
from test_data.test_fake_data import create_fake_data
create_fake_data()
```

## Step 2: Create a Python Script File
In the `flask/test_data/` directory, create a new Python file named `scenario*.py` (replace `*` with your specific scenario number or name).

## Step 3: Import Modules
Inside your newly created file, import the necessary modules from `scenario_data_post`:
```python
from scenario_data_post import create_post, create_replies
```
## Step 4: Write Post and Reply Content
Refer to the `example scenario1.py` file to draft your post and reply content. This file provides a template and example data to guide you in creating realistic and coherent posts and replies.

## Step 5: Upload Images
Upload the images required for the posts or replies to the directory `flask/app/static/images/scenario*` (replace * with your scenario number or name). Ensure that the images are appropriately named and formatted for web use.

## Step 6: Execute Scenario via Flask Shell
Enter shell by `flask shell` and type the following commands. After that press `Ctrl+D` to leave.
```
from test_data.scenario* import scenario*
scenario*()
```
Replace all occurrences of scenario* with your file name.

## Step 7: Integrate the New Scenario Module into `test_fake_data.py`
To initialize the scenario data with your test data, integrate the scenario module into `test_fake_data.py`. First, add the import statement at the beginning of the file:
```python
from scenario* import scenario*
```
Next, to execute the scenario and confirm its creation, insert the following code into the `create_fake_data` function:
```python
scenario*()
print("Created scenario* data")
```
Replace all occurrences of scenario* with your specific scenario number or name to ensure the script references the correct module and function.