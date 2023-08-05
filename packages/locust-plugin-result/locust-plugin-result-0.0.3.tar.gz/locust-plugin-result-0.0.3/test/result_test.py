# -*- coding: utf-8 -*-

import logging

from locust_plugin_result.result import set_result, RESULT_PASS, RESULT_WARN, RESULT_FAIL, logger

logger.level = logging.INFO


class _MockRunner():
    result = None


def _check_log_record(exp, caplog):
    for record in caplog.records:
        if exp in record.message:
            return True

    print("Log records:")
    print(caplog.records)
    print("ERROR: Did not find \"{exp}\" in log records")
    return False


def test_set_first_result():
    mr = _MockRunner()
    set_result(mr, RESULT_PASS, "Nice")
    assert mr.result.value == RESULT_PASS
    assert mr.result.reason == "Nice"


def test_set_result_again_warn_to_fail():
    mr = _MockRunner()

    set_result(mr, RESULT_WARN, "Up there")
    assert mr.result.value == RESULT_WARN
    assert mr.result.reason == "Up there"

    set_result(mr, RESULT_FAIL, "Out of bounds!")
    assert mr.result.value == RESULT_FAIL
    assert mr.result.reason == "Out of bounds!"


def test_set_result_again_fail_to_warn_ignored(caplog):
    mr = _MockRunner()

    set_result(mr, RESULT_FAIL, "Out of bounds!")
    assert mr.result.value == RESULT_FAIL
    assert mr.result.reason == "Out of bounds!"

    set_result(mr, RESULT_WARN, "Up there")  # This will not change result as we do no go from worse to better
    assert mr.result.value == RESULT_FAIL
    assert mr.result.reason == "Out of bounds!"

    assert _check_log_record("NOT changing result from 'fail' to 'warning': 'Up there', we will not go from worse to better!", caplog)


def test_set_non_standard_result_twice(caplog):
    mr = _MockRunner()
    set_result(mr, 'hip hip', "Lagkage")
    assert mr.result.value == 'hip hip'
    assert mr.result.reason == "Lagkage"

    set_result(mr, 'hurra', "Kagemand")
    assert mr.result.value == 'hurra'
    assert mr.result.reason == "Kagemand"

    assert _check_log_record("Non standard result values in use: 'hip hip', 'hurra'. No check, we don't know the order.", caplog)
