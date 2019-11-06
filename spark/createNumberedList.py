import string
import sys

#Crea una lista cambiando los numeros por sus consecutivos

if (len(sys.argv) < 3):
  print("Arguments missing. Use: python3 createNumberedList.py numberString numberOfElements")
  exit()

string = sys.argv[1]
num = sys.argv[2]

firstNum = ""
beginNum = False
posIni = -1
posFin = -1
i=0
for char in string:
  if char.isdigit():
    if beginNum == False:
      beginNum = True
      posIni = i
    firstNum += char
  elif beginNum == True:
    posFin = i
    break
  i = i + 1

if posIni == -1:
  print("No number found in the string.")
  exit()
  
firstPart = string[0:posIni]
print(posFin)
if posFin == -1: #El numero está al final
  lastPart = ""
else:
  lastPart = string[posFin:]

firstNumInt = int(firstNum)


stringFinal = ""
for i in range (firstNumInt , firstNumInt + int(num)):
  if stringFinal != "":
    stringFinal = stringFinal + ", "
  stringFinal = stringFinal + firstPart + str(i) + lastPart

print(stringFinal)