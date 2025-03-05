import unittest
from LoginChecker import LinearSearchChecker, BinarySearchChecker, HashTable, OptimizedBloomFilter, UltraFastCuckooFilter, generate_username

class TestLoginCheckers(unittest.TestCase):

    def test_linear_search(self):
        checker = LinearSearchChecker()
        checker.insert("user123")
        checker.insert("test456")
        self.assertTrue(checker.check("user123"))
        self.assertFalse(checker.check("not_in_list"))

    def test_binary_search(self):
        checker = BinarySearchChecker()
        usernames = ["alice", "bob", "charlie", "david"]
        for user in usernames:
            checker.insert(user)
        checker.prepare()
        self.assertTrue(checker.check("charlie"))
        self.assertFalse(checker.check("not_in_list"))

    def test_hash_table(self):
        checker = HashTable()
        checker.insert("user789")
        self.assertTrue(checker.check("user789"))
        self.assertFalse(checker.check("unknown_user"))

    def test_bloom_filter(self):
        bf = OptimizedBloomFilter(1000)
        bf.insert("alice")
        bf.insert("bob")
        self.assertTrue(bf.check("alice"))  # Should be True
        self.assertFalse(bf.check("not_in_list"))  # Should be False (low FP rate)

    def test_cuckoo_filter(self):
        cf = UltraFastCuckooFilter(1000)
        cf.insert("henry")
        cf.insert("isabel")
        self.assertTrue(cf.check("henry"))
        self.assertFalse(cf.check("unknown_user"))

    def test_generate_username(self):
        username = generate_username()
        self.assertTrue(isinstance(username, str))
        self.assertGreater(len(username), 4)  # Should be at least 5 characters

if __name__ == '__main__':
    unittest.main()
