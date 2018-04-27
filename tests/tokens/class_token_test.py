import pytest
from src.tokens.class_token import ClassToken


class TestClassToken:

    @pytest.fixture
    def mock_reader(self):
        return (char for char in 'ClassName:')

    def test_parse(self, mock_reader):
        res = ClassToken.parse(mock_reader);
        assert res == 'ClassName'
