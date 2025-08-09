from token import STAR
from langgraph.graph import StateGraph,START,END
from src.llms.groqllm import GroqLLM
from src.states.blogstate import BlogState
from src.nodes.blog_node import BlogNode

## Graph builder
class GraphBuilder:
    def __init__(self,llm):
        self.llm=llm
        self.graph=StateGraph(BlogState)
    
    
    #build a graph
    def build_topic_graph(self):
        """
        Build a graph to generate blogs based on topic
        """
        
        self.blog_node_opj=BlogNode(self.llm)
        ## nodes
        self.graph.add_node("title_creation",self.blog_node_opj.title_creation)
        self.graph.add_node("content_generation",self.blog_node_opj.content_generation)
        
        ## Edges 
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation","content_generation")
        self.graph.add_edge("content_generation",END)
        
        return self.graph
    
    # build language graph function 
    def build_language_graph(self):
        """
        Build a graph fro blog generation with input topic and language
        """
        ## Add node 
        self.blog_node_opj=BlogNode(self.llm)
        ## nodes
        self.graph.add_node("title_creation",self.blog_node_opj.title_creation)
        self.graph.add_node("content_generation",self.blog_node_opj.content_generation)
        self.graph.add_node("arabic_translation",lambda state:self.blog_node_opj.translation({**state,"current_language":"arabic"})) # pyright: ignore[reportGeneralTypeIssues, reportArgumentType]
        self.graph.add_node("french_translation",lambda state:self.blog_node_opj.translation({**state,"current_language":"french"})) # pyright: ignore[reportArgumentType, reportGeneralTypeIssues]
        self.graph.add_node("route",self.blog_node_opj.route)
        
        ## add edges and conditional edges 
        self.graph.add_edge(START,"title_creation")
        self.graph.add_edge("title_creation","content_generation")
        self.graph.add_edge("content_generation","route")
        
        ## Add Conditional edge
        self.graph.add_conditional_edges(
            "route",
            self.blog_node_opj.route_decision,
            {
                "arabic":"arabic_translation",
                "french":"french_translation"
            }
        )
        
        self.graph.add_edge("arabic_translation",END)
        self.graph.add_edge("french_translation",END)
        
        return self.graph
        
        
    
    # set up the graph 
    def setup_graph(self,usecase):
        if usecase=="topic":
            self.build_topic_graph()
        
        if usecase=="language":
            self.build_language_graph()    
        return self.graph.compile()


## Blow code for the langsmith studio
llm=GroqLLM().get_llm()

## get the graph 
graph_builder=GraphBuilder(llm)
graph=graph_builder.build_language_graph().compile()