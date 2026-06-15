"""hello モジュールのテスト。"""

from hello import greet  # pythonpath=src により src 直下を解決する。


def test_greet_default() -> None:
    # 引数なしの既定挨拶を確認する。
    assert greet() == "Hello, world!"


def test_greet_name() -> None:
    # 名前を渡したときの出力を確認する。
    assert greet("base") == "Hello, base!"
