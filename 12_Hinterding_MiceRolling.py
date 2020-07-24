"""
In this program I want to simulate a simple game which already exists in real life.
In this game you usally have two pig figurines which you throw and depending on the way they land you get points.
After each throw one can decide if to throw again or to pass, as long as the previous throw wasn't the one throw which let's you lose the game.
Because I wasn't able to make pigs in ascii code, there will the mice instead.
The possible throws for one mice are:
looking left, looking right, laying on its back (laying), only showing the bum (bum), sitting and showing the face upfront (face).
The rules are as follows:
You always lose all your gathered points if one mouse is looking left while the other one is looking right, as well as the other way around.
When both mice are doing the same your points are being doubled, except both are looking in the same direction, which just gives you no additional points.
In all the other cases the points of the mice are looked at and added individually as follows:

    looking left= 0 points
 _  _
(o)(o)--.
 \../ (  )____/
 m\/m--m


    looking right = 0 points
        _  _
    .--(o)(o)
\___(  )\../
     m--m\/m


    laying = 5 points
 ____  w--w/\w
/    (  ) /°°\
      `--(o)(o)
          ?  ?


    bum = 5 points
  q-p
 /   \
(     )
 `-(-'
    )


    face = 10 points
  q-p
 /\"/\
(`=*=')
 ^---^`-._


This game is some kind of a simple gamble game and the goal is to get as most points as possible.
"""

from numpy.random import choice

'''
the following lines are ascii pictures of mice
'''

LookingLeft = '\n  _  _\n (o)(o)--.\n  \../ (  )____/\n  m\/m--m`\n'
LookingRight = '\n         _  _\n     .--(o)(o)\n \___(  )\../\n      m--m\/m\n'
Laying = '\n  ____  w--w/\w\n /    (  ) /°°\ \n       `--(o)(o) \n           ꜚ  ꜚ\n'
Bum = '\n   q-p\n  /   \ \n (     ) \n  `-(-´\n     )\n'
Face = '\n   q-p \n  /\\"/\ \n (`=*=´) \n  ^---^`-._ \n'

elements = [LookingLeft, LookingRight, Laying, Bum, Face]  # this are the possible throws
weights = [3 / 10, 3 / 10, 3 / 20, 3 / 20, 1 / 10]  # this are the probabilities for each possible throw


Direction = {LookingLeft,
             LookingRight}  # here I put looking left and looking right together, as they both give 0 points

FivePoints = {Laying, Bum}  # here I put laying and bum together, as they both give 5 points


'''
The following function is the heart of the program, as it simulates what happens when the player throws once and 
gives back the points.
'''


def checking(Previous_Points):
    points = 0
    fail = 0
    roll1 = choice(elements, p=weights)  # here it simply makes two possible throws depending on the probabilities
    roll2 = choice(elements, p=weights)
    print(
        'You rolled ' + roll1 + ' and ' + roll2)  # the player should see the mice as it gives a nice optical feedback and gives some feeling of a board game
    if roll1 == roll2 and roll1 in Direction:  # in this case there will be no additional points, according to the rules
        print('That gives you no points.')
        points = 0  # the points variable says how many points will be added to the players points
        fail += 0  # the fail variable will be 0 in every case except when both mice are looking in opposite directions

    elif roll1 == roll2 and roll1 not in Direction:  # in this case both mice are doing the same while not looking left or right, so the points are being doubled
        print('Your points are getting doubled!')
        points += Previous_Points
        fail += 0

    elif (roll1 in Direction and roll2 == Face) or (
            roll2 in Direction and roll1 == Face):  # in this case only the 'face' mouse counts so it's worth 10 points
        print('You get additional 10 points!')
        points += 10
        fail += 0

    elif roll1 in FivePoints and roll2 in FivePoints:  # in this case both mice give independently 5 points, which sums up to 10 points
        print('You get additional 10 points!')
        points += 10
        fail += 0

    elif (roll1 in Direction and roll2 in FivePoints) or (
            roll2 in Direction and roll1 in FivePoints):  # here only the mouse giving 5 points counts to it's 5 additional points
        print('You get additional 5 points!')
        points += 5
        fail += 0

    elif (roll1 in FivePoints and roll2 == Face) or (
            roll2 in FivePoints and roll1 == Face):  # here the points simply sum up to 15 (= 5 + 10)
        print('You get additional 15 points!')
        points += 15
        fail += 0

    elif roll1 in Direction and roll2 in Direction:  # the mice can't look in the same direction as that case has been checked before, so the player loses
        points += -Previous_Points  # the program simply subtracts all the points the player gathered so far
        fail += 1  # here are the mice looking in opposite directions so the player loses

    return points, fail  # the function returns how many points the player got and if the player failed


'''
This part of the program is the environment for the function above.
It contains the 'mask' that the user will see and interact with.
'''
print('Do you want to play mice rolling?')
answer = input()
while answer != 'yes' and answer != 'no':  # I want the user to not just write garbage
    print('Please say yes or no')
    answer = input()
if answer == 'yes':
    user_points = 0  # at first the player obviously got no points
    fail = 0  # the player obviously hasn't lost yet
    rolling = checking(user_points)  # the function checking is being run
    user_points += rolling[0]  # the gained points are being added to the player points
    end = rolling[1]  # this line is to check later if the player has lost
    spawnkill = 0  # it is possible to throw 0 points in the first round. Of course that doesn't mean that the player lost so this line is to make sure that the player isn't being spawnkilled out of bad luck
    if end == 1:  # if the player lost the game is over
        print('You just lost the game mate.')
        spawnkill = 1
    else:
        print('You now have ' + str(user_points) + ' points.')  # the player has to know how many points he now got
        print('Do you want to roll again?')
    decision = input()
    while decision != 'no' and end != 1:  # the player can really play as long as he doesn't lose, so theoretically he could play forever
        previous_points = user_points
        rolling = checking(user_points)
        user_points += rolling[0]
        end = rolling[1]
        if end != 1:  # the game continues as long as the player doesn't lose
            print('You now have ' + str(user_points) + ' points.')
            print('Do you want to roll again?')
            decision = input()

    if user_points == 0 and spawnkill != 1:  # this is to check if the player legitimately lost in the first round
        print('You just lost the game mate.')
    elif spawnkill == 0:  # when the player wants to end he gets said how many points he gathered
        print('Alright, you got ' + str(user_points) + ' points, congratulations!')

elif answer == 'no':
    print('Sorry to hear that, maybe you will change your mind later.')

