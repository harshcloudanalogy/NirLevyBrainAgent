# Import necessary modules and classes from different parts of the system
from utils.logger import setup_logging  # Logging setup for debugging and tracking system events
from utils.data_manager import DataManager  # Handles data storage and retrieval
from brain import Brain  # Core processing unit responsible for decision-making
from manager import Manager  # Manages agents and system operations
from vlm_agent import VLMTextAgent, VLMImageAgent  # Agents for text and image processing
from input_module import InputModule  # Handles input processing from commands and images


def system_startup():
    """
    Initializes and starts up the system by setting up logging, 
    initializing core components (Brain, Manager, and InputModule),
    and preparing the system for execution.
    
    Returns:
        brain (Brain): The central decision-making unit.
        manager (Manager): The system manager responsible for task delegation.
        agents (InputModule): Handles text and image input processing.
    """

    # Set up logging for the system (to track operations and debug issues)
    setup_logging()

    # Initialize the data manager to handle data storage and retrieval
    data_manager = DataManager()

    # Initialize the Brain module, which processes and refines plans
    brain = Brain(data_manager)

    # Create the Manager, responsible for managing and dispatching tasks
    manager = Manager()

    # Initialize the input module, which processes user commands and images
    agents = InputModule()

    # Print a message indicating that the system has started successfully
    print("System startup complete.")

    # Return the core system components for further use
    return brain, manager, agents
