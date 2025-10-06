from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from langserve import add_routes


## Load Keys
load_dotenv()

## Groq API Key
groq_api_key = os.getenv("GROQ_API_KEY")


## LLM model
model = ChatGroq(model="Gemma2-9b-It",groq_api_key=groq_api_key)


## Create Prompt template
system_template = "Translate the following in {language}"
prompt_template = ChatPromptTemplate.from_messages([
    ("system",system_template),
    ("user","{text}")
])

## Create Output Parser
parser = StrOutputParser()

## Create Chain Prompt-->Model-->Parser
chain = prompt_template | model | parser


## App defination

# app = FastAPI(title="Langchain Server",
#               version="1.0",
#               description="A simple API server using Langchain runnable interfaces"
#               )

app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server using Langchain runnable interfaces",
    openapi_url=None,   # 👈 disables /openapi.json
    docs_url=None,      # 👈 disables Swagger UI (/docs)
    redoc_url=None      # 👈 disables ReDoc (/redoc)
)



## Adding Chain Route
add_routes(
    app,
    chain,
    path="/chain"
)

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app,host="127.0.0.1",port=8000)
