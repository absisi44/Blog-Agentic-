
from asyncio import wait
import uvicorn
from fastapi import FastAPI, Request
from src.graphs.graph_builder import GraphBuilder
from src.llms.groqllm import GroqLLM

import os 
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()

os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY") # pyright: ignore[reportArgumentType]

## API's
@app.post("/blogs")
async def create_blog(request:Request):
    data=await request.json()
    topic=data.get("topic","")
    language=data.get("language","")
    
    #create llm object
    groq_llm=GroqLLM()
    llm=groq_llm.get_llm()
    
    #get graph builder 
    graph_builder=GraphBuilder(llm)
    if topic and language:
        graph=graph_builder.setup_graph(usecase="language")
        state=graph.invoke({"topic":topic ,"current_language":language})  # pyright: ignore[reportArgumentType]
        return {"data": state}
    elif topic: 
         graph=graph_builder.setup_graph(usecase="topic")
         state=graph.invoke({"topic":topic}) # pyright: ignore[reportArgumentType]
          
         return {"data":state}
     
    return {"error": "Missing topic"}  # fallback for invalid requests
    
if __name__=="__main__":
    uvicorn.run("app:app",host="0.0.0.0",port=8000,reload=True)    
    