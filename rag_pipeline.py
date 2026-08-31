from langgraph.graph import StateGraph, START, END
from typing import List, TypedDict
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
load_dotenv()

LLM = ChatGroq(model="openai/gpt-oss-20b", api_key=os.getenv("GROQ_API_KEY"))




class AgentState(TypedDict):
    question: str
    documents: List[str]
    answer: str
    trials: int
    

    
def build_pipeline(vectorstore):
    def retrieve_node(state: AgentState):
        question = state["question"]
        docs = vectorstore.similarity_search(question, k=3)
        return {"documents": [doc.page_content for doc in docs]}
    
    def grade_node(state: AgentState):
        documents = state["documents"] 
        question = state["question"]
        prompt = (f"given the question: {question}, and the documents: {documents} are the documents relevant to the question ansewr yes or no only")
        response = LLM.invoke(prompt)
        return {"answer": response.content.strip().lower(), "trials": state["trials"] + 1}
    
    def genarate_node(state: AgentState):
        documents = state["documents"]
        question = state["question"]
        prompt = (f"given the question: {question}, and the documents: {documents} generate a detailed answer to the question following the context of the documents")
        response = LLM.invoke(prompt)
        return {"answer": response.content}
    
    
    def route_node(state: AgentState):
        answer = state["answer"]
        
        if state["trials"] >= 3:
            return "genarate_node"
        if answer == "yes":
            return "genarate_node"
        else:
            return "retrieve_node"
        
    graph = StateGraph(AgentState)
    graph.add_node("retrieve_node", retrieve_node)
    graph.add_node("grade_node", grade_node)
    graph.add_node("genarate_node", genarate_node)
    graph.add_edge(START, "retrieve_node")
    graph.add_edge("retrieve_node", "grade_node")
    graph.add_conditional_edges("grade_node", route_node)
    graph.add_edge("genarate_node", END)
    
    agent = graph.compile()
    return agent
    
    