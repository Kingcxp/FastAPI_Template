# Project Name
### Author: author

## Description
Contents of project description

## Installation
(You should have `python` and `git` installed first)
```sh
# Clone this project
git clone https://git.nju.edu.cn/gh_user/project_name.git
cd project_name
# create a virtual environment
python3 -m venv serverenv
# activate the virtual environment
# Bash
source serverenv\Scripts\activate
# Fish
source serverenv/Scripts/activate.fish
# Powershell
.\serverenv\Scripts\Activate.ps1
# Install dependencies
pip install -r requirements.txt
# Run the server
uvicorn app:app --port 8081 --host 0.0.0.0 --reload
```

## About email
If you want to send emails, you need to create a .env file with the following content:
```txt
EMAIL="user@example.com"
EMAIL_PASSKEY="YOUR_PASSKEY"
EMAIL_HOST="smtp.example.com"
```

## Contribute
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
