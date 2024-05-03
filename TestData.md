# Guideline for Generating Test Data:

- Step0: Prerequisites

Make sure you're under `flask` directory.
```
cd flask
python3 -m venv .venv
```

- Step1: Run Virtual Environment
```
source .venv/bin/activate (Linux/Mac)
.venv\Scripts\activate (Windows)
```

- Step2: Libraries and Database
```
pip install -r requirements.txt
flask db check # Create database if not exists
flask db upgrade
```

- Step3: Flask Shell
```
flask shell
```

- Step4: Import Method
```
from test_fake_data import create_fake_data()
create_fake_data()
```

 It may take few minutes to generate images, after they're created press `Ctrl+D` to leave.