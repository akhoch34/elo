import nfldb
from nflgame import teams
import math
import operator

db = nfldb.connect()

FIRSTYEAR = 2009 #Database starts at the year 2009
CURRENTYEAR = nfldb.now().year #get Current Year
ELORATINGS = {}
HOMEFIELDADV = 63 #determined Home Field is worth 2.5 points or about 63 elo rating points


def calcK(mov = 1, eloDiff = 1):
    #mov = Margin of Victory
    movMultiplier = math.log(1+mov) * (2.2/(eloDiff*.001+2.2))
    return 20 * movMultiplier

def updateElo(currentGame):
    #Calculate Elo Differential between Home and Away Teams
    eloDiffHome = ((ELORATINGS[currentGame.home_team] + HOMEFIELDADV) - ELORATINGS[currentGame.away_team])
    #Calculate Probability of Win for Home and Away Teams
    pOfWinHome= 1/(1+(math.pow(10, (-1 * eloDiffHome/400))))
    pOfWinAway = 1-pOfWinHome
    #Calculate Margin of Victory and K Value
    margin = abs(currentGame.home_score-currentGame.away_score)
    #Determine if home or away team won
    if g.loser == currentGame.away_team:
        loserAway = True
        kEloDiff = (ELORATINGS[currentGame.home_team] + HOMEFIELDADV) - ELORATINGS[currentGame.away_team]
    else:
        loserAway = False
        kEloDiff = ELORATINGS[currentGame.away_team] - (ELORATINGS[currentGame.home_team] + HOMEFIELDADV)
    kValue = calcK(margin, kEloDiff)
    #Calculate the new elo calue to be used in calculating updated elo score
    if loserAway:
        eloFactor = kValue * pOfWinAway
        ELORATINGS[currentGame.home_team] += eloFactor
        ELORATINGS[currentGame.away_team] -= eloFactor
    else:
        eloFactor = kValue * pOfWinHome
        ELORATINGS[currentGame.home_team] -= eloFactor
        ELORATINGS[currentGame.away_team] += eloFactor



for team in teams:  #initialize ELO Ratings Dictionary at 1505 for every team starting in 2009
    if team[0] not in ELORATINGS:
        ELORATINGS[team[0]] = 1505

#Start Regular Season Query
q = nfldb.Query(db)
q.game(season_year=2015, season_type='Regular')
games = sorted(q.as_games(), key=lambda g: g.gamekey)
for g in games:
    updateElo(g)

sorted_elo = sorted(ELORATINGS.items(), key=operator.itemgetter(1), reverse= True) #Sort Elo by Value
print sorted_elo

#Start Postseason Query
postQ = nfldb.Query(db)
postQ.game(season_year=2015, season_type='Postseason')
postSeason = sorted(postQ.as_games(), key=lambda g: g.gamekey)
for g in postSeason:
    updateElo(g)

sorted_elo = sorted(ELORATINGS.items(), key=operator.itemgetter(1), reverse= True) #Sort Elo by Value
print sorted_elo






