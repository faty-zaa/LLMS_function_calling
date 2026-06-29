from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class Functions:

        data: Dict[str, Any]
        
            # the name of the function
        @property
        def name(self) -> str:
            return self.data['name']
        
            # the description (add it to the prompt)
        @property
        def description(self) -> str:
            return self.data["description"]
        
            # parameters, should add them to fsm dynamically
        @property
        def parameters(self) -> Dict[str, str]:
            return {
            key: value['type']
            for key, value in self.data['parameters'].items()
            }
    
        
    