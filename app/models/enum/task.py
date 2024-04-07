from enum import StrEnum

SUMMARISE_USAGE_COUNTER = 1
PRACTICE_USAGE_COUNTER = 5

class Task(StrEnum):
    SUMMARISE = "summarise"
    PRACTICE = "practice"
    
    def get_usage_value(self) -> int:
        """
        Calculates how much the usage of the user should be incremented in the user table.
        """
        counter = 0
        match self:
            case Task.SUMMARISE:
                return SUMMARISE_USAGE_COUNTER
            case Task.PRACTICE:
                return PRACTICE_USAGE_COUNTER
        return counter 
