import os
import unittest
from shinx.services.llm_factory import get_chat_model


class TestLLMIntegration(unittest.TestCase):
    def test_llm_factory_initialization(self):
        llm = get_chat_model()
        self.assertIsNotNone(llm)

    def test_llm_live_invocation(self):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not api_key:
            self.skipTest("No GEMINI_API_KEY / GOOGLE_API_KEY found in environment or .env")

        llm = get_chat_model()
        res = llm.invoke("Reply with the single word: OK")
        content_str = str(res.content)
        self.assertIn("OK", content_str)


if __name__ == "__main__":
    unittest.main()
