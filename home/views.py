
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import codecs
from django.core import management
from Feas.settings import db
import datetime


def index(request):

    email = request.session.get("email")
    print(email)
    tweets_check = db.tweet.find_one({"email": email})
    print(tweets_check)
    user_tweets = list()
    posted_on = list()
    context = {}
    is_tweet = False
    print(tweets_check)
    if tweets_check is not None:
        print("tweet present")
        tweets_query = db.tweet.find({"email": email})
        tweets = list()
        for tweet in tweets_query:
            temp_tweet = dict()
            temp_tweet["tweet"] = tweet["tweet"]
            temp_tweet["posted_on"] = tweet["datetime"]
            tweets.append(temp_tweet)
        is_tweet = True
        print(tweets)
        context = {"tweets": tweets, "is_tweet": is_tweet}
        return render(request, 'home/index.html', context)

    else:
        print("tweet not present")
        context = {
            "is_tweet": is_tweet
        }
        return render(request, 'home/index.html', context)


def tweet(request):
    if request.method == "POST":
        tweet = request.POST.get("tweet")
        email = request.session['email']
        if len(tweet) < 81 and len(tweet) > 5:
            data = {
                'tweet': tweet,
                'email': email,
                'datetime': datetime.datetime.utcnow()
                }
            db.tweet.insert_one(data)
        return redirect('/home')


@csrf_exempt
def search(request):
    if request.method == "POST":

        user_email = request.session['email']
        name = request.POST.get("username")
        query_search_user = db.user.find({"username": {'$regex': ".*"+name+".*"}})
        query_is_following = db.user.find_one({"email": user_email})

        query_search_user_count = query_search_user.count()

        search_result = list()

        if query_search_user_count > 0:
            print("user exists")
            for user in query_search_user:
                following = dict()
                following["username"] = user["username"]
                if user['username'] not in query_is_following["following"]:
                    following["is_following"] = False
                if user['username'] in query_is_following["following"]:
                    following["is_following"] = True
                search_result.append(following)
        context = {"search_result": search_result}
        return render(request, 'home/search.html', context)

@csrf_exempt
def follow(request):
        if request.method == "POST":
            user_email = request.session['email']
            username = request.POST.get("username")
            follow_status = request.POST.get("follow_status")

            query_is_following = db.user.find_one({"email": user_email})
            following = query_is_following["following"]
            print(following)
            if username not in query_is_following["following"] and follow_status == "not_following":
                following.append(username)
                db.user.update_one(
                    {"email": user_email},
                    {"$set": {"following": following}}
                    )

            if username in query_is_following["following"] and follow_status == "following":
                following.remove(username)
                db.user.update_one(
                    {"email": user_email},
                    {"$set": {"following": following}}
                    )


            return HttpResponse(follow_status)
