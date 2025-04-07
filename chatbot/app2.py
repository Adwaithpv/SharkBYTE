import streamlit as st
from langchain_openai import OpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import database
import os

NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

# Define the model function
def model():
    llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0,
        api_key="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"  # Fetch the API key from environment variables
    )
    return llm
  
# Fetch medicine data from your database module
medicine_info = database.get_data()

# Define the function to process the query
def infer_from_rag(query: str):
    modell = model()

    pre_prompt = """
    ### You are a drug inventory assistant. Answer the query using the data provided in the JSON format. If there is no answer, respond that the question is out of context ###
    Here is the data: {medicine_info}

    Here is the query: {question}
    """

    prompt = PromptTemplate(
        template=pre_prompt,
        input_variables=["question", "medicine_info"]
    )

    chain = {"question": RunnablePassthrough(), "medicine_info": RunnablePassthrough()} | prompt | modell | StrOutputParser()
    res = chain.invoke({"question": query, "medicine_info": medicine_info})
    return res

# Streamlit UI
st.title("MediBOT: Your Medicine Inventory Assistant")

# Initialize chat history if not already done
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Ask a question:")

if st.button("Send"):
    if user_input:
        # Get response from the model
        response = infer_from_rag(user_input)
        
        # Store user input and response
        st.session_state.history.append({"user": user_input, "bot": response})

# Display chat history
for chat in st.session_state.history:
    st.write(f"You: {chat['user']}")
    st.write(f"Bot: {chat['bot']}")
