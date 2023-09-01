from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from pydantic import BaseModel

from llmserver.models.manager import ModelManager
from llmserver.core.ServiceProvider import SingletonServiceProvider
import time

from llmserver.repository.HuggingFaceModelRepository import HuggingFaceModelRepository


class Question(BaseModel):
    model: str
    prompt: str


class Reply(BaseModel):
    time: float
    message: str


modelRouter = APIRouter()

provider = SingletonServiceProvider.get_instance()


@modelRouter.get("/models")
def get_models(modelManager: ModelManager = Depends(lambda: provider.resolve(ModelManager))):
    return {"models": modelManager.models}


#
# @modelRouter.get("/huggingface-models-in-download")
# def get_queued_models(hfRepository: HuggingFaceModelRepository = provider.resolve(HuggingFaceModelRepository)):
#     return {"models": hfRepository.queue}


@modelRouter.post("/query")
def ask_model(question: Question,
              modelManager: ModelManager = Depends(lambda: provider.resolve(ModelManager))):
    if question.model not in modelManager.models:
        raise HTTPException(status_code=404, detail="Model not found")

    model = modelManager.getModel(question.model)
    modelManager.schedule(question.model)

    elapsedTime = time.time()
    reply = model.generate(question.prompt)
    elapsedTime = time.time() - elapsedTime

    return Reply(time=elapsedTime, message=reply)
