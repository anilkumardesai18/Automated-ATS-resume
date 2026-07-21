import pytest
from unittest.mock import patch
from backend.services.resume_parser import validate_file

def test_validate_file_empty():
    """Test that empty files are rejected."""
    is_valid, error, file_type = validate_file(b"", "empty.pdf")
    assert is_valid is False
    assert "empty" in error.lower()

@patch('backend.services.resume_parser.magic.from_buffer')
def test_validate_file_valid_pdf(mock_magic):
    """Test that a valid PDF file passes validation."""
    mock_magic.return_value = 'application/pdf'
    file_data = b"mock pdf content"
    is_valid, error, file_type = validate_file(file_data, "resume.pdf")
    assert is_valid is True
    assert error == ""
    assert file_type == "pdf"

@patch('backend.services.resume_parser.magic.from_buffer')
def test_validate_file_unsupported_type(mock_magic):
    """Test that unsupported mime types are rejected."""
    mock_magic.return_value = 'image/jpeg'
    file_data = b"mock image content"
    is_valid, error, file_type = validate_file(file_data, "photo.jpg")
    assert is_valid is False
    assert "unsupported file type" in error.lower()
