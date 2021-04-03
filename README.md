# Token Authentication
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Running the code](#running-our-code)
- [Conclusion](#conclusion)
## Introduction

This project is focused on CRUD(Create, Read, Update, Delete) Operations on Database by using [sqlite3](https://docs.python.org/3/library/sqlite3.html) module in python.
This python script performs the following operations.
1. Create - Insert a new instance in users and tokens tables, when new Unique UserID tries to create a new token.
2. Read - When checking for the Token ID, we are performing SELECT the record with the TokeID.
3. Update - When Users TokenID is expired and user tries to access it, we update the expiry date of the token.
4, Delete - Todo

## Requirements
> To run this file we required [Flask](https://pypi.org/project/Flask/) module.
- Run the below command in terminal to install flask module in python.
```python
pip install Flask
```
or just run the below command in terminal
```
pip install -r requirements.txt
```
# Running code
- ## Running on Terminal
- Open the Terminal, and navigate to the directory, where application.py belongs and run the below command.
```python
flask run
```

# Conclusion
-