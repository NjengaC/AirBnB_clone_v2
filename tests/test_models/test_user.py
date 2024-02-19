#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import test_basemodel
from models.user import User


class test_User(test_basemodel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "User"
        self.value = User

    def test_first_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.first_name), str)

    def test_last_name(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.last_name), str)

    def test_email(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.email), str)

    def test_password(self):
        """ """
        new = self.value()
        self.assertEqual(type(new.password), str)

    def test_user_attributes(self):
        user = User()
        # Test if user attributes exist
        self.assertTrue(hasattr(user, 'email'))
        self.assertTrue(hasattr(user, 'password'))
        self.assertTrue(hasattr(user, 'first_name'))
        self.assertTrue(hasattr(user, 'last_name'))

    def test_user_instance(self):
        # Test if user is an instance of User class
        user = User()
        self.assertIsInstance(user, User)

    def test_user_creation(self):
        # Test user creation with valid arguments
        user = User(email='test@example.com', password='password123',
                    first_name='John', last_name='Doe')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.password, 'password123')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')

    def test_user_creation_no_args(self):
        # Test user creation with no arguments
        user = User()
        self.assertIsNone(user.email)
        self.assertIsNone(user.password)
        self.assertIsNone(user.first_name)
        self.assertIsNone(user.last_name)

    def test_user_str_representation(self):
        # Test __str__() method
        user = User(email='test@example.com', password='password123',
                    first_name='John', last_name='Doe')
        expected_str = "[User] ({}) {}".format(user.id, user.__dict__)
        self.assertEqual(str(user), expected_str)

    def test_user_id_generation(self):
        # Test if id is generated for user instance
        user1 = User()
        user2 = User()
        self.assertNotEqual(user1.id, user2.id)
