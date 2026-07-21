import pytest
from unittest.mock import patch
from backend.services.jd_matcher import calculate_match_percentage

def test_calculate_match_percentage_no_jd_keywords():
    """Test that match percentage is 0 if no JD keywords are provided."""
    score = calculate_match_percentage(["Python", "SQL"], [], 0.8)
    assert score == 0.0

@patch('backend.services.jd_matcher.identify_matched_keywords')
def test_calculate_match_percentage_with_matches(mock_identify):
    """Test the score calculation based on keyword overlap and semantic similarity."""
    # Mocking that 2 out of 4 JD keywords were found in the resume
    mock_identify.return_value = ["Python", "FastAPI"]
    
    score = calculate_match_percentage(
        resume_keywords=["Python", "FastAPI", "React"],
        jd_keywords=["Python", "FastAPI", "AWS", "Docker"],
        semantic_similarity=0.8
    )
    
    # Keyword Overlap = 2 / 4 = 0.5
    # Calculation: (0.5 * 0.6 + 0.8 * 0.4) * 100 = (0.3 + 0.32) * 100 = 62.0
    assert score == pytest.approx(62.0)
