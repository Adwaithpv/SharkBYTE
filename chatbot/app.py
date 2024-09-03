import streamlit as st
from langchain_openai import OpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import database

# Define the model function
def model():
    llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0,
        api_key="API_KEY"
    )
    return llm
  
medicine_info=database.get_data()

# Define the function to process the query
def infer_from_rag(query: str):
    modell = model()

    pre_prompt = """
    ### You are a drug inventory assistant. Answer the query using the data provided in the JSON format. If there is no answer, respond that the question is out of context ###
    {{medicine_info}}

    Here is the query: {question}
    """

    prompt = PromptTemplate(
        template=pre_prompt,
        input_variables=["question"]
    )

    chain = {"question": RunnablePassthrough()} | prompt | modell | StrOutputParser()
    res = chain.invoke({"question": query})
    return res

# Streamlit UI
st.title("Medicine Inventory Chatbot")

# Display chat interface
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Ask a question about the medicine inventory:")

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
