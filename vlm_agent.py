"""
vlm_agent.py

This file contains two agents:
1. **VLMTextAgent**: Processes text-based commands and generates a structured execution plan.
2. **VLMImageAgent**: Processes images along with commands and generates a structured execution plan.

Both agents use Groq's Llama-3 models for inference:
- **Text**: `llama-3.3-70b-versatile`
- **Image**: `llama-3.2-11b-vision-preview`

Each agent outputs a plan containing:
- A unique `plan_id`
- The `source` (text or image)
- A `timestamp`
- A list of actions to execute

The plans are passed to the `Brain` for further processing.
"""
import json
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool, create_schema_from_function, convert_runnable_to_tool 
from langchain.agents import create_openai_tools_agent
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig, Runnable
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import List, Optional
import datetime
import os
import base64
import uuid
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Define a Pydantic model for structured plan generation
class Plans(BaseModel):
    """Schema for structured task execution plans."""
    plan: List[str] = Field(..., description="List of steps to execute the task.")



# Define a model for casual responses
class CasualAnswer(BaseModel):
    """Schema for normal responses that do not include plans."""
    msg: str = Field(..., description="Casual answer to the manager.")



class VLMTextAgent:
    """
    Text-based agent that processes commands and generates execution plans.
    Uses Groq's Llama-3.3-70b-versatile model for structured outputs.
    """
    
    def __init__(self):
        self.prompt = (
            """
            You are a powerful brain module of a robot operating in a store.
            - For casual answers, use `CasualAnswer`.
            - For making execution plans, use `Plans`.
            - You will receive a command from the Manager and generate a structured execution plan.
            """
        )
        
        self.tools = [Plans, CasualAnswer]
        self.llm = ChatGroq(temperature=0, model_name="llama-3.3-70b-versatile", max_retries=2)
        self.structured_output = self.llm.bind_tools(self.tools)
        self.agent_type = "text"
    
    def invoke(self, command: str) -> dict:
        """
        Processes a command and generates an execution plan.
        """
        today_time_date = datetime.datetime.utcnow().isoformat()
        inputs = [SystemMessage(content=self.prompt + f" Today's datetime is {today_time_date}")]
        inputs.append(HumanMessage(content=command))

        result = self.structured_output.invoke(inputs)
        output = result.tool_calls
        print(output)

        no_plan_executed = True
        if output[0]["name"] == "CasualAnswer":
            return output[0]["args"]["msg"], no_plan_executed
        
        else:
            list_of_plan = output[0]["args"]["plan"]
            no_plan_executed = False
            plan = {
                "plan_id": str(uuid.uuid4()),
                "source": self.agent_type,
                "timestamp": today_time_date,
                "actions": list_of_plan
            }, no_plan_executed
            return plan






class Plans_Image(BaseModel):
    '''Step by step plan in a list format ['', '', '' ]'''
    plan: List[str] = Field(..., description="List of plans what to do or how to execute the task.")


class VLMImageAgent:
    """
    Image-based agent that processes an image along with a command and generates an execution plan.
    Uses Groq's Llama-3.2-11b-vision-preview model for structured outputs.
    """
    
    def __init__(self):
        self.agent_type = "image"
        self.prompt = """
            You are a powerful brain module of a robot operating in a store.
            - For making execution plans, use `Plans`.
            - You will receive a command along with an image and generate a structured execution plan. How to complete that task step by step.
            """.strip()
        
        self.llm = ChatGroq(
                            model="llama-3.2-90b-vision-preview",
                                temperature=0.0,
                                max_retries=2,
                            ).bind_tools([Plans_Image])
    

    def get_image(self, image_path: str) -> str:
        """Encodes an image file as a base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def encode_image(self, image_path: str) -> str:
        """Returns a base64-encoded string representation of an image."""
        return self.get_image(image_path)
    
    def invoke(self, image_path: Optional[str] = None, image_url: Optional[str] = None, image_bytes: Optional[str] = None) -> dict:
        """
        Processes an image along with a command and generates an execution plan.
        """
        
        if image_path:
            base64_image = self.encode_image(image_path)
            url = f"data:image/jpeg;base64,{base64_image}"
        elif image_bytes:
            url = f"data:image/jpeg;base64,{image_bytes}"
        else:
            url = image_url
        
        cmnd = "Check any task given in the Image like robot will send the image of store you have to findout what we have to do next. Make a plan in a list format step by step."
        human = HumanMessage(content=[
            {"type": "text", "text": f"{self.prompt}. The task is: {cmnd}"},
            {"type": "image_url", "image_url": {"url": url}}
        ])

        
        today_time_date = datetime.datetime.utcnow().isoformat()
        messages = []
        messages.append(human)
        result = self.llm.invoke(messages)
        
        print("result", result)
        try:
            llm_response = result.content
            # Step 1: Extract the JSON portion (between { and })
            start = llm_response.find('{')
            end = llm_response.rfind('}') + 1
            json_str = llm_response[start:end]


            # Step 2: Parse the JSON string into a Python dictionary

            data = json.loads(json_str)

            # Step 3: Access the 'plan' list from the 'parameters' field
            plan_parameters = data['parameters']['plan']

        except:
            plan_parameters = result.tool_calls[0]["args"]["plan"]
        
        plan = {
            "plan_id": str(uuid.uuid4()),
            "source": self.agent_type,
            "timestamp":today_time_date ,
            "actions": plan_parameters
        }
        return plan, False


