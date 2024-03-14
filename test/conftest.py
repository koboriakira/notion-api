def pytest_configure(config):
    config.addinivalue_line(
        "markers", "learning: mark tests as learning exercises"
    )
