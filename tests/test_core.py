"""
Unit tests for UtilTools core functionality
"""
import unittest
import tempfile
import os
from pathlib import Path
from utiltools.core import Plugin, PluginManager, register_plugin
from utiltools.config import Config


class TestPlugin(Plugin):
    """Test plugin for unit tests"""
    
    def execute(self, value=None):
        return {"result": value}


class TestPluginSystem(unittest.TestCase):
    """Test the plugin system"""
    
    def setUp(self):
        self.pm = PluginManager()
    
    def test_plugin_registration(self):
        """Test registering a plugin"""
        plugin = TestPlugin()
        self.pm.register(plugin, category="test")
        
        self.assertIn("testplugin", self.pm.list_plugins())
        self.assertIn("testplugin", self.pm.list_plugins("test"))
    
    def test_plugin_retrieval(self):
        """Test retrieving a plugin"""
        plugin = TestPlugin()
        self.pm.register(plugin)
        
        retrieved = self.pm.get_plugin("testplugin")
        self.assertIsInstance(retrieved, TestPlugin)
    
    def test_plugin_execution(self):
        """Test executing a plugin"""
        plugin = TestPlugin()
        self.pm.register(plugin)
        
        result = self.pm.execute("testplugin", value="test_value")
        self.assertEqual(result["result"], "test_value")
    
    def test_list_categories(self):
        """Test listing plugin categories"""
        plugin1 = TestPlugin()
        self.pm.register(plugin1, category="cat1")
        
        categories = self.pm.list_categories()
        self.assertIn("cat1", categories)


class TestConfig(unittest.TestCase):
    """Test the configuration system"""
    
    def setUp(self):
        # Create temporary config file
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, "test_config.yml")
        self.config = Config(config_path=self.config_path)
    
    def tearDown(self):
        # Clean up temporary files
        if os.path.exists(self.config_path):
            os.remove(self.config_path)
        os.rmdir(self.temp_dir)
    
    def test_default_config(self):
        """Test default configuration values"""
        self.assertEqual(self.config.get("logging.level"), "INFO")
        self.assertIsNotNone(self.config.get("network.timeout"))
    
    def test_set_and_get(self):
        """Test setting and getting configuration values"""
        self.config.set("test.value", "hello")
        self.assertEqual(self.config.get("test.value"), "hello")
    
    def test_save_and_load(self):
        """Test saving and loading configuration"""
        self.config.set("test.saved", "value")
        self.config.save()
        
        # Create new config instance with same path
        new_config = Config(config_path=self.config_path)
        self.assertEqual(new_config.get("test.saved"), "value")
    
    def test_nested_config(self):
        """Test nested configuration values"""
        self.config.set("level1.level2.level3", "nested_value")
        self.assertEqual(self.config.get("level1.level2.level3"), "nested_value")


class TestFileSearchPlugin(unittest.TestCase):
    """Test file search plugin"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.pm = PluginManager()
        self.pm.discover_plugins()
    
    def tearDown(self):
        # Clean up temporary files
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_file_search_by_pattern(self):
        """Test searching files by pattern"""
        # Create test files
        Path(self.temp_dir, "test1.txt").touch()
        Path(self.temp_dir, "test2.txt").touch()
        Path(self.temp_dir, "other.log").touch()
        
        plugin = self.pm.get_plugin("filesearchplugin")
        results = plugin.execute(path=self.temp_dir, pattern="*.txt", recursive=False)
        
        self.assertEqual(len(results), 2)
    
    def test_file_search_by_content(self):
        """Test searching files by content"""
        test_file = Path(self.temp_dir, "content.txt")
        test_file.write_text("This is a test file with specific content")
        
        plugin = self.pm.get_plugin("filesearchplugin")
        results = plugin.execute(
            path=self.temp_dir,
            pattern="*.txt",
            content="specific content",
            recursive=False
        )
        
        self.assertEqual(len(results), 1)
        self.assertIn("content.txt", results[0])


class TestTextProcessing(unittest.TestCase):
    """Test text processing plugins"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.pm = PluginManager()
        self.pm.discover_plugins()
        self.test_file = os.path.join(self.temp_dir, "test.txt")
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_text_search_replace(self):
        """Test text search and replace"""
        # Create test file
        with open(self.test_file, 'w') as f:
            f.write("Hello world, hello universe")
        
        plugin = self.pm.get_plugin("textsearchreplaceplugin")
        result = plugin.execute(
            self.test_file,
            search="hello",
            replace="hi",
            dry_run=False
        )
        
        self.assertEqual(result['matches'], 2)
        self.assertTrue(result['changed'])
        
        # Verify content changed
        with open(self.test_file, 'r') as f:
            content = f.read()
            self.assertIn("hi universe", content)


class TestSystemMonitoring(unittest.TestCase):
    """Test system monitoring plugins"""
    
    def setUp(self):
        self.pm = PluginManager()
        self.pm.discover_plugins()
    
    def test_system_info(self):
        """Test getting system information"""
        plugin = self.pm.get_plugin("systeminfoplugin")
        info = plugin.execute()
        
        self.assertIn("platform", info)
        self.assertIn("cpu", info)
        self.assertIn("memory", info)
        self.assertIn("disk", info)
        
        # Check that values are reasonable
        self.assertGreater(info['cpu']['usage_percent'], 0)
        self.assertGreater(info['memory']['total'], 0)
    
    def test_process_list(self):
        """Test listing processes"""
        plugin = self.pm.get_plugin("processmonitorplugin")
        processes = plugin.execute('list', limit=5)
        
        self.assertIsInstance(processes, list)
        self.assertLessEqual(len(processes), 5)
        
        if processes:
            self.assertIn('pid', processes[0])
            self.assertIn('name', processes[0])


if __name__ == '__main__':
    unittest.main()
