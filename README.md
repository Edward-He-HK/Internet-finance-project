# Internet-finance-project

> A React-Redux game loop.

## Table of Contents

* [Introduction](#introduction)
* [Description](#description)
  * [Backend server](#backend-server)
  * [Frontend application](#frontend-application)

## Introduction

This is a mini project related to blockchain and iOS app development. User can perform transaction and mining through our iOS application with a backend server to handle the requests. This project is implemented with all fundemental blockchain functions.

## Description

### Backend server

The backend server is write in Python and hosted in an AWS EC2 instance. Python 3 is used to compile the python code. Run the server.py program in the linux OS can start the backend program. The backend will handle all the transaction requests and the CRUD operations from the frontend mobile appllication. 

```
python3 server.py 5000
```

### Frontend application

The frontend application is for iOS environment with swift programming.
