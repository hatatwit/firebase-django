# firebase-django
A website allows users to store and share files with multiple users, get updated on announcements and schedule events. Following every steps in the firebase-django-tutorial-version5.doc to replicate the website with detail and effective instructions.

## Installation

```bash
$ git clone https://github.com/hatatwit/firebase-django.git
$ cd firebase-django
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py runserver

```

# Demo

### index.html
Homepage where users need to sign in/sign up to access any features of the website.
![alt text](https://github.com/hatatwit/firebase-django/blob/master/homePage.png?raw=true)

![alt text](https://github.com/hatatwit/firebase-django/blob/master/userAuth.png?raw=true)


### doc.html
Document page where users add and store any files to share it with others.
![alt text](https://github.com/hatatwit/firebase-django/blob/master/doc.png?raw=true)

### event.html
Event page where users schedule a new event with the purpose, time and date of the event.
![alt text](https://github.com/hatatwit/firebase-django/blob/master/event.png?raw=true)

### post.html
Post page where users post announcements that other users can also see it.
![alt text](https://github.com/hatatwit/firebase-django/blob/master/announce.png?raw=true)


## Build with
Web technologies: HTML, CSS, Bootstrap, Python, Django 

Server and Other Tools: Firebase, GCP, Dockerfile

Database: Firebase Realtime Database

## License

[MIT](https://choosealicense.com/licenses/mit/)





