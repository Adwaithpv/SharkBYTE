import streamlit as st
import google.generativeai as genai
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
import database
from langchain_google_genai import GoogleGenerativeAI

# Define the model function
def model():
    # Configure the Gemini API
    genai.configure(api_key="")
    
    # Initialize the model using LangChain's Google integration
    llm = GoogleGenerativeAI(
        model="gemini-2.0-flash-lite",  
        temperature=0,
        google_api_key=""  
    )
    return llm
  
medicine_info = database.get_data()

# Define the function to process the query
def infer_from_rag(query: str):
    modell = model()

    pre_prompt = """
    ### You are a friendly drug inventory management assistant. Answer the query using the data provided in the JSON format.If no data is present regarding the medcine asked, reply that the product does not exist in the database. If a question is asked that is out of context, respond that the question is out of context.Do not offer any medical advice or diagnosis. ###
    {medicine_info}

    Here is the query: {question}
    """

    prompt = PromptTemplate(
        template=pre_prompt,
        input_variables=["question", "medicine_info"]
    )

    chain = (
        {
            "question": RunnablePassthrough(),
            "medicine_info": lambda _: medicine_info
        } 
        | prompt 
        | modell 
        | StrOutputParser()
    )
    
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
