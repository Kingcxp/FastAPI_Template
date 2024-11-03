# Project Name
### Author: author

## Description
This is the backend of Project name.

## Installation
(You should have `python` and `git` installed first)
```sh
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

## Contribute
Change the codes and submit a pull request.
