import tweepy
import datetime
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy import API
from tweepy.streaming import StreamListener
import twitter, time
from pathlib import Path
import json

def get_api(cfg):
'''Gets API Authentication'''
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

cfg = { 
    "consumer_key"        : "Insert Consumer Key here",
    "consumer_secret"     : "Insert Consumer Secret here",
    "access_token"        : "Insert Access Token here",
    "access_token_secret" : "Insert Access Token Secret here" 
    }

def Profile(atname):
'''Returns Dictionary with persons ID, screen name, and name(This is their @ name).'''
  personinfo = api.get_user(atname)
  person = {
            "id"            : personinfo.id,
            "screen name"   : personinfo.screen_name,
            "name"          : personinfo.name
            }
  return person

api = get_api(cfg)
newfollowers=[]
exfollowers=[]
listoffollowers=[]
followerlist = api.followers_ids()

def FollowerListEditor():
'''Opens and reads list of followers. Used to compare to new list of followers'''
    my_file = open("ListOfFollowers.txt","w")
    for i in followerlist:
        my_file.write(str(i)+'\n')

def FollowerChecker():
'''Checks to see if list of followers exists. If so, compares it to current list,
and updates list'''
    my_file = Path("C:\Users\gurma\Desktop\TwitterTicTacToe\ListOfFollowers.txt")
    if my_file.exists() == True:
        my_file = open("ListOfFollowers.txt","r")
        my_filelist = my_file.readlines()
        for i in followerlist:
            listoffollowers.append(str(i)+"\n")
            if str(i)+"\n" not in my_filelist:
                newfollowers.append(i)
        for i in my_filelist:
            if i not in listoffollowers:
                exfollowers.append(i)
        FollowerListEditor()
    else:
        FollowerListEditor()

def ResultsPrinter():
'''Prints out results based on who unfollowed or followed you'''
    print("People who followed you")
    for i in newfollowers:
      try:
        person = Profile(i)
        print(person['screen name'])
      except:
        print("ERROR: Person search failed : {}".format(i))
    print("---------------------------")
    print("People who unfollowed you")
    for i in exfollowers:
      try:
        person = Profile(i)
        print(person['screen name'])
      except:
        print("ERROR: Person search failed : {}".format(i))


def APIRateChecker():
'''Checks API rate limit to make sure you can check your followers list'''
    mainjson = json.dumps(api.rate_limit_status())
    mainjsons = json.loads(mainjson)
    return(str(mainjsons["resources"]["followers"]["/followers/ids"]['remaining']))
    


def main():
	'''Runs main program'''
    print("Twitter Follower Checker")
    if APIRateChecker() == '0':
        print("Rate Limit exceeded. Wait until it resets")
    else:
        print("You have " + APIRateChecker() + " tries remaining")
        FollowerChecker()
        ResultsPrinter()
    end = raw_input("Press ENTER to quit")
    

main()
