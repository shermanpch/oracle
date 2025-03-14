"""
This script retrieves content based on user-specified numeric inputs using the Oracle class,
then queries an LLM using the provided query_llm function from the llm_handler module.

Workflow:
    1. Prompt the user for a question, language, and three numeric inputs.
    2. Initialize the Oracle instance with a data directory.
    3. Process the numeric inputs to determine file paths.
    4. Retrieve the content from the parent and child .txt files.
    5. Pass the user query along with the retrieved content to the LLM for further processing.
"""

from llm_handler import query_llm
from oracle import Oracle

if __name__ == "__main__":
    # Prompt the user for their query.
    user_query = input("Enter your question: ")

    try:
        # Gather additional input: language and three numeric parameters.
        language = input("Enter the language: ")
        first = int(input("Enter the first number: "))
        second = int(input("Enter the second number: "))
        third = int(input("Enter the third number: "))
    except ValueError:
        # Handle invalid numeric inputs.
        print("Invalid input. Please enter valid integers.")
        exit(1)

    # Create an Oracle instance using the designated data directory.
    oracle = Oracle("data/")

    # Set the numeric inputs and process them into coordinate values.
    oracle.input(first, second, third)
    oracle.convert_to_cord()

    # Retrieve the content from the parent and child .txt files.
    parent_content = oracle.get_txt_file(oracle.get_parent_directory())
    child_content = oracle.get_txt_file(oracle.get_child_directory())

    # Query the LLM using the user's query and the retrieved file contents.
    # The result is then printed to the console.
    print(query_llm(user_query, parent_content, child_content, language))
