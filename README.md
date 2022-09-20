# Car rental
Link to live version: https://swampy-car-rentals.azurewebsites.net

## Table of contents
* [General info](#General-info)
* [Technologies](#Technologies)
* [Setup](#Setup)
* [Features](#Features)
* [Dev decisions & personal goals](#Dev-decisions)

### General info
This is a car rental project made with Django. This site allows you to manage a relatively simple car rental company.
The application allows you to add and remove cars from the fleet and assign a car to a given user in order to rent a car. The user can browse the cars and rent a car.


### Technologies
Project is created with: 
* Python 3.9.0
* Django 4.0.4
* Pillow 9.1.0
* python-dotenv 0.20.0
* Bootstrap 5
* django-filter 21.1
* reportlab 3.6.10


### Setup 
Being a Python web framework, Django requires Python. You can verify that Python is installed by typing python from your shell:
`python3 --version` 

If you don't have Python installed you can go to (https://www.python.org/downloads/) to download it.

Creating a new virtual environment: 
`$ python3 -m venv myenv`

Start the virtual environment with the command:
`myenv\Scripts\activate.ps1`

Then you should clone the repository:
`$ git clone https://github.com/sda-project-group/car-rent.git`
`$ cd car-rent`

Then install the dependencies:
`(myenv)$ pip install -r requirements.txt`

Once pip has finished downloading the dependencies:

`(myenv)$ cd project`
`(myenv)$ python manage.py runserver`

And navigate to http://127.0.0.1:8000


### Features

Customer:
* account registration and profile editing
* logging in to the customer account
* password change
* viewing the cars available at the rental company
* renting a car in a selected period of time after checking if the car is available
* checking his orders (pending, past and future)
* rental period change for individual orders - if dates allow


Administrator:
* creating accounts for employees
* deleting and editing customer and employee accounts
* granting permissions to users
* approval of car edits
* adding cars to the fleet
* car removal

Employee:
* editing cars (must be approved by the administrator)
* handling car returns for a given day
* handling late car returns, or problematic cases

### Dev decisions & personal goals

Some context:

* This project`s purpose was educational. 
* Our aim was to practice working as an online team, to achieve the goals set in a design document.
The idea was to deliberately create features as they were designed  - as opposed to putting in whatever we have managed to work.
* It started as a 5-man team but 2 have left making close to no contributions and the third - Gosia - has heavily contributed in the first period, but discontinued work after moving the project to this repository.
* Most of the contributions by Przemek and Roman were a pair-effort, meaning that we had been working on the same problem together at the same time but only one was making a given commit 
* As we are all beginner level python devs, the front end part of the project has low priority (if it`s not an eyesore - it is good enough)

*All the above had some influence on our subsequent decisions.* We have decided, for instance, to honour the work of Gosia and leave as much of her code and front-end design as possible even if it costed us some visual integrity, or we knew we would have done things differently.

There are parts of a site that handle certain tasks differently - a good example would be error messages.
This is not because of an omission, or an error but rather a deliberate decision made to ensure that we learn various ways of achieving the same goal and their pros and cons.
