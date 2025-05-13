#!/usr/bin/env python
import json
import sys
from textwrap import dedent
import warnings
from pydantic import ValidationError
from models.models import JobResults

from datetime import datetime

from crew import AutomatedJobSearch

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    print("## Welcome to Job Search Crew")
    print("-------------------------------")
    query = input(
        dedent("""
        Provide the list of characteristics for the job you are looking for: 
        """)
    )

    # Prompt user for security clearance preference
    print("Do you want to include jobs with:")
    print("1. Security clearance")
    print("2. Only security clearance")
    print("3. No security clearance")
    choice = input("Enter your choice (1, 2, or 3): ")

    crew = AutomatedJobSearch(query)  # Pass the choice to AutomatedJobSearch
    # crew = AutomatedJobSearch(query, clearance_filter=choice)  # Pass the choice to AutomatedJobSearch

    try:
        result = crew.crew().kickoff()
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

    # print("Validating final result..")
    # try:
    #     validated_result = JobResults.model_validate_json(json.loads(result.raw))
    # except ValidationError as e:
    #     print(e.json())
    #     print("Data output validation error.")

    print("\n\n########################")
    print("## VALIDATED RESULT ")
    print("########################\n")
    print(result)

if __name__ == "__main__":
    run()