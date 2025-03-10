"""This is a test file only to check the files response. Please ignore it"""

from utils.data_manager import DataManager
from input_module import InputModule
from brain import Brain


all_plans = [
        {
            "plan_id": "020ba06e-582d-4e93-ac76-559255cc9296",
            "source": "text",
            "timestamp": "2025-02-26T12:21:43.621037",
            "actions": "Based on the current inventory levels, I will create a restocking plan for aisle 5. \n\n1. Check the current stock levels of each product in aisle 5.\n2. Identify the products that are running low or are out of stock.\n3. Determine the quantity of each product that needs to be restocked.\n4. Create a list of the products that need to be restocked and the quantity needed.\n5. Prioritize the restocking of essential items and high-demand products.\n6. Schedule the restocking of aisle 5 for the next available time slot.\n7. Assign staff to restock the aisle and ensure that the products are properly shelved and faced.\n8. Monitor the restocking process and make any necessary adjustments.\n\nBy following this plan, we can ensure that aisle 5 is fully stocked and that customers have access to the products they need."
        },
        {
            "plan_id": "4d19fd17-01ae-4da8-a86b-6bc0105debe2",
            "source": "image",
            "timestamp": "2025-02-26T12:21:45.343149",
            "actions": "Here is the restocked plan for Aisle 5:\n\n**Step 1: Identify the Aisle**\n\n* Ensure Aisle 5 is clearly marked and easily accessible.\n* Verify that the aisle is not obstructed by any shelves or other obstacles.\n\n**Step 2: Gather Supplies**\n\n* Collect the necessary restocking items, including:\n\t+ Shelves or display units\n\t+ Products to be restocked\n\t+ Packaging materials (e.g., boxes, bags)\n\t+ Restocking equipment (e.g., pallet jack, forklift)\n\n**Step 3: Clear the Aisle**\n\n* Move any products or equipment that may be blocking the aisle.\n* Ensure the floor is clear of debris or obstacles.\n\n**Step 4: Restock Shelves**\n\n* Begin restocking shelves with the collected products.\n* Ensure products are facing the correct direction and are properly aligned.\n* Verify that shelves are not overstocked or understocked.\n\n**Step 5: Restock Display Units**\n\n* Restock display units with the collected products.\n* Ensure products are properly displayed and facing the correct direction.\n* Verify that display units are not overstocked or understocked.\n\n**Step 6: Restock Packaging Materials**\n\n* Restock packaging materials, including boxes and bags.\n* Ensure packaging materials are properly stored and easily accessible.\n\n**Step 7: Restock Equipment**\n\n* Restock restocking equipment, including pallet jacks and forklifts.\n* Ensure equipment is properly maintained and functioning correctly.\n\n**Step 8: Verify Restocking**\n\n* Verify that all shelves and display units are fully restocked.\n* Check that products are properly aligned and facing the correct direction.\n* Ensure that the aisle is clear of debris or obstacles.\n\n**Step 9: Record Restocking**\n\n* Record the restocking activity, including the quantity of products restocked and the time of restocking.\n* Update inventory records to reflect the restocked products.\n\nBy following these steps, Aisle 5 should be fully restocked and ready for customer use."
        }
    ]



data_manager = DataManager()

brain = Brain(data_manager)
new_plans = brain.process_plans(all_plans)
print(new_plans)