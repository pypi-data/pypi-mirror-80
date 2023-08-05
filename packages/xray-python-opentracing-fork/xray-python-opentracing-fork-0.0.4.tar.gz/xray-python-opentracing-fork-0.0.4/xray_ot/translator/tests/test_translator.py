from basictracer.span import BasicSpan
from opentracing.logs import ERROR_OBJECT

from xray_ot.settings import RecordingSettings
from xray_ot.translator.translator import preprocess_component_tags, Translator


DEFAULT_SETTINGS = RecordingSettings()


def test_preprocess_component_tags():
    tags_in = {
        "http.url": "https://example.com/",
        "http.method": "POST",
        "error": False,
        "hello": "",
        "hello.world": "",
        "abc": "",
    }
    tags_out = {"url": "https://example.com/", "method": "POST"}

    results = preprocess_component_tags("http", tags_in)
    assert results == tags_out


def test_translate_db_tags():
    tags_in = {
        "component": "db",
        "db.url": "postgres://127.0.0.1/db",
        "db.user": "postgres",
        "db.type": "postgres",
        "db.statement": "SELECT 1;",
    }
    tags_out = {
        "sql": {
            "url": tags_in["db.url"],
            "user": tags_in["db.user"],
            "database_type": tags_in["db.type"],
            "sanitized_query": tags_in["db.statement"],
        },
    }

    translator = Translator(DEFAULT_SETTINGS)
    results = translator.process_component(tags_in)

    assert results == tags_out


def test_translate_unknown_component_tags():
    tags_in = {
        "component": "graphql",
        "graphql.mutation": "createUser",
        "error": False,
    }
    tags_out = {
        "annotations": {"graphql_mutation": tags_in["graphql.mutation"],},
    }

    translator = Translator(DEFAULT_SETTINGS)
    results = translator.process_component(tags_in)

    assert results == tags_out


def test_translate_missing_component_tags():
    tags_in = {
        "error": False,
    }
    tags_out = {
        "annotations": {"_error": False,},
    }

    translator = Translator(DEFAULT_SETTINGS)
    results = translator.process_component(tags_in)

    assert results == tags_out


def test_translate_http_tags():
    tags_in = {
        "component": "http",
        "http.method": "POST",
        "http.url": "https://example.com/",
        "http.status_code": 405,
        "http.content_length": 5000,
        "http.other_repl": "abc",
    }
    tags_out = {
        "http": {
            "request": {"method": tags_in["http.method"], "url": tags_in["http.url"],},
            "response": {
                "status": tags_in["http.status_code"],
                "content_length": tags_in["http.content_length"],
                "other_repl": tags_in["http.other_repl"],
            },
        },
    }

    translator = Translator(DEFAULT_SETTINGS)
    results = translator.process_component(tags_in)

    assert results == tags_out


def test_translate_error_fatal_error():
    span = BasicSpan(tracer=None)

    tags_in = {
        "component": "http",
        "http.method": "POST",
        "error": True,
    }

    for tag_name, tag_value in tags_in.items():
        span.set_tag(tag_name, tag_value)

    span.log_kv({ERROR_OBJECT: ValueError("Expected an integer but got a string")})

    tags_out = {
        "fault": True,
        "http": {"request": {"method": "POST"}, "response": {}},
        "exception": {
            "message": "Expected an integer but got a string",
            "type": "ValueError",
        }
    }

    results = Translator.translate(settings=DEFAULT_SETTINGS, span=span)
    exception_id = results["exception"].pop("id")
    assert len(exception_id) == 16
    assert results == tags_out


def test_translate_error_handled_error():
    span = BasicSpan(tracer=None)

    tags_in = {
        "component": "http",
        "http.method": "POST",
        "error": True,
    }

    for tag_name, tag_value in tags_in.items():
        span.set_tag(tag_name, tag_value)

    tags_out = {
        "error": True,
        "http": {"request": {"method": "POST"}, "response": {}},
    }

    results = Translator.translate(settings=DEFAULT_SETTINGS, span=span)
    assert results == tags_out
