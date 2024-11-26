import pytest
import os
from pytest import fixture
import torch
from unittest.mock import MagicMock, patch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from llm import (
    text_splitter,
    get_embedding,
    chunk_evaluation_chain,
    feedback_evaluation,
    process_coursework,
)

def test_text_splitter():
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit." * 50
    chunks = text_splitter(text)
    assert len(chunks) > 0
    assert all(len(chunk) <= 1000 for chunk in chunks)

def test_get_embedding():

    text = "This is a test sentence."
    result = get_embedding(text)
    
    assert isinstance(result, str), "Embedding result should be a string"
    
    # Check that it contains sentiment labels (case-insensitive)
    assert any(keyword in result.lower() for keyword in ["negative", "neutral", "positive"]), \
        "Result should contain sentiment keywords (negative, neutral, positive)"
    
    # Check that the result is properly structured
    lines = result.split('\n')
    assert len(lines) > 0, "Result should contain at least one ranking"
    for line in lines:
        assert ')' in line and ' ' in line, \
            "Each line should be formatted as 'rank) label probability'"
        parts = line.split(' ')
        assert len(parts) >= 3, "Each line should have a rank, label, and score"
        assert parts[0].endswith(')'), "First part should end with ')' indicating rank"
        try:
            float(parts[-1])  # Check if the last part is a valid number (probability)
        except ValueError:
            assert False, "The last part of each line should be a numeric score"
        
def test_chunk_evaluation_chain_filled():

    prompt = chunk_evaluation_chain()


    example_chunk = "The essay provides a good thesis but lacks depth."
    example_sentiment = "Neutral with slightly positive tone."
    example_scheme = "Content: 40%, Structure: 30%, Grammar: 30%."

    filled_prompt = prompt.format(
        chunk=example_chunk,
        sentiment_info=example_sentiment,
        marking_scheme=example_scheme
    )


    assert example_chunk in filled_prompt, "The essay chunk should be correctly inserted into the prompt"
    assert example_sentiment in filled_prompt, "The sentiment info should be correctly inserted into the prompt"
    assert example_scheme in filled_prompt, "The marking scheme should be correctly inserted into the prompt"


    assert '"score": <integer between 0 and 100>' in filled_prompt, \
        "The JSON example format should remain intact after formatting"
    assert '"feedback": "<your detailed feedback here>"' in filled_prompt, \
        "The JSON example format should remain intact after formatting"

def test_feedback_evaluation_prompt_filled():
    
    prompt = feedback_evaluation()

    example_feedback = "Chunk 1: Good analysis. Chunk 2: Needs more depth."
    
    filled_prompt = prompt.format(chained_feedback=example_feedback)

    assert example_feedback in filled_prompt, "The feedback should be correctly inserted into the prompt"
    assert '"overall_score": <integer between 0 and 100>' in filled_prompt, \
        "The JSON format for overall_score should remain intact after formatting"
    assert '"comments": "<your detailed summary here>"' in filled_prompt, \
        "The JSON format for comments should remain intact after formatting"
    assert '"chunk_evaluations": []' in filled_prompt, \
        "The JSON format for chunk_evaluations should remain intact after formatting"

def test_process_coursework():

    os.environ["OPENAI_API_KEY"] = "api-key"
 
    with patch("llm.get_coursework") as mock_get_coursework, \
         patch("llm.get_marking_scheme") as mock_get_marking_scheme, \
         patch("llm.update_coursework_marks") as mock_update_coursework_marks:
        
       
        mock_get_coursework.return_value = {
            "coursework_id": 1,
            "coursework_content": "This is an example essay text that is longer than 1000 characters " 
                                   "to simulate chunking. " * 50  # Simulate a long text
        }
        mock_get_marking_scheme.return_value = "Sample Marking Scheme"
        mock_update_coursework_marks.return_value = None

        essay_text = mock_get_coursework.return_value["coursework_content"]

        chunks = text_splitter(essay_text)

        assert len(chunks) > 1, "Text should split into multiple chunks."

        result = process_coursework(1, 1)

        assert result == "Processed coursework 1 successfully."

        mock_get_coursework.assert_called_once_with(1)
        mock_get_marking_scheme.assert_called_once_with(1)
        mock_update_coursework_marks.assert_called_once()


