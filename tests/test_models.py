
import unittest
import sys
sys.path.append('../')
from common_code import CommonTester
from app import models, db


class UserTestCase(CommonTester):
    def test_init(self):
        user = models.User(username='lala', name="Lala Lele", password='lele')
        user_admin = models.User(
            username='lili', name="Lili Lolo", password='lolo', superuser=True)

        self.assertNotEqual(user.password, 'lele')
        self.assertTrue(user.check_password('lele'))
        self.assertNotEqual(user_admin.password, 'lolo')
        self.assertTrue(user_admin.check_password('lolo'))

        self.assertFalse(user.is_admin)
        self.assertTrue(user_admin.is_admin)

        self.assertIsNone(user.get_id())
        self.assertIsNone(user_admin.get_id())

        # Sabe both users to our test database
        user.save()
        user_admin.save()
        self.assertEqual(user.get_id(), 1)
        self.assertEqual(user_admin.get_id(), 2)

    def test_set_check_password(self):
        user = models.User(username='lala', name="Lala Lele", password='lele')
        user_admin = models.User(
            username='lili', name="Lili Lolo", password='lolo', superuser=True)
        user.save()
        user_admin.save()

        self.assertTrue(user.check_password('lele'))
        user.set_password("huahua")
        self.assertTrue(user.check_password('huahua'))

        self.assertTrue(user_admin.check_password('lolo'))
        user_admin.set_password("yeahhh")
        self.assertTrue(user_admin.check_password('yeahhh'))

    # def test_constraints(self):
    #     user = models.User(username='lala', name="Lala Lele", password='lele')
    #     user2 = models.User(username='lala', name="Haha hehe", password='hum')
    #     user.save()
    #     # with self.assertRaises(sqlalchemy.exc.IntegrityError):
    #     with self.assertRaises(Exception):
    #         user2.save()


class TrabalhosTestCase(CommonTester):
    pass


# xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
if __name__ == '__main__':
    unittest.main()
