from enum import Enum

class ChatLength(Enum):
    SHORT = "Short (5 replies)"
    MEDIUM = "Medium (10 replies)"
    LONG = "Long (20 replies)"

    def to_int(self) -> int:
        return {
            ChatLength.SHORT: 5,
            ChatLength.MEDIUM: 10,
            ChatLength.LONG: 20,
        }[self]

def get_current_chat_language():
    return "Spanish"
