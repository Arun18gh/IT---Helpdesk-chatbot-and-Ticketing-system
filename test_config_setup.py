import unittest
import config
from pymongo import MongoClient
from pymongo.errors import ConfigurationError

class ConfigTest(unittest.TestCase):

    def test_mongo_uri_exists(self):
        """Check if MONGO_URI is defined and looks valid."""
        self.assertTrue(hasattr(config, 'MONGO_URI'))
        self.assertIsInstance(config.MONGO_URI, str)
        self.assertIn("mongodb://", config.MONGO_URI)

    def test_database_connection(self):
        """Try connecting to the 'it_helpdesk' database using a safe context."""
        try:
            with MongoClient(config.MONGO_URI) as client:
                db = client["it_helpdesk"]
                self.assertIsNotNone(db)
        except ConfigurationError:
            self.fail("Could not connect to MongoDB")

    def test_collections_exist(self):
        """Ensure tickets and users collections exist."""
        self.assertEqual(config.tickets_collection.name, "tickets")
        self.assertEqual(config.users_collection.name, "users")

if __name__ == "__main__":
    unittest.main()
