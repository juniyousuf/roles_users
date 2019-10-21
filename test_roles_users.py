import unittest
from roles_users import setRoles
from roles_users import setUsers
from roles_users import getSubordinates

class RolesUsersTest(unittest.TestCase):
    def testValidRole(self):
      roles = [
        {
            "Id": 1,
            "Name": "System Administrator",
            "Parent": 0
        }
      ]
      roles_dict = setRoles(roles)
      self.assertEqual(roles_dict[1].name, "System Administrator")
      self.assertEqual(roles_dict[1].parent, 0)
      self.assertEqual(roles_dict[1].children, set())
      self.assertEqual(roles_dict[1].users, set())


    def testValidRoleChildren(self):
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
          "Name": "Area Manager",
          "Parent": 1,
        }
      ]
      roles_dict = setRoles(roles)
      self.assertEqual(roles_dict[1].name, "System Administrator")
      self.assertEqual(roles_dict[1].parent, 0)
      self.assertEqual(roles_dict[1].children, {2, 3})
      self.assertEqual(roles_dict[1].users, set())
  

    def testDuplicateRoleIds(self):
      roles = [
        {
          "Id": 1,
          "Name": "System Administrator",
          "Parent": 0
        },
        {
          "Id": 1,
          "Name": "CEO",
          "Parent": 0,
        }
      ]
      with self.assertRaises(Exception):
        setRoles(roles)

 
    def testParentRoleAfterSubRole(self):
      roles = [
        {
          "Id": 2,
          "Name": "Location Manager",
          "Parent": 1
        },
        {
          "Id": 1,
          "Name": "System Administrator",
          "Parent": 0,
        }
      ]
      with self.assertRaises(Exception):
        setRoles(roles)


    def testParentRoleNotExist(self):
      roles = [
        {
          "Id": 2,
          "Name": "Location Manager",
          "Parent": 1
        },
      ]
      with self.assertRaises(Exception):
        setRoles(roles)
    

    def testValidRoleAndUser(self):
      roles = [
        {
            "Id": 1,
            "Name": "System Administrator",
            "Parent": 0
        }
      ]
      users = [
        {
          "Id": 1,
          "Name": "Adam Admin",
          "Role": 1
        }
      ]
      roles_dict = setRoles(roles)
      user_dict = setUsers(users, roles_dict)
      self.assertEqual(roles_dict[1].name, "System Administrator")
      self.assertEqual(roles_dict[1].parent, 0)
      self.assertEqual(roles_dict[1].children, set())
      self.assertEqual(roles_dict[1].users, {1})
      
      self.assertEqual(user_dict[1].name, "Adam Admin")
      self.assertEqual(user_dict[1].role, 1)


    def testInvalidUser(self):
      roles = [
        {
            "Id": 1,
            "Name": "System Administrator",
            "Parent": 0
        }
      ]
      roles_dict = setRoles(roles)
      with self.assertRaises(Exception):
        setUsers([], roles_dict)
      

    def testInvalidUserRole(self):
      roles = [
        {
            "Id": 1,
            "Name": "System Administrator",
            "Parent": 0
        }
      ]
      users = [
        {
          "Id": 1,
          "Name": "Adam Admin",
          "Role": 2
        }
      ]

      roles_dict = setRoles(roles)
      self.assertEqual(roles_dict[1].name, "System Administrator")
      self.assertEqual(roles_dict[1].parent, 0)
      self.assertEqual(roles_dict[1].children, set())
      self.assertEqual(roles_dict[1].users, set())

      with self.assertRaises(Exception):
        setUsers(users, roles_dict)


    def testMultipleUsersForRole(self):
      roles = [
        {
          "Id": 1,
          "Name": "System Administrator",
          "Parent": 0
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
          "Name": "John Admin",
          "Role": 1
        },
      ]
      roles_dict = setRoles(roles)
      user_dict = setUsers(users, roles_dict)
      self.assertEqual(roles_dict[1].name, "System Administrator")
      self.assertEqual(roles_dict[1].parent, 0)
      self.assertEqual(roles_dict[1].children, set())
      self.assertEqual(roles_dict[1].users, {1,2})
      
      self.assertEqual(user_dict[1].name, "Adam Admin")
      self.assertEqual(user_dict[1].role, 1)
      self.assertEqual(user_dict[2].name, "John Admin")
      self.assertEqual(user_dict[2].role, 1)


    def testDuplicateUserId(self):
      roles = [
        {
          "Id": 1,
          "Name": "System Administrator",
          "Parent": 0
        }
      ]
      users = [
        {
          "Id": 1,
          "Name": "Adam Admin",
          "Role": 1
        },
        {
          "Id": 1,
          "Name": "John Admin",
          "Role": 1
        },
      ]
      roles_dict = setRoles(roles)
      self.assertEqual(roles_dict[1].name, "System Administrator")
      self.assertEqual(roles_dict[1].parent, 0)

      with self.assertRaises(Exception):
        setUsers(users, roles_dict)