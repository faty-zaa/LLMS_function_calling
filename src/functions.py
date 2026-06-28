from typing import Dict, Any, List

class Functions:
    def __init__(self, data: List[Dict[str, Any]]):
        self.data: Dict[str, Any] = data
        
        # the name of the function
        self.name: str = data['name']
        
        # the description (add it to the prompt)
        self.description: str = data["description"]
        
        # parameters, should add them to fsm dynamically
        self.parameters: Dict[str, str] = {
            key: value['type']
            for key, value in data['parameters'].items()
        }
    
        
    