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
        api_key="sk-proj-YTe9QLFG4LIyHNkKMqVBT3BlbkFJ1aitU6CtH3aJwn5oYdAR"
    )
    return llm
  


# Define the function to process the query
def infer_from_rag(query: str):
    modell = model()

    pre_prompt = """
    ### You are a sentence prediction bot.Based on the sentence provided , auto-fill the sentence using the right words. ###

    Here is the sentence: {question}
    """

    prompt = PromptTemplate(
        template=pre_prompt,
        input_variables=["question"]
    )

    chain = {"question": RunnablePassthrough()} | prompt | modell | StrOutputParser()
    res = chain.invoke({"question": query})
    return res

# Streamlit UI
st.title("Auto-fill bot")

# Display chat interface
if "history" not in st.session_state:
    st.session_state.history = []

# User input
user_input = st.text_input("Send a Sentence:")

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
