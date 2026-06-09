def test_create_app_default_configuration():
    from pomodoro import create_app

    app = create_app()

    assert app.config["TESTING"] is False
    assert app.config["DEBUG"] is True
    assert app.static_url_path == "/static"


def test_create_app_testing_configuration():
    from pomodoro import create_app

    app = create_app("testing")

    assert app.config["TESTING"] is True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == "sqlite:///:memory:"
