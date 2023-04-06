import random 
import math

# global row format 
# 0   , 1  , 2   , 3   , 4   , 5   , 6   , 7 , 8   , 9     , 10,        , 11              , 12
# year,0-12,12-24,24-36,36-48,48-60,60-72,72+,total, births, deaths(nat), deaths(conflict), conquestAdd

def modifyGroups():
  global totalPop, pop0To12, pop12To24, pop24To36 , pop36To48, pop48To60, pop60To72, pop72plus
  totalPop = 0
  pop0To12 = 0
  pop12To24 = 0
  pop24To36 = 0
  pop36To48 = 0
  pop48To60 = 0
  pop60To72 = 0
  pop72plus = 0
  for (age,count) in popDist: 
    if (age > 0 and age < 12) : 
      pop0To12 = int(round(pop0To12 + count))
      totalPop = totalPop + count
    elif (age >= 12 and age < 24) : 
      pop12To24 = int(round(pop12To24 + count))
      totalPop = totalPop + count
    elif (age >= 24 and age < 36) : 
      pop24To36 = int(round(pop24To36 + count))
      totalPop = totalPop + count
    elif (age >= 36 and age < 48) : 
      pop36To48 = int(round(pop36To48 + count))
      totalPop = totalPop + count
    elif (age >= 48 and age < 60) : 
      pop48To60 = int(round(pop48To60 + count))
      totalPop = totalPop + count
    elif (age >= 60 and age < 72) : 
      pop60To72 = int(round(pop60To72 + count))
      totalPop = totalPop + count
    elif (age >= 72) : 
      pop72plus = int(round(pop72plus + count))
      totalPop = totalPop + count

def seed():
  global popDist, year, births, deathsNat, deathsWar, conquestAdd
  year = 0
  deathsNat = 0
  deathsWar = 0
  births = 0
  conquestAdd = 0
  #triangle curve distribution
  #popDist = [(i,random.randint(0,i/3)) for i in range(1,42)] + [(i,random.randint(0, max((84-(2*i))/3,1)))for i in range(42,84)]
  #pencil distribution
  popDist = [(i,random.randint(0,10)) for i in range(1,42)] + [(i,random.randint(0, max((84-(2*i))/3,1)))for i in range(42,84)]
  modifyGroups()

def conquest():
  global popDist, deathsWar, conquestAdd

  combatPopRate = 0.25
  combatPopSurvivalRate = 0.99
  totalCombatPop = 0
  popDist2 = []
  for (age,count) in popDist: 
    if(age >= 18 and age <= 60):
      combatReady = int(round(count * combatPopRate))
      remainers = count - combatReady
      combatSurvivors = int(round(combatReady * combatPopSurvivalRate))
      deathsWar = deathsWar + combatReady - combatSurvivors
      totalCombatPop = totalCombatPop + combatSurvivors
      totalSurvivors = combatSurvivors+remainers
      popDist2 = popDist2 + [(age,totalSurvivors)]

  popDist3 = []
  conquestRate = .01
  for (age,count) in popDist2: 
    if(age <= 36):
      conquestCount = int(round(conquestRate * totalCombatPop))
      conquestAdd = conquestAdd + conquestCount
      popDist3 = popDist3 + [(age,count+conquestCount)]
  popDist = popDist3

#def war ():
#def plague():

#def rebellion():


def addBabies(booster = 1):
  global popDist, births
  fertile = 0
  birthRate = (random.randint(10,20)/100.0) * booster
  for (age,count) in popDist: 
    if(age >= 18 and age <= 36):
      fertile = fertile + count
  births = round(fertile*birthRate)
  popDist = popDist + [(1,births)]

def increaseAges():
  global popDist
  popDist2 = []
  for (age,count) in popDist: 
    popDist2 = popDist2 + [(age+1,count)]
  popDist = popDist2

def removeDeaths():
  global popDist, deathsNat
  popDist2 = []
  childSurvival = random.randint(50,70)/100.0
  adultSurvival = random.randint(95,100)/100.0
  elderSurvival = random.randint(25,30)/100.0
  for (age,count) in popDist: 
    if age < 12:
      popDist2 = popDist2 + [(age,int(round(count*childSurvival)))]
      deathsNat = deathsNat + count - int(round(count*childSurvival))
    elif age >= 12 and age < 72:
      popDist2 = popDist2 + [(age,int(round(count*(adultSurvival))))]
      deathsNat = deathsNat + count - int(round(count*adultSurvival))
    else:
      popDist2 = popDist2 + [(age,int(round(count*(elderSurvival))))]
      deathsNat = deathsNat + count - int(round(count*elderSurvival))
  popDist = popDist2

def addYear(conquestYear = False):
  global year, births, deathsNat, deathsWar, conquestAdd
  births = 0
  deathsNat = 0
  deathsWar = 0
  conquestAdd = 0
  year = year + 1
  increaseAges()
  addBabies()
  removeDeaths()
  if (conquestYear) :
    conquest()
  modifyGroups()


def print_header():
  print("year   0-12     12-24     24-36    36-48    48-60     60-72      72+      total      births      deaths(nat)       deaths(conflict)      conquestAdd")

def print_dist():
  print("{}     {}       {}        {}        {}        {}        {}        {}        {}       {}          {}                {}        {}")\
  .format(year, pop0To12, pop12To24, pop24To36, pop36To48, pop48To60, pop60To72, pop72plus, totalPop, births, deathsNat, deathsWar, conquestAdd)

if __name__ == '__main__':
  print_header()
  seed()
  print_dist()
  for i in range(0,100) :
    addYear(conquestYear = True)
    print_dist()
