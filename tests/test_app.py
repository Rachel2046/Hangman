import os
import random
import tempfile

import pytest
from hm import app

def test_get_random_word_respects_min_length(monkeypatch):
    words = ["apple\n", "banana\n", "pear\n", "fig\n", "grape\n"]
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.writelines(words)
        temp_file.flush()
        temp_path = temp_file.name

    monkeypatch.setattr("hm.app.WORD_LIST", temp_path)
    random.seed(0)

    result = app.get_random_word(app.WORD_LIST, min_word_length=5)

    assert result is not None
    assert len(result) >= 5
    assert result in {"APPLE", "BANANA", "GRAPE"}

    os.remove(temp_path)


def test_get_random_word_skips_parentheses(monkeypatch):
    words = ["(ignore)\n", "hello\n", "world\n"]
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        temp_file.writelines(words)
        temp_file.flush()
        temp_path = temp_file.name

    monkeypatch.setattr("hm.app.WORD_LIST", temp_path)
    random.seed(1)

    result = app.get_random_word(app.WORD_LIST, min_word_length=1)

    assert result in {"HELLO", "WORLD"}
    assert result != "(IGNORE)"

    os.remove(temp_path)


def test_index_initializes_session():
    app.app.config["TESTING"] = True
    with app.app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200

        with client.session_transaction() as sess:
            assert "word" in sess
            assert sess["guesses"] == []
            assert sess["misses"] == 0
            assert sess["message"] == ""
