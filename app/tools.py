def rag_tool(question, context):
    question = question.lower()
    context = context.lower()

    for line in context.split("."):
        if any(word in line for word in question.split()):
            return line.strip()

    return "❌ Sorry, I could not find this information in the uploaded document."
