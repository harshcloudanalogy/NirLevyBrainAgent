# Robotic Brain Application

## Description
This project is a Python-based AI agentic application designed to process user inputs (such as text or images) and generate actionable plans. It integrates multiple components, including data management, AI-powered agents, and a task execution manager to efficiently handle commands and automate tasks.

## Installation
Follow these steps to install dependencies and set up the project:

```sh
git clone https://github.com/harshcloudanalogy/NirLevyBrainAgent.git

pip install -r requirements.txt
```

## Project Structure and Files
Here’s a breakdown of the key files involved in the process:
- **Check the flowchart folder to check the flow diagram**

### **1. main.py**
- **Purpose:** Entry point of the application.
- **What it does:** Initializes the system and coordinates different modules.

### **2. routes.py**
- **Purpose:** Defines API routes for handling user commands or image requests.
- **What it does:** Routes user inputs appropriately to the corresponding processing modules.
- **Example Routes:**
  - `/test_robotimage` → Handles image-related tasks.
  - `/test_command` → Manages user commands.

### **3. input_module.py**
- **Purpose:** Handles initial processing of user inputs (text and images).
- **What it does:**
  - `TextAgent` → Processes text commands.
  - `ImageAgent` → Handles image inputs.

### **4. vlm_agent.py**
- **Purpose:** Manages vision and text-based processing.
- **What it does:**
  - `VLMImageAgent` → Analyzes images.
  - `VLMTextAgent` → Analyzes text.

### **5. brain.py**
- **Purpose:** Acts as the "brain" (Supervisor) of the system, responsible for decision-making and planning.
- **What it does:** Generates and refines plans using input data and context from the DataManager.

### **6. manager.py**
- **Purpose:** Executes the refined plans.
- **What it does:** Assigns tasks to robots or systems based on generated plans.

### **7. utils/data_manager.py**
- **Purpose:** Manages data storage and retrieval.
- **What it does:**
  - Provides access to the `store_context.json` file.
  - Fetches and updates store-related context.
  - **Includes a Knowledge Graph to store product information and locations**.

### **8. utils/logger.py**
- **Purpose:** Handles system logging.
- **What it does:** Logs system events, errors, and debugging information.

## Knowledge Graph Integration in DataManager
The **DataManager** builds a **knowledge graph** to store and retrieve information about products and their locations. This helps agents quickly fetch product details.

- **Graph Structure:**
  - **Aisles** → **Shelves** → **Categories** → **Subcategories** → **Products**
- **Usage:**
  - Agents can query the graph to find product locations and stock levels.
  - Enhances response accuracy and automation for inventory management.

## How It Works (System Flow)

1. **User Interaction:**
   - The process starts when a user runs `main.py` or sends a command.

2. **Routing (routes.py):**
   - The request is directed to the correct module (e.g., text processing, image analysis).

3. **Processing (input_module.py):**
   - Text and image inputs are analyzed and prepared for further action.

4. **Analysis (vlm_agent.py):**
   - AI models analyze the processed input to extract relevant insights.

5. **Planning (brain.py):**
   - The system generates an initial plan and retrieves additional context from `DataManager`.

6. **Execution (manager.py):**
   - The refined plan is assigned to the appropriate system or robot for execution.

## Running the Project
To start the application, run the following command:

For Windows (Command Prompt)
```sh
venv\Scripts\activate
```
For Ubuntu/Linux & macOS (Terminal)
```sh
source venv/bin/activate
```
```sh
{Env directory path}/myenv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

This will launch the application, making it accessible via API endpoints.


