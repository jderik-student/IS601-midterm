# pylint: disable=unnecessary-dunder-call, invalid-name, unused-argument
'''
    This file contains tests to test app.py
'''
import os
import pytest
import singleton
from app import App

def test_app_start():
    """Test that the app starts correctly and intailizes everything needed to run the app."""
    app = App()
    current_env = app.get_environment_variable('ENVIRONMENT')
    current_user = app.get_environment_variable('USERNAME')
    assert current_env in ['DEV', 'PROD'], f"Invalid ENVIRONMENT: {current_env}"
    assert current_user in ['jderik-local', 'jderik-dev', 'jderik-prod'], f"Invalid USERNAME: {current_user}"
    assert os.path.exists(os.path.dirname(singleton.calc_history_path_location)), "Data directory was not created"
    assert os.path.exists(singleton.calc_history_path_location), "Calculator History csv file was not created"
    with pytest.raises(SystemExit) as e:
        app.start()
    assert e.type == SystemExit
    assert str(e.value) == "Exiting...", "The app did not exit as expected"
