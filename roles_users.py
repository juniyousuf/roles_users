import sys


"""
Create a Role class to set up roles

In the initial loading of roles users will be None for each role

Children are sub-roles of a role that are populated as sub-roles
are initialized.
"""

class Role:

  def __init__(self, name, parent):
    self.name=name
    self.parent=parent
    self.children=set()
    self.users=set()

  
  def __str__(self):
    str='"Name": "%s", "Parent": %s, "children": %s, "Users": %s' % (self.name, self.parent, repr(self.children), repr(self.users))
    return str


"""
Create a User class to set up Users

As users are initialized their ids are added to the roles.users
variable
"""

class User:

  def __init__(self, name, role):
    self.name=name
    self.role=role


  def __str__(self):
    str = '"Name": "%s", "Role": %s' % (self.name, self.role)
    return str


"""
Below function initializes roles.

As part of solution it'll throw error if:
 - (Input) Roles are None/Empty
 - Duplicate role id is found
 - Parent role doesn't exist that means if a parent role
 is even later in the list it'll throw an exception
 
It returns a dictionary with key as role id and value as
object of class Role


- If role parent id is 0 it's Admin role with no parent
- If parent exist of a role, id of it is added to
role.children set
"""
def setRoles(roles):
  if(len(roles) < 1):
    raise Exception("There should be at least one role")
  else:
    roles_dict = dict()
    children = set()
    for role in roles:
      if role["Id"] in roles_dict:
        raise Exception("Duplicate roles IDs. Ids should be unique")
      else:
        if (role["Parent"]!=0) and (role["Parent"] not in roles_dict):
          raise Exception("Parent roles doesn't exist. Can't create an orphan.")
        if (role["Parent"]!=0):
          roles_dict[role["Parent"]].children.add(role["Id"])
        role_obj = Role(role["Name"], role["Parent"])
        roles_dict[role["Id"]] = role_obj
  return roles_dict


"""
Below mentioned function initializes users.

As part of solution it'll throw error if:
 - (Input) Users are None/Empty
 - Duplicate user id is found
 - Role that's being setup for user doesn't exist

It returns a dictionary with key as user id and value as
object of class User and sets up user id in roles dictionary in
roles.children
"""
def setUsers(users, roles):
  if(len(users) < 1):
    raise Exception("There should be at least one user")
  else:
    users_dict = dict()
    for user in users:
      if user["Id"] in users_dict:
        raise Exception("User ID already taken. Put another ID for this user.")
      elif user["Role"] not in roles:
        raise Exception("Unknown role for user. Choose an existing role for user")
      users_dict[user["Id"]]=User(user["Name"], user["Role"])
      roles[user["Role"]].users.add(user["Id"])
    return users_dict

"""
Final function to be called for printing all
sub users.

It iterate through all the sub-roles and gets 
users' id of each role and get user info from 
users set and stringify it and adds it to a set.
At the end converts the set to a string with ','
as delimiter and returns a string
"""
def getUsersViaRoles(sub_roles, users, roles):
  ret_str=""
  ret_set = set()
  for sub_role_id in sub_roles:
    for user_id in roles[sub_role_id].users:
      ret_set.add('{"Id": %s, %s}' % (user_id, users[user_id]))
  ret_str = (','.join(str(e) for e in ret_set))
  return ret_str;

"""
Get all the sub-roles of a role recursively.
It adds all the roles to a set and returns the 
set when it reaches a bottom level role
"""
def getSubRoles(role_id, sub_roles, roles):
  if(len(roles[role_id].children)==0):
    return sub_roles
  else:
    for child_role in roles[role_id].children:
      sub_roles.add(child_role)
      getSubRoles(child_role, sub_roles, roles)
  return sub_roles

"""
Orchestrator function that first gets sub-roles
set via getSubRoles then get all user from that
via getUsersViaRoles and prints the result
"""
def getSubordinates(user_id, users, roles):
  if(user_id not in users):
    raise Exception("User doesn't exist")
  elif (len(roles[users[user_id].role].children)==0):
    print("No subordinates found")
  else:
    sub_roles = getSubRoles(users[user_id].role, set(), roles)
    print(getUsersViaRoles(sub_roles, users, roles))


def main(user_id):
  roles = [
    {
      "Id": 1,
      "Name": "System Administrator",
      "Parent": 0
    },
    {
      "Id": 2,
      "Name": "Location Manager",
      "Parent": 1,
    },
    {
      "Id": 3,
      "Name": "Supervisor",
      "Parent": 2,
    },
    {
      "Id": 4,
      "Name": "Employee",
      "Parent": 3,
    },
    {
      "Id": 5,
      "Name": "Trainer",
      "Parent": 3,
   }
  ]
  
  users = [
    {
      "Id": 1,
      "Name": "Adam Admin",
      "Role": 1
    },
    {
      "Id": 2,
      "Name": "Emily Employee",
      "Role": 4
    },
    {
      "Id": 3,
      "Name": "Sam Supervisor",
      "Role": 3
    },
    {
      "Id": 4,
      "Name": "Mary Manager",
      "Role": 2
    },
    {
      "Id": 5,
      "Name": "Steve Trainer",
      "Role": 5
    }
  ]

# Set up roles from the input provided above 
  roles_dict = setRoles(roles)
# Set up user from the input provided above
  users_dict = setUsers(users, roles_dict)
# Get all subordinates of a user
  getSubordinates(user_id, users_dict, roles_dict)


if __name__== "__main__":
  if(len(sys.argv) < 2):
    raise Exception("This code takes one argument i.e. the user id")
  main(int(sys.argv[1]))
