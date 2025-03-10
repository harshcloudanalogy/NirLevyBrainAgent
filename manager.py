
import time
from typing import Dict, List, Any
from collections import deque



class Manager:
    def __init__(self):
        # Dictionary to store queues for each robot, using deque for efficient popping
        self.robot_queues: Dict[str, deque] = {}
        # Robot status with capabilities and availability
        self.robot_status: Dict[str, Dict[str, Any]] = {
            "robot_1": {"available": True, "capabilities": ["navigate", "pick_item"], "location": "aisle_1"},
            "robot_2": {"available": True, "capabilities": ["restock_shelf", "report_status"], "location": "aisle_5"},
            "robot_default": {"available": True, "capabilities": ["general"], "location": "store_center"}
        }
        print("Manager initialized with robots:", list(self.robot_status.keys()))

    def dispatch_plans(self, refined_plans: List[Dict[str, Any]]) -> None:
        """
        Receive refined plans from the Brain module and dispatch them to appropriate robots.
        Plans are assumed to be text-based.
        """
        if not refined_plans:
            print("No refined plans received for dispatch.")
            return

        for plan in refined_plans:
            try:
                robot_id = self.determine_robot(plan)
                if robot_id:
                    self.enqueue_plan(robot_id, plan)
                    print(f"Plan {plan['plan_id']} dispatched to {robot_id}")
                else:
                    print(f"Warning: No suitable robot found for plan {plan['plan_id']}")
            except Exception as e:
                print(f"Error dispatching plan {plan.get('plan_id', 'unknown')}: {e}")


    def determine_robot(self, plan: Dict[str, Any]) -> str:
        """
        Determine the best robot for a text-based plan based on actions and context.
        Returns robot_id or None if no suitable robot is available.
        """
        actions = plan.get("actions", [])
        context = plan.get("context", {})

        # Check each robot's capabilities against the plan's actions
        for robot_id, status in self.robot_status.items():
            if status["available"]:
                # Check if robot capabilities match any required actions
                if "general" in status["capabilities"] or any(action in status["capabilities"] for action in actions):
                    # Additional check for location if provided in context
                    if "location" in context:
                        if context["location"] == status["location"] or robot_id == "robot_default":
                            return robot_id
                    else:
                        return robot_id

        # Fallback to default robot if available and no specific match found
        if self.robot_status["robot_default"]["available"]:
            return "robot_default"

        print(f"No available robot for plan {plan['plan_id']} with actions {actions}")
        return None

    def enqueue_plan(self, robot_id: str, plan: Dict[str, Any]) -> None:
        """
        Add a plan to the specified robot's queue.
        """
        if robot_id not in self.robot_queues:
            self.robot_queues[robot_id] = deque()
        self.robot_queues[robot_id].append(plan)
        # Mark robot as busy if this is the first task in its queue
        if len(self.robot_queues[robot_id]) == 1:
            self.robot_status[robot_id]["available"] = False

    def execute_robot_queues(self) -> None:
        """
        Execute all queued plans for each robot, ensuring careful task execution.
        """
        for robot_id, queue in list(self.robot_queues.items()):
            while queue:
                try:
                    task = queue.popleft()
                    self.send_to_robot(robot_id, task)
                    # Simulate task execution (replace with real robot feedback in production)
                    time.sleep(1)  # Placeholder for execution time
                    print(f"Task {task['plan_id']} completed by {robot_id}")
                except Exception as e:
                    print(f"Error executing task {task.get('plan_id', 'unknown')} on {robot_id}: {e}")
                finally:
                    # Mark robot as available and clean up if queue is empty
                    if not queue:
                        self.robot_status[robot_id]["available"] = True
                        del self.robot_queues[robot_id]



    def send_to_robot(self, robot_id: str, task: Dict[str, Any]) -> None:
        """
        Simulate sending a task to a robot. Replace with actual robot communication in production.
        """
        actions = task.get("actions", [])
        print(f"Sending task {task['plan_id']} to {robot_id} with actions: {actions}")
        # Placeholder for actual robot communication (e.g., API call or hardware int