
from src.states.blogstate import BlogState
from langchain_core.messages import SystemMessage,HumanMessage
from src.states.blogstate import Blog

class BlogNode:
    """class to represent thew nodes 
    """
    
    def __init__(self,llm):
        self.llm=llm
        
    
    # First node for title creation 
    def title_creation(self,state:BlogState):
        """
        Create the title of the blog 
        """
        if "topic" in state and state['topic']:
            prompt="""
                        You Are an expert blog content writer. Use Markdown Formatting.
                        Generate a blog title for the {topic}. This title should be creative and SEO Friendly
                    """
            system_message=prompt.format(topic=state['topic'])   
            response=self.llm.invoke(system_message) 
            return {"blog":{"title":response.content}}  
        
    
    # second node for content generation 
    def content_generation(self, state: BlogState):
        """
        Generate the blog 
        """   
        if "topic" in state and state['topic']:
            system_prompt="""
                            You Are an expert blog content writer. Use Markdown Formatting.
                        Generate a blog content with detailed breakdown for the {topic}.
                        """
            system_message=system_prompt.format(topic=state["topic"]) 
            response=self.llm.invoke(system_message)  
            return {
                "blog":{
                    "title":state["blog"]['title'],"content":response.content # pyright: ignore[reportArgumentType]
                    }
            } 
     
    # Third node for translation
    def translation(self, state: BlogState):
        """
        Translate the content to the specified language.
        """
        current_language = state["current_language"]
        blog_content = state["blog"]["content"] # pyright: ignore[reportArgumentType]

        translation_prompt = f"""
        Translate the following text into {current_language}.
        - The output should only be the translated text.
        - Do not add a title or any extra information.
        - The entire response must be in {current_language}.
        - Do not include any characters or words from other languages.
        
        ORIGINAL CONTENT:
        {blog_content}
        """

        # Get the translated text as a simple string
        translated_content = self.llm.invoke(translation_prompt).content

        # Update the content of the existing blog in the state
        state["blog"]["content"] = translated_content # pyright: ignore[reportIndexIssue]

        return state
        
    ## Rout function
    def route(self, state: BlogState):
        current_language = str(state.get("current_language", "")).strip().lower()
        print(current_language)
        return {"current_language": current_language}
    
    
    ## Route decision  
    def route_decision(self,state:BlogState):
        """Rout the content to the respective translate function
        """
        
        if state['current_language'] =="arabic":
            return "arabic"
        elif state['current_language'] =="french":
            return "french"
        else:
            return state['current_language']
                    