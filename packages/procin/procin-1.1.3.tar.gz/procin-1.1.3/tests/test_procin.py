#!/usr/bin/env python

"""Tests for `procin` package."""

import pytest
import procin
import json

wierd_string = 'ä'
def test_filename():
    c = procin.Command()
    command = [wierd_string]
    s = c.command_to_filename(command)
    assert c.filename_to_command(s) == command
    command = ["echo", "-n", "[]"]
    s = c.command_to_filename(command)
    print(s)
    assert s == "echo^n-n^n^l^r^n"
    assert c.filename_to_command(s) == command
    print(command)

def test_array():
    c = procin.Command(json=True)
    ab = c.run(["echo", "-n", "[]"])
    assert ab == []
    ab = c.run(["echo", "[]"])
    assert ab == []
    ab = c.run(["/bin/echo", f'{{"v": "{wierd_string}"}}'])
    assert ab["v"] == wierd_string

def test_cache(tmpdir):
    c = procin.Command(json=True, cache=True, cache_dir=str(tmpdir))
    command = ["/bin/echo", "-n", '{"h": "hello"}']
    assert c.in_cache(command) == None
    j = c.run(command)
    assert j["h"] == "hello"
    s = c.in_cache(command)
    js = json.loads(s)
    assert j == js
    assert j == c.run(command)

def test_sematics():
    c = procin.Command()
    ab = c.run(["echo", "-n", "[]"], json=True)
    assert ab == []
    with pytest.raises(AttributeError) as excinfo:
        ab = c.run(["echo", "-n", "[]"], x=True)
    with pytest.raises(json.decoder.JSONDecodeError) as excinfo:
        ab = c.run(["echo", "-n", "not json"], json=True)

def test_print_command(capsys):
    c = procin.Command(print_command=True)
    ab = c.run(["echo", "hi"])
    captured = capsys.readouterr()
    assert "echo" in captured.out
    assert "hi" in captured.out

def test_print_output(capsys):
    c = procin.Command(print_output=True)
    ab = c.run(["echo", "hi"])
    captured = capsys.readouterr()
    assert "echo" not in captured.out
    assert "hi" in captured.out

def test_run_fail():
    c = procin.Command()
    with pytest.raises(Exception) as excinfo:
        _ = c.run(["false"])
    result = c.run(["false"], catch=True)

def travis_fail_test_cache_clear():
    command = ["true"]
    c = procin.Command(cache=True, cache_dir="test")
    c.run(command)
    assert c.in_cache(command) != None
    c.clear_cache()
    assert c.in_cache(command) == None

def test_run_does_not_change_defaults():
    c = procin.Command(json=True)
    js = c.run(["echo", "-n", "[]"], json=False)
    assert(isinstance(js, str))
    js = c.run(["echo", "-n", "[]"])
    assert(not isinstance(js, str))
    

