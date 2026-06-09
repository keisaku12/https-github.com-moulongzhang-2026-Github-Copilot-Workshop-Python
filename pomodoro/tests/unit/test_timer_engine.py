from pomodoro.config import DevelopmentConfig, ProductionConfig, TestingConfig


def test_development_config_values():
    assert DevelopmentConfig.DEBUG is True
    assert DevelopmentConfig.TESTING is False
    assert DevelopmentConfig.SQLALCHEMY_DATABASE_URI.startswith("sqlite:///")


def test_testing_config_values():
    assert TestingConfig.DEBUG is False
    assert TestingConfig.TESTING is True
    assert TestingConfig.SQLALCHEMY_DATABASE_URI == "sqlite:///:memory:"


def test_production_config_values():
    assert ProductionConfig.DEBUG is False
    assert ProductionConfig.TESTING is False
    assert ProductionConfig.SQLALCHEMY_DATABASE_URI.startswith("sqlite:///")
