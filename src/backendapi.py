from fastapi import FastAPI
from typing import List
from dbfunctions import evaluate_coursework, remain_marks, change_marks
from llm import process_all_courseworks

app = FastAPI()

# For the page with two input bars and button to process all courseworks
# First input bar is the module_id
# Second input bar is the marking_scheme_id
# Everything is done in the database, so nothing needs to be returned here
@app.post("/submit")
def submit_data(data: List[str]):
    module_id, marking_scheme_id = data[0], data[1]
    process_all_courseworks(module_id, marking_scheme_id)
    return None

# For this api call (Optional)
# After all the courseworks have been processed by the automarker
# It will display all the unfairly marked courseworks in result
# Result is an array of dictionaries with this format
# {
#  "coursework_id": coursework_id,
#  "status": status,
#  "coursework_marks": coursework_marks,
#  "autochecker_marks": autochecker_marks,
#  "autochecker_comments": autochecker_comments
# }
@app.post("/evaluate")
async def evaluate():
    # Call the function to evaluate courseworks
    result = evaluate_coursework()
    return result

# Two buttons one to auto update mark to auto mark and one to make it teacher mark

# Accepts the auto mark marks, and changes coursework mark to autochecker mark
@app.post("/acceptautomark")
async def acceptautomark(data: str):
    change_marks(data)
    return None

# Denys the auto mark marks, changes autochecker marks to be the coursework marks
# This is here just to prevent it from showing up after calling the evaluate function again
@app.post("/denyautomark")
async def denyautomark(data: str):
    remain_marks(data)
    return None