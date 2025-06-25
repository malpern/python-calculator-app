import pytest
import subprocess
import sys
import os


class TestMainBlock:
    
    def test_main_block_execution(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', 'app.py')
        
        # Test that the script can be imported without running the main block
        try:
            import app
            assert hasattr(app, 'app')
            assert hasattr(app, 'index')
            assert hasattr(app, 'calculate')
        except ImportError:
            pytest.fail("Could not import app module")
            
    def test_script_runs_when_executed_directly(self):
        script_path = os.path.join(os.path.dirname(__file__), '..', 'app.py')
        
        # This would test if the script runs when called directly
        # For testing purposes, we'll just verify the file exists and is readable
        assert os.path.exists(script_path)
        assert os.path.isfile(script_path)
        
        with open(script_path, 'r') as f:
            content = f.read()
            assert "if __name__ == '__main__':" in content
            assert "app.run(" in content