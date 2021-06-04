import functions as f
import os
import logo

def idToIdAndName(id):
  name = f.allUsersById[id]["fullName"]
  return f"{id}.{name}"

def userListToIdAndNameList(userList):
  return [idToIdAndName(user["id"]) for user in userList]

def idListToUserList(idList):
  return [f.allUsersById[id] for id in idList] 

def idListToIdAndNameList(idList):
  return [idToIdAndName(id) for id in idList]

def printUser(user):
  print("----USER INFORMATION----")
  print(f"ID          : {user['id']}")
  print(f"Name        : {user['fullName']}")
  print(f"Age         : {user['age']}")
  print(f"Study Year  : {user['studyYear']}")
  print(f"Study Field : {user['studyField']}")
  print(f"Residence   : {user['residence']}")
  print(f"Interests   : {' '.join([f.ALL_INTERESTS[i] for i in user['interests']])}")
  print(f"Followers   : {' '.join(idListToIdAndNameList(user['followers']))}")
  print(f"Following   : {' '.join(idListToIdAndNameList(user['following']))}")

def printAllUsersByName():
  print("----ALL USERS ORDERED BY NAME----")
  for letter, userList in f.allUsersDict.items():
    idsAndNames = ', '.join(userListToIdAndNameList(userList))

    print(f"{letter}) {idsAndNames}")

def printAllUsersById():
  print("----ALL USERS ORDERED BY ID----")
  for userString in userListToIdAndNameList(f.allUsersById.values()):
    print(userString)

def printUserFollowers(id):
  user = f.allUsersById[id]
  followers = user["followers"]
  print(f"{user['fullName']} is followed by {len(followers)} user{'s' if len(followers) != 1 else ''}:")

  for idName in idListToIdAndNameList(followers):
    print(f"  {idName}")

def clearAndLogo():
  clearConsole()
  logo.printLogo()

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)