import json
from typing import Annotated, List, Literal
import networkx as nx


class DataManager:
    """
    DataManager is responsible for handling store-related data, including:
    - Retrieving and updating store context from a JSON file.
    - Constructing a knowledge graph for efficient product retrieval.
    """

    def __init__(self, context_file="/home/clpud/Levy_Brain_Agent/store_files/store_context.json"):
        """
        Initializes the DataManager with a default store context file.

        Args:
            context_file (str): The file path to the store context JSON file.
        """
        self.context_file = context_file



    def get_store_context(self):  # need_to_search: Literal["yes", "no"]
        """
        Retrieves the current store context data from the JSON file.

        Returns:
            dict: The store context containing aisles, shelves, and product details.
                  Returns an empty dictionary in case of an error.
        """
        try:
            with open(self.context_file, "r") as file:
                context = json.load(file)
            return context
        except Exception as e:
            print(f"Error loading store context: {e}")
            return {}



    def update_store_context(self, new_context: Annotated[str, "The new context to update in the store file."]):
        """
        Updates the store context with new data.

        Args:
            new_context (str): The updated store context in JSON format.

        Returns:
            str: Success or failure message.
        """
        try:
            with open(self.context_file, "w") as file:
                json.dump(new_context, file)
            return "Store context updated successfully"
        except Exception as e:
            return "Error updating store context, please try again"




    def get_the_knowledge_graph(self, data_file):
        """
        Generates a knowledge graph representation of the store context.

        Args:
            data_file (str): Path to the store context JSON file.

        Returns:
            networkx.DiGraph: The constructed knowledge graph of the store.
        """
        try:
            with open(self.context_file, "r") as f:
                data = json.load(f)

            # Create a directed graph
            G = nx.DiGraph()

            # Build the knowledge graph from store data
            G = self.build_knowledge_graph(G, data)

            return G
        except Exception as e:
            print(f"Error creating knowledge graph: {e}")
            return None



    @staticmethod
    def build_knowledge_graph(G, data):
        """
        Constructs a knowledge graph of the store layout using NetworkX.

        Args:
            G (networkx.DiGraph): An empty directed graph.
            data (dict): The store context data.

        Returns:
            networkx.DiGraph: The constructed knowledge graph.
        """
        for aisle, aisle_info in data["aisles"].items():
            # Add aisle as a node
            G.add_node(aisle, type="aisle", location=aisle_info["location"])

            # Iterate through each shelf in the aisle
            for side, shelves in aisle_info["shelves"].items():
                for shelf in shelves:
                    shelf_node = f"{aisle}_shelf_{shelf['shelf_number']}_{side}"
                    G.add_node(shelf_node, type="shelf", number=shelf["shelf_number"], side=side)
                    G.add_edge(aisle, shelf_node)  # Connect aisle to shelf

                    # Add category node and link it to the shelf
                    category = shelf["category"]
                    category_node = f"{aisle}_{category}"
                    G.add_node(category_node, type="category", name=category)
                    G.add_edge(shelf_node, category_node)

                    # Iterate through subcategories
                    for subcategory, products in shelf["subcategories"].items():
                        subcategory_node = f"{aisle}_{subcategory}"
                        G.add_node(subcategory_node, type="subcategory", name=subcategory)
                        G.add_edge(category_node, subcategory_node)

                        # Add each product under its respective subcategory
                        for product in products:
                            product_node = product["product"]
                            G.add_node(
                                product_node,
                                type="product",
                                stock=product["stock"],
                                reorder_threshold=product["reorder_threshold"],
                                aisle=aisle,
                                shelf_number=shelf["shelf_number"],
                                shelf_side=side,
                                category=category,
                                subcategory=subcategory
                            )
                            G.add_edge(subcategory_node, product_node)  # Link product to subcategory

        return G
