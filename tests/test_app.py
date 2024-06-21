# pylint: disable=unnecessary-dunder-call, invalid-name, unused-argument
'''
    This file contains tests to test app.py
'''
import pytest
from app import App

def test_app_start(monkeypatch):
    """Test that the REPL exits correctly on 'exit' command."""
    monkeypatch.setattr('builtins.input', lambda _: 'exit')
    app = App()
    current_env = app.get_environment_variable('ENVIRONMENT')
    current_user = app.get_environment_variable('USERNAME')
    assert current_env in ['DEV', 'PROD'], f"Invalid ENVIRONMENT: {current_env}"
    assert current_user in ['jderik-local', 'jderik-dev', 'jderik-prod'], f"Invalid USERNAME: {current_user}"
    with pytest.raises(SystemExit) as e:
        app.start()
    assert e.type == SystemExit
    assert str(e.value) == "Exiting...", "The app did not exit as expected"
