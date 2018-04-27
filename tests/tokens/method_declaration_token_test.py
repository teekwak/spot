import pytest
from src.tokens.method_declaration_token import MethodDeclarationToken


class TestMethodDeclarationToken:

    @pytest.fixture
    def mock_reader(self):
        return (char for char in 'MethodName()')

    def test_parse(self, mock_reader):
        res = MethodDeclarationToken.parse(mock_reader);
        assert res == 'MethodName'
