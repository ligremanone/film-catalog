from unittest import TestCase

from services.auth import redis_tokens


class RedisTokensHelperTestCase(TestCase):
    def test_generate_and_save_token(self) -> None:
        new_token = redis_tokens.generate_and_save_token()
        expected_exists = True
        self.assertEqual(
            expected_exists,
            redis_tokens.token_exists(new_token),
        )

    def test_add_token(self) -> None:
        new_token = redis_tokens.generate_token()
        redis_tokens.add_token(new_token)
        self.assertTrue(
            redis_tokens.token_exists(new_token),
        )

    def test_get_token(self) -> None:
        tokens = redis_tokens.get_tokens()
        self.assertTrue(tokens)
        self.assertIsInstance(tokens, list)
        self.assertGreater(len(tokens), 0)

    def test_delete_token(self) -> None:
        token = redis_tokens.generate_token()
        redis_tokens.add_token(token)
        self.assertTrue(
            redis_tokens.token_exists(token),
        )
        redis_tokens.delete_token(token)
        self.assertFalse(
            redis_tokens.token_exists(token),
        )
