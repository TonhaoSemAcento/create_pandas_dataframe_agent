from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
import pandas as pd
import streamlit as st
import tempfile

def read_csv_into_dataframe(csv_name):
   df = pd.read_csv(csv_name,encoding="utf-8", delimiter=";")
   return df

def main():
    st.set_page_config(page_title="👨‍💻 Talk with your CSV")
    st.title("👨‍💻 Talk with your CSV")
    uploaded_file = st.sidebar.file_uploader("Upload your Data", type="csv")
    setup = False
    question = st.text_input("Send a Message")
    if st.button("Submit Query", type="primary"):
        with st.spinner("Processing your question..."):
            if not setup:
                if uploaded_file :
                #use tempfile because CSVLoader only accepts a file_path
                    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_file_path = tmp_file.name

                    data_frame = read_csv_into_dataframe(tmp_file_path)
                    print (data_frame.head())
                    llm = OpenAI(temperature=0)

                    p_agent = create_pandas_dataframe_agent(llm=llm,df=data_frame,verbose=True)


                    setup = True

                # Run the query and return the result
                result = p_agent.run(question)
                st.write("Response:", result)

if __name__ == '__main__':
    main()
