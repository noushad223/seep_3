import pytest
from unittest.mock import MagicMock, patch
from conftest import *
from llm import *

@patch("conftest.db_conn")
def test_get_all_courseworks_ids(mock_db_conn):
    # Mock database cursor
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(1,), (2,), (3,)]  # Example IDs

    # Mock connection context manager
    mock_conn = MagicMock()
    mock_conn.execute.return_value = None
    mock_conn.fetchall.return_value = [(1,), (2,), (3,)]
    mock_db_conn.return_value.__enter__.return_value = mock_conn

    # Call the function under test
    result = get_all_courseworks_ids()

    # Assertions
    assert result == [1, 2, 3]  # Ensure IDs are extracted correctly
    mock_db_conn.assert_called_once()  # Verify db_conn was called
    mock_conn.execute.assert_called_once_with(
        "SELECT coursework_id FROM Courseworks WHERE coursework_marks IS NULL;"
    )

def test_text_splitter():
    text = "a" * 1500
    chunks = text_splitter(text)
    assert len(chunks) == 2
    assert len(chunks[0]) <= 1000
    assert len(chunks[1]) <= 1000

@patch("llm.AutoTokenizer.from_pretrained")
@patch("llm.AutoModelForSequenceClassification.from_pretrained")
def test_get_embedding(mock_model, mock_tokenizer):
    # Mock tokenizer
    mock_tokenizer.return_value = MagicMock()
    mock_tokenizer.return_value.__call__.return_value = {"input_ids": [1, 2, 3]}
    
    # Mock model
    mock_model_instance = MagicMock()
    mock_model_instance.return_value = {"logits": [[2.0, 1.0, 0.5]]}
    mock_model.return_value = mock_model_instance
    
    # Mock softmax
    with patch("llm.softmax", return_value=[0.8, 0.15, 0.05]):
        result = get_embedding("test text")
        
        assert "1) negative 0.8" in result
        assert "2) neutral 0.15" in result

@patch("llm.get_coursework")
@patch("llm.get_marking_scheme")
@patch("llm.text_splitter")
@patch("llm.get_embedding")
@patch("llm.OpenAI")
@patch("llm.update_coursework_marks")
def test_process_coursework(mock_update, mock_openai, mock_sentiment, mock_splitter, mock_scheme, mock_coursework):
    # Mock coursework data
    mock_coursework.return_value = {
        "coursework_id": 1,
        "coursework_content": "Test essay text."
    }
    
    # Mock marking scheme
    mock_scheme.return_value = "Marking scheme content"
    
    # Mock text splitter
    mock_splitter.return_value = ["Chunk 1", "Chunk 2"]
    
    # Mock sentiment analysis
    mock_sentiment.side_effect = ["sentiment1", "sentiment2"]
    
    # Mock OpenAI chain
    mock_openai.return_value.invoke.side_effect = [
        {"score": 90, "feedback": "Good"},
        {"score": 85, "feedback": "Excellent"},
        {"overall_score": 87, "comments": "Great job", "chunk_evaluations": []},
    ]
    
    result = process_coursework(1, 1)
    assert "Processed coursework 1 successfully." in result
    
    # Ensure database is updated
    mock_update.assert_called_once_with(1, 87, "Great job")