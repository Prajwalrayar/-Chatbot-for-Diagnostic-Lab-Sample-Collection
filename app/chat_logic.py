# def detect_intent(user_input: str):
#     text = user_input.lower()

#     if any(word in text for word in ["book", "test", "sample", "appointment"]):
#         return "BOOK_TEST"

#     return "RAG_QUERY"
def detect_intent(text: str):
    return "BOOK_TEST"
 