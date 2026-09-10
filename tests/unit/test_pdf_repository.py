from pathlib import Path

import pytest
from diskcache import Cache
from pymupdf import Document

from features.pdf_display.models.pdf.pdf_doc import PdfDoc
from pdf_reader.core.caches.pdf_cache import PdfCache
from features.pdf_display.repository.pdf_repository import PdfRepository


@pytest.fixture
def cache(tmp_path):
    c = Cache(str(tmp_path), disk=PdfCache)
    yield c
    c.close()

@pytest.fixture
def sample_pdf_path():
    return Path(__file__).parent / "fixtures" /"sample.pdf"

@pytest.fixture
def invalid_path():
    return Path(__file__).parent / "fixtures" / "nonexistent.pdf"

@pytest.fixture
def text():
    return "Sample text"

@pytest.fixture
def page_number():
    return 1

class TestPdfRepository:
    @pytest.fixture(autouse=True)
    def _setup(self, cache):
        print('setting up repo')
        self.pdf_repo = PdfRepository(cache)
        yield
        print("Tear down repo")
        del self.pdf_repo

    def test_open_pdf(self, sample_pdf_path):
        response = self.pdf_repo.open_pdf(str(sample_pdf_path))
        assert response is not None
        assert isinstance(response, Document)

    def test_open_pdf_with_nonexistent_file(self, invalid_path):
        response = self.pdf_repo.open_pdf(str(invalid_path))
        assert response is None

    def test_open_pdf_with_empty_path_raises_help_message(self, sample_pdf_path):
        invalid_path = ""
        with pytest.raises(ValueError):
            self.pdf_repo.open_pdf(invalid_path)

    def test_save_pdf(self,page_number, text):
        response = self.pdf_repo.save_pdf(page_number,text)
        assert response is not None
        assert isinstance(response, PdfDoc)

