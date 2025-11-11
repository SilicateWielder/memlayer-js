from sqlalchemy.orm import Session
from db.models import Conversation, Interaction, EpisodicMemory
from core.llm import llm_interface

class ConsolidationEngine:
    def consolidate_interaction(
        self,
        db: Session,
        conversation_id: str,
        user_id: str,
        user_message: str,
        assistant_message: str,
    ) -> Interaction:
        """
        Processes a single interaction and stores it, along with its episodic memory.
        """
        # 1. Find or create the conversation
        conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
        if not conversation:
            conversation = Conversation(id=conversation_id, user_id=user_id)
            db.add(conversation)
            # We need to commit here to ensure the conversation exists before linking to it
            db.commit()
            db.refresh(conversation)

        # 2. Create the Interaction record
        interaction = Interaction(
            conversation_id=conversation.id,
            user_id=user_id,
            user_message=user_message,
            assistant_message=assistant_message,
        )
        db.add(interaction)
        # Commit to get an ID for the interaction
        db.commit()
        db.refresh(interaction)

        # 3. Create the Episodic Memory
        # The content for the memory is a simple concatenation for now
        memory_content = f"User: {user_message}\nAssistant: {assistant_message}"
        
        # 4. Generate the embedding
        embedding = llm_interface.get_embedding(memory_content)

        if embedding:
            episodic_memory = EpisodicMemory(
                interaction_id=interaction.id,
                content=memory_content,
                embedding=embedding,
                timestamp=interaction.timestamp,
                importance=0.5, # Default importance
            )
            db.add(episodic_memory)
            # Commit everything
            db.commit()
            db.refresh(interaction)
        
        return interaction

# A global instance for easy access
consolidation_engine = ConsolidationEngine()