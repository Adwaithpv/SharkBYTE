import streamlit as st
from langchain_openai import OpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# Define the model function
def model():
    llm = OpenAI(
        model="gpt-3.5-turbo-instruct",
        temperature=0,
        api_key="API-KEY-HERE"
    )
    return llm

# Define the function to process the query
def infer_from_rag(query: str):
    modell = model()

    pre_prompt = """
    ### You are a drug inventory assistant. Answer the query using the data provided in the JSON format. If there is no answer, respond that the question is out of context ###
    [
      {{
        "medicine_name": "AmoxiCure",
        "type": "Antibiotic",
        "expiry_date": "2025-09-14",
        "manufacturing_date": "2023-09-14",
        "current_location": "Warehouse A - Chicago, IL",
        "last_updated_time": "2024-08-30T14:23:45Z"
      }},
      {{
        "medicine_name": "PainRelief",
        "type": "Analgesic",
        "expiry_date": "2024-12-02",
        "manufacturing_date": "2022-12-02",
        "current_location": "Pharmacy - Springfield, IL",
        "last_updated_time": "2024-08-30T10:15:22Z"
      }},
      {{
        "medicine_name": "CoughAway",
        "type": "Antitussive",
        "expiry_date": "2026-01-30",
        "manufacturing_date": "2024-01-30",
        "current_location": "Distributor Center - St. Louis, MO",
        "last_updated_time": "2024-08-29T08:50:17Z"
      }},
      {{
        "medicine_name": "Glucosan",
        "type": "Antidiabetic",
        "expiry_date": "2025-06-11",
        "manufacturing_date": "2023-06-11",
        "current_location": "Warehouse B - Peoria, IL",
        "last_updated_time": "2024-08-28T12:32:05Z"
      }},
      {{
        "medicine_name": "FluShield",
        "type": "Vaccine",
        "expiry_date": "2025-11-18",
        "manufacturing_date": "2023-11-18",
        "current_location": "Health Center - Urbana, IL",
        "last_updated_time": "2024-08-30T16:45:55Z"
      }},
      {{
        "medicine_name": "HeartSecure",
        "type": "Cardiovascular",
        "expiry_date": "2025-05-07",
        "manufacturing_date": "2023-05-07",
        "current_location": "Hospital - Decatur, IL",
        "last_updated_time": "2024-08-31T09:12:42Z"
      }},
      {{
        "medicine_name": "ZyloCalm",
        "type": "Anxiolytic",
        "expiry_date": "2025-02-23",
        "manufacturing_date": "2023-02-23",
        "current_location": "Pharmacy - Bloomington, IL",
        "last_updated_time": "2024-08-31T07:34:10Z"
      }},
      {{
        "medicine_name": "DermCare",
        "type": "Dermatological",
        "expiry_date": "2024-11-10",
        "manufacturing_date": "2022-11-10",
        "current_location": "Warehouse A - Chicago, IL",
        "last_updated_time": "2024-08-29T11:20:50Z"
      }},
      {{
        "medicine_name": "AllerFree",
        "type": "Antihistamine",
        "expiry_date": "2026-03-19",
        "manufacturing_date": "2024-03-19",
        "current_location": "Distributor Center - St. Louis, MO",
        "last_updated_time": "2024-08-28T14:03:38Z"
      }},
      {{
        "medicine_name": "NeuroMax",
        "type": "Nootropic",
        "expiry_date": "2025-08-05",
        "manufacturing_date": "2023-08-05",
        "current_location": "Warehouse B - Peoria, IL",
        "last_updated_time": "2024-08-30T19:18:21Z"
      }},
      {{
        "medicine_name": "HyperBlock",
        "type": "Antihypertensive",
        "expiry_date": "2025-07-22",
        "manufacturing_date": "2023-07-22",
        "current_location": "Health Center - Urbana, IL",
        "last_updated_time": "2024-08-30T21:37:54Z"
      }}
    ]

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
