from pydantic import BaseModel
import sqlite3


class Conversation(BaseModel):
    id: str
    summary: str
    messages: list


class ConversationStorage:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.create_tables()

    def create_tables(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                summary TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT,
                message TEXT,
                position INTEGER,
                FOREIGN KEY (conversation_id) REFERENCES conversations (id)
            )
        ''')
        conn.commit()
        conn.close()

    def get_conversation(self, conversation_id: str, recent_history_length: int) -> Conversation:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT summary FROM conversations WHERE id=?", (conversation_id,))
        row = cursor.fetchone()
        if row is None:
            conn.close()
            return None

        summary = row[0]

        if recent_history_length > 0:
            cursor.execute(
                "SELECT message FROM messages WHERE conversation_id=? ORDER BY position DESC LIMIT ?",
                (conversation_id, recent_history_length)
            )
        else:
            cursor.execute("SELECT message FROM messages WHERE conversation_id=?", (conversation_id,))

        messages = [row[0] for row in cursor.fetchall()]
        conn.close()

        return Conversation(id=conversation_id, summary=summary, messages=messages)

    def save_conversation(self, conversation: Conversation, recent_history_length: int):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO conversations (id, summary) VALUES (?, ?)",
                       (conversation.id, conversation.summary))
        conn.commit()

        if recent_history_length == 0:
            cursor.execute("DELETE FROM messages WHERE conversation_id=?", (conversation.id,))
        else:
            messages_to_insert = conversation.messages[-recent_history_length:]
            cursor.execute("DELETE FROM messages WHERE conversation_id=?", (conversation.id,))
            cursor.executemany("INSERT INTO messages (conversation_id, message, position) VALUES (?, ?, ?)",
                               [(conversation.id, message, idx + 1) for idx, message in enumerate(messages_to_insert)])
        conn.commit()
        conn.close()
