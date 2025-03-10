from fastapi import APIRouter
from input_module import InputModule
from utils.data_manager import DataManager
from brain import Brain
from pydantic import BaseModel
from typing import Optional

# Initialize FastAPI router
router = APIRouter()

## Request model for agent creation
class AgentCreateRequest(BaseModel):
    manager_id: str  # Unique identifier for the manager
    command: Optional[str] = None  # Command to be processed
    image_url: Optional[str] = None # URL of the image to process
    image_path: Optional[str] = None  # Optional local image path
    image_bytes: Optional[bytes] = None  # Optional raw image bytes



# Initialize core components
agents = InputModule()
data_manager = DataManager()
brain = Brain(data_manager)

@router.post("/test_command")
async def create_agent(requests: AgentCreateRequest):
    """
    API endpoint to create an agent based on the given command and image input.
    
    Args:
    - requests (AgentCreateRequest): Request payload containing manager ID, command
    
    Returns:
    - dict: Status message and generated plan details.
    """
    command = requests.command

    # Generate plans using text and image agents
    plan, no_plan_executed = agents.process_text_requests(command)
    if no_plan_executed:
        msg = plan
        new_plans = msg

    else:
        # Combine all plans and process them with the brain agent
        new_plans = brain.process_plans(command=command, plans=plan)
    
    return {"status": "Agent created", "agent": new_plans}



@router.post("/test_robotImage")
async def create_agent(requests: AgentCreateRequest):
    """
    API endpoint to create an agent based on the given command and image input.
    
    Args:
    - requests (AgentCreateRequest): Request payload containing manager ID,image details.
    
    Returns:
    - dict: Status message and generated plan details.
    """

    image = requests.image_url

    # Generate plans using text and image agents
    plan, no_plan_executed = agents.process_image_input(image_url=image)
    if no_plan_executed:
        msg = plan
        new_plans = msg

    else:
        # Combine all plans and process them with the brain agent
        new_plans = brain.process_plans(plans=plan)
    
    return {"status": "Agent created", "agent": new_plans}