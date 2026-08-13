import unittest

from app.users.models import User
from app.ai.agent import serialize_tool_result


class SerializeToolResultTests(unittest.TestCase):
    def test_handles_sqlalchemy_models(self):
        user = User(id=7, name="Alice")

        result = serialize_tool_result([user])

        self.assertEqual(result, [{"id": 7, "name": "Alice"}])


if __name__ == "__main__":
    unittest.main()
