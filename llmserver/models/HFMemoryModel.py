from transformers import AutoTokenizer, AutoModel, GenerationConfig, AutoModelForCausalLM, Pipeline, pipeline

from llmserver.models.interfaces import Model
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
import faiss
import torch


class HFMemoryModel(Model):
    model: AutoModelForCausalLM | None = None
    tokenizer: AutoTokenizer | None = None
    memory = None

    def __init__(self, name: str, **kwargs):
        self.index = None
        self.nlp = None
        self.config = None
        self.model = None
        self.tokenizer = None
        self.memory = None
        self.name = name
        self.kwargs = kwargs

    def loadModel(self, memory_index_path=None):
        self.tokenizer = AutoTokenizer.from_pretrained(self.name)
        self.model = AutoModelForCausalLM.from_pretrained(self.name)
        # Define the pipeline
        self.nlp = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
        # Load the long-term memory
        self.index = faiss.read_index(memory_index_path)

    def unloadModel(self):
        del self.tokenizer
        del self.model

    def generate(self, prompt: str) -> str:
        if not self.model or not self.tokenizer:
            raise ValueError()
        # configure
        self.config = GenerationConfig(max_new_tokens=200)  # permit to change the response quality

        # query tokenization
        tokens = self.tokenizer(prompt, return_tensors="pt")  # pytorch like tensors

        # reply
        outputs = self.model.generate(**tokens)
        return str(self.tokenizer.batch_decode(
            outputs, skip_special_tokens=True
        ))  # special token are not needed for readable response

    def __del__(self):
        self.unloadModel()
        if self.tokenizer:
            del self.tokenizer
        if self.model:
            del self.model

    def retrieve_similar_examples(self, query, k=5):
        # Generate the embeddings for the query
        embeddings = self.nlp(query, return_tensors="pt")["input_ids"]
        # Convert the embeddings to a numpy array
        embeddings = embeddings.detach().numpy()
        # Perform a similarity search
        distances, indices = self.index.search(embeddings, k)
        # Retrieve the top-k most similar examples
        similar_examples = []
        for i in range(k):
            example = faiss.retrieve_example_by_index(indices[0][i])
            similar_examples.append(example)
        return similar_examples

    def generate_response(self, input_text, memory):
        # Retrieve the top-k most similar examples from the memory
        similar_examples = self.retrieve_similar_examples(memory)
        # Concatenate the input text and the similar examples
        prompt = input_text + "\n\n" + "\n\n".join(similar_examples)
        # Generate the response using the transformer model
        response = self.nlp(prompt, max_length=50)[0]["generated_text"]
        return response