# -*- coding: utf-8 -*-
"""test_verifier.py — 回验器测试（三信号PASS/FAIL分支·pytest）"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from verifier.verifier import verify_artifact_exists, verify_task_completion, verify_user_feedback  # noqa: E402


def test_artifact_exists_pass():
    fp = os.path.join(os.path.dirname(__file__), "test_verifier.py")
    assert verify_artifact_exists(fp)["value"] is True


def test_artifact_exists_fail():
    assert verify_artifact_exists(os.path.join(os.path.dirname(__file__), "不存在.py"))["value"] is False


def test_user_feedback_pass():
    assert verify_user_feedback("同意，继续")["value"] is True


def test_user_feedback_reject():
    assert verify_user_feedback("不行，重做")["value"] is False


def test_user_feedback_empty():
    assert verify_user_feedback("")["value"] is False


def test_task_completion_json():
    fp = os.path.join(os.path.dirname(__file__), "..", "src", "data", "router_rules.json")
    assert verify_task_completion(fp)["value"] is True
