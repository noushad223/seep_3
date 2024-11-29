from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer, AutoConfig
import numpy as np
from scipy.special import softmax
from concurrent.futures import ThreadPoolExecutor
from dbfunctions import *
import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'default-invalid-key')

class ChunkEvaluation(BaseModel):
    score: int = Field(description="Score from 0-100")
    feedback: str = Field(description="Detailed feedback explanation")

# Define structure for final evaluation output
class FinalEvaluation(BaseModel):
    overall_score: int = Field(description="Final score from 0-100")
    comments: str = Field(description="Summary of overall evaluation")
    chunk_evaluations: List[ChunkEvaluation] = Field(description="List of individual chunk evaluations")

# Text splitter to prevent token limit from being hit when using LLMs
def text_splitter(essay_text): 
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Adjust to the token limit of the model
        chunk_overlap=200  # Ensure overlap for context continuity
    )
    chunks = text_splitter.split_text(essay_text)
    return chunks

# Sentiment analysis, useful in english essays/coursework for emotional tone of the essay
# Values for get_embedding looks like this
# 1) negative 0.7389
# 2) neutral 0.2174
# 3) positive 0.0437

def get_embedding(text): 
    formatted_values = []
    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment-latest"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    config = AutoConfig.from_pretrained(MODEL)
    # PT
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    #model.save_pretrained(MODEL)
    encoded_input = tokenizer(text, return_tensors='pt')
    output = model(**encoded_input)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    ranking = np.argsort(scores)
    ranking = ranking[::-1]
    for i in range(scores.shape[0]):
        l = config.id2label[ranking[i]]
        s = scores[ranking[i]]
        formatted_values.append(f"{i+1}) {l} {np.round(float(s), 4)}")
    return "\n".join(formatted_values) 

# Template build for evaluating essay in chunks
def chunk_evaluation_chain():
    prompt = PromptTemplate.from_template("""
    You are an autochecker, designed to evaluate whether an essay has been marked too harshly or too lightly.
    Your task is to evaluate this chunk and provide a score and feedback in STRICT JSON format.

    Here is a chunk of the essay:
    {chunk} 

    Here is the sentimental analysis of the essay:
    {sentiment_info}
    
    Here is the marking scheme:
    {marking_scheme}
    
    IMPORTANT: You must respond ONLY with a JSON object in exactly this format:
    {{
        "score": <integer between 0 and 100>,
        "feedback": "<your detailed feedback here>"
    }}

    Do not include any additional text, explanations, or formatting outside of the JSON object.
    """)
    return prompt

# Final marks and feedback for summarising essay as a whole
def feedback_evaluation():
    prompt = PromptTemplate.from_template("""
    Based on the following feedback for essay chunks:

    {chained_feedback}

    IMPORTANT: You must respond ONLY with a JSON object in exactly this format:
    {{
        "overall_score": <integer between 0 and 100>,
        "comments": "<your detailed summary here>",
        "chunk_evaluations": []
    }}

    Do not include any additional text, explanations, or formatting outside of the JSON object.
    """)
    return prompt

# Main function to process courseworks
def process_coursework(coursework_id, marking_scheme_id):
    
    openAI_Model = OpenAI()
    chunk_parser = PydanticOutputParser(pydantic_object=ChunkEvaluation)
    final_parser = PydanticOutputParser(pydantic_object=FinalEvaluation)
    
    coursework_data = get_coursework(coursework_id)
    marking_scheme = get_marking_scheme(marking_scheme_id)
    chunk_evaluations = []  # Renamed for clarity
    
    prompt = chunk_evaluation_chain()
    feedback_prompt = feedback_evaluation()

    if coursework_data:
        # Get essay contents
        essay_text = coursework_data["coursework_content"]
        # Process essay_text into chunks of 1000 characters
        chunks = text_splitter(essay_text)

        # Process each chunk
        for chunk in chunks:
            sentiment = get_embedding(chunk)
            chain = prompt | openAI_Model | chunk_parser

            feedback = chain.invoke(
                input={
                    "chunk": chunk,
                    "sentiment_info": sentiment,
                    "marking_scheme": marking_scheme
                }
            )
            chunk_evaluations.append(feedback)
        
        # Format chunk evaluations for the final prompt
        formatted_feedback = "\n".join([
            f"Chunk {i+1}:\nScore: {eval.score}\nFeedback: {eval.feedback}" 
            for i, eval in enumerate(chunk_evaluations)
        ])

        # Generate final evaluation
        chain2 = feedback_prompt | openAI_Model | final_parser
        final_feedback = chain2.invoke({
            "chained_feedback": formatted_feedback
        })

        final_marks = final_feedback.overall_score
        final_comments = final_feedback.comments

        # Update database
        update_coursework_marks(coursework_id, final_marks, final_comments)
        return f"Processed coursework {coursework_id} successfully."
    return f"Coursework {coursework_id} not found."

def process_all_courseworks():
    coursework_ids = get_all_courseworks_ids()

    with ThreadPoolExecutor(max_workers=4) as executor:  
        results = list(executor.map(process_coursework, coursework_ids))

    for result in results:
        print(result)