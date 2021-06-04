import functions as f
import interface as it

def menu_main():
  it.clearAndLogo()
  print(
  "Welcome to the Snapch-UTT!\n"
  "Please choose the function you want to execute:\n"
  "1 - Connect to an existent account\n" # change infos, follow someone, diplay followers, delete the account
  "2 - Search engine\n"  # filters: name, field, year, interests
  "3 - Create an account  \n" 
  "4 - Exit "
  )

  correct_choice = False
  while not correct_choice:
    correct_choice = True
    choice = input("Function: ")
    if choice == '1':
      menu_connect()
    elif choice == '2':
      menu_search()
    elif choice == '3':
      menu_new_user()
    else:
      correct_choice = False
      print("ERROR: Invalid choice")

def menu_show_user_list(userIds, prompt = "List of users: "):
  it.clearAndLogo()
  print(prompt)
  for line in it.idListToIdAndNameList(userIds):
    print("  ", line)

  choice = input("Enter 'x' to view users in detail, leave blank to continue: ")

  if choice == "x":
    it.clearAndLogo()
    print(prompt)
    for user in it.idListToUserList(userIds):
      it.printUser(user)
      print()
    input("Press any key to continue")

def menu_new_user():
  it.clearAndLogo()
  print("----CREATE A NEW USER PROFILE----")
  fullName   =     input("Full Name   : ").title()
  age        = int(input("Age         : "))
  studyYear  = int(input("Study Year  : "))
  studyField =     input("Study Field : ").title()
  residence  =     input("Residence   : ")

  print("  Possible interests: ")
  for i, interest in enumerate(f.ALL_INTERESTS):
    print(f"    {i+1}. {interest} ")

  interestsString = input("List of interests(by index): ")

  interestsSet = set()
  for i in interestsString.split(" "):
    if(f.hasNumbers(i)):
      # The interests are stored in an array with the index starting from 0, whereas the user inputs them with an index starting a 1.
      interestsSet.add(int(i)-1)
  
  return f.addNewUser(fullName, age, studyYear, studyField, residence, interestsSet)



def menu_search():
  it.clearAndLogo()
  print("----USER SEARCH----")
  print("Fields can be left blank: ")
  
  name = input("Input the name of the user: ")
  if (name == ""): name = None

  yearString = input("Input the study year of the user: ")
  if (yearString == ""): 
    year = None
  else:
    year = int(yearString)

  field = input("Input the study field of the user: ")
  if (field == ""): field = None

  print("  Possible interests: ")
  for i, interest in enumerate(f.ALL_INTERESTS):
    print(f"    {i+1}. {interest} ")

  interestsString = input("Input all of your interests:")
  if (name == ""): name = None

  interestsSet = set()
  for i in interestsString.split(" "):
    if(f.hasNumbers(i)):
      # The interests are stored in an array with the index starting from 0, whereas the user inputs them with an index starting a 1.
      interestsSet.add(int(i)-1)

  results = f.searchUsers(name, year, field, interestsSet)
  menu_show_user_list(results, "Search results: ")

def menu_connect():
  it.clearAndLogo()
  print("----USER CONNECT----")
  id = int(input("Enter your accound account ID: "))

  while not f.accountExists(id):
    id = int(input("ERROR: User does not exist: "))

  while True:
    it.clearAndLogo()
    print("Hello {} (user id: {})".format(f.allUsersById[id]["fullName"], id))
    print()
    print("----ACCOUNT FUNCTIONS----")
    print(
      "1 - View account information\n"
      "2 - Modify user informations\n"
      "3 - Follow a user\n"
      "4 - Unfollow a user\n"
      "5 - Display all followers\n"
      "6 - Find suggested users\n"
      "7 - Delete your account\n"
      "8 - Log out"
      )

    correct_choice = False
    while not correct_choice:
      correct_choice = True
      choice = int(input("Function: "))
      if choice == 1:
        menu_user_information(id)
      elif choice == 2:
        menu_update_user(id)
      elif choice == 3:
        menu_follow_user(id)
      elif choice == 4:
        menu_unfollow_user(id)
      elif choice == 5:
        menu_display_followers(id)
      elif choice == 6:
        return
      else:
        correct_choice = False
        print("ERROR: Invalid selection")


def menu_user_information(userId):
  it.clearAndLogo()
  it.printUser(f.allUsersById[userId])
  print()
  input("Press any key to continue")    

def menu_update_user(userId):
  it.clearAndLogo()
  user = f.allUsersById[userId]

  oldFullName     = user["fullName"]
  oldAge          = user["age"]
  oldStudyYear    = user["studyYear"]
  oldStudyField   = user["studyField"]
  oldResidence    = user["residence"]
  oldInterestsSet = user["interests"]

  print("----UPDATE USER PROFILE----")
  newFullName        = input(f"Full Name ({oldFullName}): ").title()
  newAgeString       = input(f"Age ({oldAge}): ")
  newStudyYear       = input(f"Study Year ({oldStudyYear}): ")
  newStudyField      = input(f"Study Field ({oldStudyField}): ")
  newResidence       = input(f"Residence ({oldResidence}): ")

  print("  Possible interests: ")
  for i, interest in enumerate(f.ALL_INTERESTS):
    print(f"    {i+1}. {interest} ")

  interestsString = input(f"Interests ({' '.join([str(i+1) for i in oldInterestsSet])}): ")

  newInterestsSet = set()
  for i in interestsString.split(" "):
    if(f.hasNumbers(i)):
      # The interests are stored in an array with the index starting from 0, whereas the user inputs them with an index starting a 1.
      newInterestsSet.add(int(i)-1)

  isFirstLetterDifferent = False
  if newFullName != "":
    # If the first letter of user's name changes, we need to update it in the allUsersDict. We first remove the user from the dictionary before changing the name, then later we will re-add it with the new name.
    
    if newFullName[0] != oldFullName[0]:
      isFirstLetterDifferent = True
      f.removeUserFromAllUsersDict(user)
      

  user["fullName"]   =     f.sameIfEmptyString(oldFullName, newFullName)
  user["age"]        = int(f.sameIfEmptyString(str(oldAge), newAgeString))
  user["studyYear"]  = int(f.sameIfEmptyString(str(oldStudyYear), newStudyYear))
  user["studyField"] =     f.sameIfEmptyString(oldStudyField, newStudyField)
  user["residence"]  =     f.sameIfEmptyString(oldResidence, newResidence)
  
  if len(newInterestsSet) != 0:
    user["interests"] = newInterestsSet

  if isFirstLetterDifferent:
    f.addUserToAllUsers(user)

def menu_follow_user(followerId):
  it.clearAndLogo()
  print("----USER FOLLOW----")
  
  while True:
    choice = int(input("User id(-1 to quit): "))

    if choice == -1: return
    if choice == followerId:
      print("Can't follow yourself")
      continue

    if f.addFollow(followerId, choice):
      print("You are now following {}".format(it.idToIdAndName(choice)))
    else:
      print("Couldn't follow user")

def menu_unfollow_user(userId):
  it.clearAndLogo()
  print("----USER UNFOLLOW----")
  
  while True:
    choice = int(input("User id(-1 to quit): "))

    if choice == -1: return
    if choice == userId:
      print("Can't unfollow yourself")
      continue

    if f.removeFollow(userId, choice):
      print("You are no longer following {}".format(it.idToIdAndName(choice)))
    else:
      print("Couldn't unfollow user")

def menu_display_followers(userId):
  it.clearAndLogo()
  followers = f.allUsersById[userId]["followers"]
  menu_show_user_list(followers, "You have {} followers".format(len(followers)))

f.createTestUsers()

while menu_main(): pass