import pytest
from core.signals.bridge import Bridge
from pdf_reader.ui.main_window import MainWindow



class TestMainWindow:

    @pytest.fixture
    def window(self, qtbot, monkeypatch):
        """A MainWindow with frontend loading stubbed out, since we're not
        testing web content here — just the native Qt wiring around it."""
        monkeypatch.setattr(MainWindow, "_load_frontend", lambda self: None)
        win = MainWindow()
        qtbot.addWidget(win)  # ensures qtbot cleans it up after the test
        yield win
        win.view.setPage(None)  # release the page before the window/profile go away
        qtbot.wait(50)

    def test_window_title(self, window):
        assert window.windowTitle() == "Pdf Reader"

    def test_initial_size(self, window):
        assert window.size().width() == 1200
        assert window.size().height() == 800

    def test_webview_is_central_widget(self, window):
        assert window.centralWidget() is window.view

    def test_bridge_registered_on_channel(self, window):
        assert isinstance(window.bridge, Bridge)
        assert window.channel.registeredObjects()["bridge"] is window.bridge

    def test_webview_page_uses_the_same_channel(self, window):
        assert window.view.page().webChannel() is window.channel

    def test_missing_frontend_build_raises_helpful_error(self, qtbot, monkeypatch):
        """When DEV_MODE is off and dist/ hasn't been built, MainWindow should
        fail loudly with guidance rather than silently show a blank window."""
        monkeypatch.setattr("pdf_reader.config.DEV_MODE", 0)
        monkeypatch.setattr("os.path.exists", lambda path: False)

        with pytest.raises(FileNotFoundError, match="npm install && npm run build"):
            MainWindow()