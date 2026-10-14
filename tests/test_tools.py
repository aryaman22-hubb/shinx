import unittest
from shinx.tools import create_db_tool_registry
from tests.test_optimizer_agent import MockDatabaseAdapter


class TestDBTools(unittest.TestCase):
    def setUp(self):
        self.adapter = MockDatabaseAdapter()
        self.registry = create_db_tool_registry(self.adapter)

    def test_registry_contains_expected_tools(self):
        expected = ["explain_query", "inspect_table", "get_table_stats", "list_tables", "get_database_info"]
        registered_names = [tool.name for tool in self.registry.get_all_tools()]
        for name in expected:
            self.assertIn(name, registered_names)

    def test_explain_query_success(self):
        result = self.registry.execute("explain_query", {"query": "SELECT * FROM members WHERE email = 'test@example.com';"})
        self.assertNotIn("error", result)
        self.assertEqual(result.get("node_type"), "Seq Scan")

    def test_explain_query_blocks_mutations(self):
        for mutation in ["INSERT INTO members VALUES (1);", "DELETE FROM members;", "TRUNCATE members;", "DROP TABLE members;"]:
            res = self.registry.execute("explain_query", {"query": mutation})
            self.assertIn("error", res)
            self.assertIn("Only read-only SELECT queries", res["error"])

    def test_inspect_table(self):
        result = self.registry.execute("inspect_table", {"table_name": "members"})
        self.assertNotIn("error", result)
        self.assertEqual(result.get("name"), "members")

    def test_table_stats(self):
        result = self.registry.execute("get_table_stats", {"table_name": "members"})
        self.assertNotIn("error", result)
        self.assertEqual(result.get("row_count"), 50000)

    def test_list_tables(self):
        result = self.registry.execute("list_tables", {"schema_name": "public"})
        self.assertIn("tables", result)
        self.assertIn("members", result["tables"])
        self.assertIn("organizations", result["tables"])

    def test_database_info(self):
        result = self.registry.execute("get_database_info", {})
        self.assertNotIn("error", result)
        self.assertIn("version", result)


if __name__ == "__main__":
    unittest.main()
