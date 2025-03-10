"""This is a test file only to check the files response. Please ignore it"""

from input_module import InputModule
from vlm_agent import VLMTextAgent

agents = InputModule()



command = "restock aisle 5"
image_url = "https://c8.alamy.com/comp/2BW0RXF/orlandoflusa-5420-aisles-at-a-publix-grocery-store-with-signs-above-each-aisle-designating-what-is-contained-in-the-aisle-2BW0RXF.jpg"

# text_plan = VLMTextAgent().invoke(command)

text_plan = InputModule().process_text_requests(command)
image_plan = InputModule().process_image_input(cmnd = command, image_url=image_url, image_bytes = None, image_path=None)


print("text_plan: ", text_plan)
print("\n\n\n")
print("image_plan:", image_plan)





