import pytest
import core.signals.bridge as bridge


class TestBridge:

    def setup_method(self, method):
        print(f"Setting up {method.__name__}")
        self.bridge = bridge.Bridge()

    def teardown_method(self, method):
        print(f"Tearing down {method.__name__}")
        del self.bridge

    def test_get_system_info_returns_nonempty_string(self):
        info = self.bridge.get_system_info()
        assert isinstance(info, str)
        assert len(info) > 0

    def test_send_message_returns_expected_format(self):
        response = self.bridge.send_message("hello")
        assert "hello" in response
        assert response.startswith("Python received:")

    def test_bridge_message(self):
        test_result = self.bridge.send_message('Hello')
        assert test_result == "Python received: 'Hello'"

    def test_send_message_emits_signal(self, qtbot):
        """sendMessage should both return a value AND emit messageReceived,
        since React listens to the signal for proactive pushes."""

        with qtbot.waitSignal(self.bridge.messageReceived, timeout=1000) as blocker:
            self.bridge.send_message("ping")

        assert "ping" in blocker.args[0]

    def test_bridge_message_zero_args(self):
        with pytest.raises(TypeError):
            self.bridge.send_message(0)
