import base64
import os

import gradio as gr
import pandas as pd
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

df = pd.read_csv("./data/TMDB_movie_dataset_v11.csv")
engine = create_engine("sqlite:///db/movies.db")

df.to_sql("movies", engine, if_exists="replace", index=False)
movies_db = SQLDatabase.from_uri("sqlite:///db/movies.db")

model = ChatOpenAI(model="gpt-4-0125-preview", temperature=0, api_key=OPENAI_API_KEY)
agent_executor = create_sql_agent(model, db=movies_db, agent_type="openai-tools", verbose=True)

answer_prompt = """
You're a friendly AI assistant. See the results of running a given SQL query and generate natural responses to questions.

SQL query execution result:
{sql_result}

Please answer the result in Korean.
"""

answer_prompt_template = ChatPromptTemplate.from_template(answer_prompt)
answer_chain = answer_prompt_template | model | StrOutputParser()

with open("./assets/movie.png", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

with open("./src/main.css", "r") as file:
    css = file.read()

title_html = f"""
<div id="custom-title">
   <img src="data:image/png;base64,{encoded_string}" alt="AI CineSearch Icon">
   <h1>AI 영화 검색</h1>
</div>
"""

def movie_assistant(user_input):
    query = agent_executor.invoke({"input": user_input})
    result = answer_chain.invoke({"sql_result": query})
    return result

iface = gr.Interface(fn=movie_assistant,
                     inputs=[gr.Textbox(label="어떤 영화를 찾으시나요?", lines=10)],
                     outputs=[gr.Textbox(label="AI가 찾은 영화입니다.", lines=10)],
                     description=title_html,
                     css=css)

iface.launch(debug=True)