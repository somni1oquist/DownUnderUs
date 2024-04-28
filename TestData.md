Guidline for generate test data:

Step1: run venv environment
Unix or Mac: source venv/bin/activate
Windows: venv\Scripts\activate

Step2: run flask shell
Command: flask shell

Step3: import create_fake_posts function
Command:
from app.test_fake_data import create_fake_posts
create_fake_posts(50)
create_fake_users(20)

create_fake_posts(50) will generate 50 posts
create_fake_users(20) will generate 20 users