from pomodoro.models import Session, Settings


def test_session_model_fields():
    assert Session.__tablename__ == "sessions"
    assert Session.type.property.columns[0].type.python_type is str
    assert Session.duration_seconds.property.columns[0].type.python_type is int


def test_settings_model_defaults():
    assert Settings.__tablename__ == "settings"
    assert Settings.work_minutes.property.columns[0].default.arg == 25
    assert Settings.short_break_minutes.property.columns[0].default.arg == 5
    assert Settings.long_break_minutes.property.columns[0].default.arg == 15
    assert Settings.cycles_until_long_break.property.columns[0].default.arg == 4
