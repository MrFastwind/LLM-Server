from fastapi import APIRouter, Depends

from llmserver.core.ServiceProvider import SingletonServiceProvider
from llmserver.repository.ConversationRepository import ConversationRepository

conversationRouter = APIRouter()

provider = SingletonServiceProvider.get_instance()


@conversationRouter.get("/conversation/create")
async def get_conversation(
        conversationRepository: ConversationRepository = Depends(lambda: provider.resolve(ConversationRepository))):
    conversation = conversationRepository.get_conversation(id)
    return conversation


@conversationRouter.get("/conversation/{id}")
async def get_conversation(id: str, conversationRepository: ConversationRepository = Depends(lambda: provider.resolve(ConversationRepository))):
    conversation = conversationRepository.get_conversation(id)
    return conversation


@conversationRouter.post("/conversation/{id}/message")
async def add_message_to_conversation(id: str, message: str,
                                      conversationRepository: ConversationRepository = Depends(lambda: provider.resolve(ConversationRepository)),
                                      summarizer: HistorySummarizer = Depends()
                                      ):
    conversation = conversationRepository.get_conversation(id)
    conversation['messages'].append(message)
    summarized_history = summarizer.summarize_history(conversation, num_messages_to_exclude=1)
    conversation['history'] = summarized_history
    conversationRepository.save_conversation(conversation)
    return conversation
