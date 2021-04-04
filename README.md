# Token Authentication
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Running the code](#running-our-code)
- [Conclusion](#conclusion)
## Introduction

This project is focused on CRUD(Create, Read, Update, Delete) Operations on Database by using [sqlite3](https://docs.python.org/3/library/sqlite3.html) module in python.
This python script performs the following operations.
1. Create - Insert a new instance in users and tokens tables when a new Unique UserID tries to create a new token.
2. Read - When checking for the Token ID, we perform SELECT the record with the TokeID.
3. Update - When Users TokenID is expired, and the user tries to access it, we update the token's expiry date.
4. Delete - When users opt for deleting the token, we delete the instance in the database. 

## Requirements
> To run this file, we required [Flask](https://pypi.org/project/Flask/) module.
- Run the below command in the Terminal to install the flask module in python.
```python
pip install Flask
```
or just run the below command in Terminal
```
pip install -r requirements.txt
```
## Running our code
- ## Running on Terminal
Open the Terminal, navigate to the directory where application.py belongs, run the below command, and open up the link for accessing the web application.
```python
flask run
```

## Conclusion
- This project aims to interact with the databases while we log on to our accounts on the web. By developing this project, I hope you know how web pages work and interactions with the databases on the Internet. If you find any bugs or want to improve this project. Please, fork this repo. 

## Contribute
**Contributions are always welcome.**
