from transformers import AutoTokenizer, AutoModel, GenerationConfig, AutoModelForCausalLM, Pipeline, pipeline

from llmserver.models.interfaces import Model
from llmserver.utils.logger import error


# class HuggingFaceLLModel(Model):
#     model: AutoModelForCausalLM | None = None
#     tokenizer: AutoTokenizer | None = None
#
#     def __init__(self, name: str, **kwargs):
#         self.config = None
#         self.model = None
#         self.tokenizer = None
#         self.name = name
#         self.kwargs = kwargs
#
#     def loadModel(self):
#         self.tokenizer = AutoTokenizer.from_pretrained(self.name)
#         self.model = AutoModelForCausalLM.from_pretrained(self.name)
#
#     def unloadModel(self):
#         del self.tokenizer
#         del self.model
#
#     def generate(self, prompt: str) -> str:
#         if not self.model or not self.tokenizer:
#             raise ValueError()
#         # configure
#         self.config = GenerationConfig(max_new_tokens=200)  # permit to change the response quality
#
#         # query tokenization
#         tokens = self.tokenizer(prompt, return_tensors="pt")  # pytorch like tensors
#
#         # reply
#         outputs = self.model.generate(**tokens)
#         return str(self.tokenizer.batch_decode(
#             outputs, skip_special_tokens=True
#         ))  # special token are not needed for readable response
#
#     def __del__(self):
#         self.unloadModel()
#         if self.tokenizer:
#             del self.tokenizer
#         if self.model:
#             del self.model


class HuggingFaceLLModel(Model):
    pipeline: Pipeline | None = None

    def __init__(self, name: str, config =None):
        self.config = config if config is not None else GenerationConfig(max_new_tokens=200)
        self.name = name

    def loadModel(self):
        self.pipeline = pipeline(model=self.name)

    def unloadModel(self):
        del self.pipeline

    def generate(self, prompt: str) -> str:
        if not self.pipeline:
            raise ValueError()
        # configure


        try:
            # Process the input data using the model pipeline
            processed_data = self.pipeline(prompt)[0]["generated_text"].strip()
            return processed_data
        except Exception as e:
            error(self.__class__.__name__,f"Error processing input: {e}")
            return "Error processing input"

    def __del__(self):
        self.unloadModel()
        if self.pipeline:
            del self.pipeline

