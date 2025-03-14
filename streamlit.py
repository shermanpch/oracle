from pydantic import BaseModel

import streamlit as st
from llm_handler import query_llm
from oracle import Oracle


def main():
    """
    Main function to run the Streamlit application for 'The Oracle - I Ching Interpreter'.

    This function configures the Streamlit page, sets up the sidebar for user input,
    processes the numeric inputs to determine file paths using the Oracle class,
    retrieves the content from the parent and child .txt files, queries the LLM using the
    provided inputs, and finally displays the output in Markdown format along with the
    child image centered under the "Line Change" header.
    """
    # Configure the Streamlit page settings
    st.set_page_config(page_title="The Oracle", layout="wide")
    st.title("🔮 The Oracle - I Ching Interpreter")

    # Sidebar: Collect input parameters from the user.
    with st.sidebar:
        st.header("🔢 Query Parameters")
        user_query = st.text_input("📜 Enter your question:")
        language = st.selectbox(
            "🌍 Select the language:", options=["Chinese", "English"]
        )
        first = st.number_input("🧮 Enter the first number:", value=0, step=1)
        second = st.number_input("🧮 Enter the second number:", value=0, step=1)
        third = st.number_input("🧮 Enter the third number:", value=0, step=1)
        submit_query = st.button("🔍 Submit Query")

    # Process and display results when the query is submitted.
    if submit_query:
        # Initialize the Oracle with the data directory.
        oracle = Oracle("data/")
        # Provide the numeric inputs to the Oracle.
        oracle.input(first, second, third)
        # Convert the inputs into coordinate values.
        oracle.convert_to_cord()

        # Retrieve the content from the parent and child .txt files.
        parent_content = oracle.get_txt_file(oracle.get_parent_directory())
        child_content = oracle.get_txt_file(oracle.get_child_directory())
        child_image_path = oracle.get_image_path(oracle.get_child_directory())

        st.header("📜 Oracle's Response")

        # Query the LLM with the user query, retrieved file contents, and language preference.
        structured_output = query_llm(
            user_query,
            parent_content,
            child_content,
            language,
            "streamlit",
        )

        def display_markdown(structured_output: BaseModel) -> None:
            """
            Display the contents of a Pydantic model as Markdown in a Streamlit app.

            This function converts the provided Pydantic model into a JSON-serializable
            dictionary and iterates over its key-value pairs. Each key is formatted as a Markdown header,
            and its corresponding value is displayed as a sub-section. If the key is "Line Change",
            the child image is displayed centered below the header.

            Parameters:
                structured_output (BaseModel): A Pydantic model instance containing structured data.

            Returns:
                None
            """
            # Convert Pydantic model to a JSON-serializable dictionary.
            data = structured_output.model_dump(mode="json")

            for key, value in data.items():
                # Display the field name as a Markdown header.
                header = f"### {key.replace('_', ' ').title()}"
                st.markdown(header)

                # If the key is "Line Change", display the child image centered.
                if key.strip().lower() == "line_change":
                    # Use HTML to center the image.
                    st.image(
                        child_image_path,
                        caption="Line Change",
                    )

                # If the value is a dictionary, iterate through its key-value pairs.
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        st.markdown(
                            f"**{sub_key.replace('_', ' ').title()}**: {sub_value}"
                        )
                else:
                    st.write(value)

        # Display the LLM's structured output in Markdown format along with the child image.
        display_markdown(structured_output)


if __name__ == "__main__":
    main()
