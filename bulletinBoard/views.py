from django.shortcuts import render, redirect
from django.contrib import auth
import pyrebase
import datetime
import re

config = {
    "apiKey": "AIzaSyBnjPbt239hSnxpt29goF60-R85HErLuTo",
    "authDomain": "fir-django-a355c.firebaseapp.com",
    "projectId": "fir-django-a355c",
    "storageBucket": "fir-django-a355c.appspot.com",
    "messagingSenderId": "162110570998",
    "appId": "1:162110570998:web:fdff7d57d334449f7c07d7",
    "measurementId": "G-2JWGY8HH2T",
    "databaseURL":"https://fir-django-a355c-default-rtdb.firebaseio.com/",
    "serviceAccount": "fir-django-a355c-sdk.json",
}
# Initializing database, auth and firebase for further use
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()

# Homepage view
def homepage(request):

    return render(request, "index.html")


# Authentication views
def signIn(request):
    return render(request, "signIn.html")


def postsignIn(request):
    email = request.POST.get('email')
    pw = request.POST.get('pass')
    try:
        # if there is no error then signin the user with given email and password
        user = authe.sign_in_with_email_and_password(email, pw)
    except:
        message = "Your account or password is incorrect. If you don't remember your password, reset it now."
        return render(request, "signIn.html", {"message": message})
    session_id = user['idToken']
    request.session['uid'] = str(session_id)

    return render(request, "welcome.html", {"email": email})


def signOut(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request, "index.html")


def signUp(request):
    return render(request, "signUp.html")


def postsignUp(request):
    username = request.POST.get('username')
    email = request.POST.get('email')
    pw = request.POST.get('pass')

    try:
        # creating a user with the given email and password
        user = authe.create_user_with_email_and_password(email, pw)
        uid = user["localId"]
        data = {"username": username, "email": email, "pass": pw}
        database.child("users").child(uid).set(data)
        message = "Successfully create new account"
        return render(request, "signIn.html", {"message": message})
    except:
        message = "Unable to create account"
        return render(request, "signUp.html", {"message": message})


def reset(request):
    return render(request, "reset.html")


def postReset(request):
    email = request.POST.get('email')
    try:
        authe.send_password_reset_email(email)
        message = "A email to reset password is succesfully sent"
        return render(request, "reset.html", {"message": message})
    except:
        message = "Something went wrong, Please check the email you provided is registered or not"
        return render(request, "reset.html", {"message": message})


# Document views
def document(request):
    get_time = database.child('archive').child('documents').shallow().get().val()
    try:
        docId = []
        for i in get_time:
            docId.append(i)

        date = []
        title = []
        url = []
        for i in docId:
            get_date = database.child("archive").child("documents").child(i).child("date").get().val()
            get_title = database.child("archive").child("documents").child(i).child("title").get().val()
            get_url = database.child("archive").child("documents").child(i).child("url").get().val()
            title.append(get_title)
            url.append(get_url)
            date.append(get_date)

        documentLst = [(title[i], date[i], docId[i], url[i]) for i in range(0, len(docId))]

        return render(request, 'document.html', {"documentLst": documentLst})

    except:
        return render(request, "document.html")


def upload(request):

    return render(request, "upload.html")


def postUpload(request):
    current_time = datetime.datetime.now()
    timestamp = current_time.timestamp()

    date = "{0}-{1}-{2}".format(current_time.month, current_time.day, current_time.year)
    title = request.POST.get('title')
    url = request.POST.get('url')

    try:
        data = {"title": title, "date": date, "url": url}
        database.child('archive').child('documents').child(str(int(timestamp))).set(data)
        return redirect(document)
    except:
        message = " Unable to upload file"
        return render(request, "upload.html", {"message": message})


def delete(request):
    docId = request.GET.get('docId')
    get_url = database.child("archive").child('documents').child(docId).child("url").get().val()

    try:
        # Delele data on Firebase database
        database.child("archive").child('documents').child(docId).remove()
        extractFilename = re.search('/o/(.*?)\?alt', get_url)
        storage.delete(extractFilename.group(1))
        return redirect(document)
    except:
        message = "Unable to delete file"
        return render(request, 'document.html', {"message": message})


# Post views
def post(request):
    get_postId = database.child("archive").child("posts").shallow().get().val()
    try:
        postId = []
        for i in get_postId:
            postId.append(i)

        postId.sort(reverse=True)

        date = []
        title = []
        content = []
        for i in postId:
            get_date = database.child("archive").child("posts").child(i).child("date").get().val()
            get_title = database.child("archive").child("posts").child(i).child("title").get().val()
            get_content = database.child("archive").child("posts").child(i).child("content").get().val()
            date.append(get_date)
            title.append(get_title)
            content.append(get_content)


        postLst = [(title[i], content[i], date[i], postId[i]) for i in range(0, len(postId))]

        return render(request, "post.html", {"postLst": postLst})

    except:
        return render(request, "post.html",)


def add(request):

    return render(request, "add.html")


def postAdd(request):
    current_time = datetime.datetime.now()
    timestamp = current_time.timestamp()

    date = current_time.strftime("%m/%d/%Y %H:%M:%S")

    title = request.POST.get('title')
    content = request.POST.get('content')

    try:
        data = {"title": title, "content": content, "date": date}
        database.child("archive").child("posts").child(str(int(timestamp))).set(data)
        return redirect(post)
    except:
        message = " Unable to add post"
        return render(request, "add.html", {"message": message})


def remove(request):
    postId = request.GET.get('postId')

    try:
        # Delele data on Firebase database
        database.child("archive").child("posts").child(postId).remove()
        return redirect(post)
    except:
        message = "Unable to delete post"
        return render(request, 'post.html', {"message": message})

# Event views
def agenda(request):
    get_date = database.child("events").shallow().get().val()
    try:
        eventId = []
        for i in get_date:
            eventId.append(i)

        eventId.sort(reverse=True)

        event = []
        date = []
        start_time = []
        end_time = []
        content = []

        for i in eventId:
            get_event = database.child("events").child(i).child("event").get().val()
            get_date = database.child("events").child(i).child("date").get().val()
            get_start_time = database.child("events").child(i).child("start_time").get().val()
            get_end_time = database.child("events").child(i).child("end_time").get().val()
            get_content = database.child("events").child(i).child("content").get().val()
            event.append(get_event)
            date.append(get_date)
            start_time.append(get_start_time)
            end_time.append(get_end_time)
            content.append(get_content)


        eventLst = [(event[i], date[i], start_time[i], end_time[i], content[i], eventId[i]) for i in range(0,
                                                                                                        len(eventId))]

        return render(request, 'agenda.html', {"eventLst": eventLst})

    except:

        return render(request, "agenda.html")

def create(request):

    return render(request, "create.html")

def postCreate(request):
    current_time = datetime.datetime.now()
    timestamp = current_time.timestamp()

    event = request.POST.get('event')
    content = request.POST.get('content')
    start_time = request.POST.get('start_time')
    end_time = request.POST.get('end_time')
    date = request.POST.get('date')

    try:
        data = {"date": date,"event": event,"start_time": start_time, "end_time": end_time, "content": content}
        database.child("events").child(str(int(timestamp))).set(data)
        return redirect(agenda)
    except:
        message = " Unable to create event"
        return render(request, "create.html", {"message": message})

def cancel(request):
    eventId = request.GET.get('eventId')

    try:
        # Delele data on Firebase database
        database.child("events").child(eventId).remove()
        return redirect(agenda)
    except:
        message = "Unable to delete event"
        return render(request, 'agenda.html', {"message": message})
