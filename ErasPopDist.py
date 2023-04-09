import random 
import math
import pandas

def updateRowWithLatestGroupPopulations(popDist, row):
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

  row['pop0To12'] = pop0To12
  row['pop12To24'] = pop12To24
  row['pop24To36'] = pop24To36
  row['pop36To48'] = pop36To48
  row['pop48To60'] = pop48To60
  row['pop60To72'] = pop60To72
  row['pop72plus'] = pop72plus
  row['totalPop'] = totalPop 
  return row

def seed():
  #triangle curve distribution
  #popDist = [(i,random.randint(0,i/3)) for i in range(1,42)] + [(i,random.randint(0, max((84-(2*i))/3,1)))for i in range(42,84)]
  #pencil distribution
  popDist = [(i,random.randint(0,10)) for i in range(1,42)] + [(i,random.randint(0, max((84-(2*i))/3,1)))for i in range(42,84)]
  row = {}
  row['year'] = 0
  row['deathsNat'] = 0
  row['deathsWar'] = 0
  row['births'] = 0
  row['conquestAdd'] = 0
  return popDist, updateRowWithLatestGroupPopulations(popDist, row)

# def conquest():
#   global popDist, deathsWar, conquestAdd

#   combatPopRate = 0.25
#   combatPopSurvivalRate = 0.99
#   totalCombatPop = 0
#   popDist2 = []
#   for (age,count) in popDist: 
#     if(age >= 18 and age <= 60):
#       combatReady = int(round(count * combatPopRate))
#       remainers = count - combatReady
#       combatSurvivors = int(round(combatReady * combatPopSurvivalRate))
#       deathsWar = deathsWar + combatReady - combatSurvivors
#       totalCombatPop = totalCombatPop + combatSurvivors
#       totalSurvivors = combatSurvivors+remainers
#       popDist2 = popDist2 + [(age,totalSurvivors)]

#   popDist3 = []
#   conquestRate = .01
#   for (age,count) in popDist2: 
#     if(age <= 36):
#       conquestCount = int(round(conquestRate * totalCombatPop))
#       conquestAdd = conquestAdd + conquestCount
#       popDist3 = popDist3 + [(age,count+conquestCount)]
#  popDist = popDist3

#def war ():
#def plague():

#def rebellion():


def increaseAges(popDist):
  popDist2 = []
  for (age,count) in popDist: 
    popDist2 = popDist2 + [(age+1,count)]
  popDist = popDist2
  return popDist

def addBabies(popDist, row, booster = 1):
  fertile = 0
  birthRate = (random.randint(10,20)/100.0) * booster
  for (age,count) in popDist: 
    if(age >= 18 and age <= 40):
      fertile = fertile + count
  row['births'] = int(round(fertile*birthRate))
  popDist = popDist + [(1,row['births'])]
  return popDist, row


def removeDeaths(popDist, row):
  deathsNat = 0
  popDist2 = []
  childSurvival = random.randint(80,90)/100.0
  adultSurvival = random.randint(95,100)/100.0
  elderSurvival = random.randint(25,30)/100.0
  for (age,count) in popDist: 
    if age < 12:
      childrenSurvived = int(round(count*childSurvival))
      childrenDied = count - childrenSurvived
      popDist2 = popDist2 + [(age,childrenSurvived)]
      deathsNat = deathsNat + childrenDied
    elif age >= 12 and age < 72:
      adultsSurvived = int(round(count*(adultSurvival)))
      adultsDied = count - adultsSurvived
      popDist2 = popDist2 + [(age, adultsSurvived)]
      deathsNat = deathsNat + adultsDied
    else:
      eldersSurvived = int(round(count*(elderSurvival)))
      eldersDied = count - eldersSurvived
      popDist2 = popDist2 + [(age, eldersSurvived)]
      deathsNat = deathsNat + eldersDied
  row['deathsNat'] = deathsNat
  popDist = popDist2
  return popDist, row

def addYear(year, popDist, row, conquestYear = False):
  row['year'] = year
  popDist = increaseAges(popDist)
  popDist, row = addBabies(popDist, row, booster = 2)
  popDist, row = removeDeaths(popDist, row)
  if (conquestYear) :
    conquest()
  row = updateRowWithLatestGroupPopulations(popDist, row)
  return popDist, row

def addRowToTable(table, row):
  table.append([
      row['year'], 
      row['pop0To12'], 
      row['pop12To24'], 
      row['pop24To36'], 
      row['pop36To48'], 
      row['pop48To60'], 
      row['pop60To72'], 
      row['pop72plus'], 
      row['totalPop'], 
      row['births'], 
      row['deathsNat']
    ])

def print_table(table):
  pandas.set_option('display.max_columns',None)
  pandas.set_option('display.max_rows',None)
  pandas.set_option('display.width',0)
  df = pandas.DataFrame(
    table, 
    columns = 
      ['year','pop0To12','pop12To24','pop24To36','pop36To48','pop48To60','pop60To72','pop72plus','totalPop','births','deathsNat']
    )
  print(df)


if __name__ == '__main__':
  popDist, row = seed()
  table = []
  addRowToTable(table, row)
  for i in range(1,500) :
    row = {}
    popDist, row = addYear(i, popDist, row, conquestYear = False)
    addRowToTable(table, row)
  print_table(table)