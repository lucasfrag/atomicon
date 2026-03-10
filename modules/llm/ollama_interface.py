import ollama


class OllamaLLM:

    def __init__(self, model="llama3.1:8b"):

        self.model = model

    def generate(self, prompt):

        response = ollama.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )

        return response["message"]["content"]