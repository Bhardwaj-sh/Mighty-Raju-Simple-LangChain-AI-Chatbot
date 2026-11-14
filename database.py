import sqlite3
import uuid
from datetime import datetime
import os

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mighty_raju_chats.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables for conversations, messages, and projects."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Projects table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_saved INTEGER DEFAULT 0,
                project_id TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE SET NULL
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            )
        """)
        
        # Indexes for fast lookup
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_updated ON conversations(updated_at DESC)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_msg_conv ON messages(conversation_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_saved ON conversations(is_saved)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_conv_project ON conversations(project_id)")
        
        conn.commit()

# -------------------------------------------------------------------
# Conversation Operations
# -------------------------------------------------------------------
def create_conversation(title="New Conversation", project_id=None):
    conv_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (id, title, created_at, updated_at, is_saved, project_id) VALUES (?, ?, ?, ?, 0, ?)",
            (conv_id, title, now, now, project_id)
        )
        conn.commit()
    return conv_id

def get_conversation(conv_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, p.name as project_name 
            FROM conversations c 
            LEFT JOIN projects p ON c.project_id = p.id 
            WHERE c.id = ?
        """, (conv_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_conversation_title(conv_id, new_title):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
            (new_title, datetime.now().isoformat(), conv_id)
        )
        conn.commit()

def touch_conversation(conv_id):
    """Update updated_at timestamp to bring conversation to the top of recent chats."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE conversations SET updated_at = ? WHERE id = ?",
            (datetime.now().isoformat(), conv_id)
        )
        conn.commit()

def toggle_save_conversation(conv_id):
    """Toggle is_saved status (bookmark)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT is_saved FROM conversations WHERE id = ?", (conv_id,))
        row = cursor.fetchone()
        if row:
            new_val = 0 if row["is_saved"] else 1
            cursor.execute("UPDATE conversations SET is_saved = ? WHERE id = ?", (new_val, conv_id))
            conn.commit()
            return bool(new_val)
    return False

def set_conversation_saved(conv_id, is_saved: bool):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE conversations SET is_saved = ? WHERE id = ?", (1 if is_saved else 0, conv_id))
        conn.commit()

def set_conversation_project(conv_id, project_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE conversations SET project_id = ? WHERE id = ?", (project_id, conv_id))
        conn.commit()

def delete_conversation(conv_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
        cursor.execute("DELETE FROM conversations WHERE id = ?", (conv_id,))
        conn.commit()

def get_recent_conversations(limit=5):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, p.name as project_name 
            FROM conversations c 
            LEFT JOIN projects p ON c.project_id = p.id 
            ORDER BY c.updated_at DESC 
            LIMIT ?
        """, (limit,))
        return [dict(row) for row in cursor.fetchall()]

def get_all_conversations():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, p.name as project_name,
                   (SELECT COUNT(*) FROM messages WHERE conversation_id = c.id) as message_count
            FROM conversations c 
            LEFT JOIN projects p ON c.project_id = p.id 
            ORDER BY c.updated_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

def get_saved_conversations():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, p.name as project_name,
                   (SELECT COUNT(*) FROM messages WHERE conversation_id = c.id) as message_count
            FROM conversations c 
            LEFT JOIN projects p ON c.project_id = p.id 
            WHERE c.is_saved = 1 
            ORDER BY c.updated_at DESC
        """)
        return [dict(row) for row in cursor.fetchall()]

def search_conversations(query):
    if not query or not query.strip():
        return []
    pattern = f"%{query.strip()}%"
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT c.*, p.name as project_name,
                   (SELECT content FROM messages WHERE conversation_id = c.id AND content LIKE ? LIMIT 1) as matched_snippet
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id
            LEFT JOIN projects p ON c.project_id = p.id
            WHERE c.title LIKE ? OR m.content LIKE ?
            ORDER BY c.updated_at DESC
        """, (pattern, pattern, pattern))
        return [dict(row) for row in cursor.fetchall()]

# -------------------------------------------------------------------
# Message Operations
# -------------------------------------------------------------------
def add_message(conv_id, role, content):
    now = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (conversation_id, role, content, timestamp) VALUES (?, ?, ?, ?)",
            (conv_id, role, content, now)
        )
        cursor.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conv_id))
        conn.commit()

def get_messages(conv_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT role, content, timestamp FROM messages WHERE conversation_id = ? ORDER BY id ASC",
            (conv_id,)
        )
        return [{"role": row["role"], "content": row["content"], "timestamp": row["timestamp"]} for row in cursor.fetchall()]

def clear_conversation_messages(conv_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE conversation_id = ?", (conv_id,))
        cursor.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (datetime.now().isoformat(), conv_id))
        conn.commit()

def delete_last_assistant_message(conv_id):
    """Remove the most recent assistant message from the conversation (for regeneration)."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM messages 
            WHERE id = (
                SELECT id FROM messages 
                WHERE conversation_id = ? AND role = 'assistant' 
                ORDER BY id DESC LIMIT 1
            )
        """, (conv_id,))
        cursor.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (datetime.now().isoformat(), conv_id))
        conn.commit()

# -------------------------------------------------------------------
# Project Operations
# -------------------------------------------------------------------
def create_project(name):
    name = name.strip()
    if not name:
        return None
    proj_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO projects (id, name, created_at) VALUES (?, ?, ?)", (proj_id, name, now))
            conn.commit()
            return proj_id
        except sqlite3.IntegrityError:
            # Already exists
            cursor.execute("SELECT id FROM projects WHERE name = ?", (name,))
            row = cursor.fetchone()
            return row["id"] if row else None

def get_all_projects():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.*, COUNT(c.id) as chat_count
            FROM projects p
            LEFT JOIN conversations c ON p.id = c.project_id
            GROUP BY p.id
            ORDER BY p.name ASC
        """)
        return [dict(row) for row in cursor.fetchall()]

def get_project_conversations(project_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.*, p.name as project_name
            FROM conversations c
            JOIN projects p ON c.project_id = p.id
            WHERE c.project_id = ?
            ORDER BY c.updated_at DESC
        """, (project_id,))
        return [dict(row) for row in cursor.fetchall()]

def rename_project(project_id, new_name):
    new_name = new_name.strip()
    if not new_name:
        return False
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE projects SET name = ? WHERE id = ?", (new_name, project_id))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def delete_project(project_id):
    """Delete a project and unassign its conversations without deleting them."""
    with get_connection() as conn:
        cursor = conn.cursor()
        # Unassign conversations
        cursor.execute("UPDATE conversations SET project_id = NULL WHERE project_id = ?", (project_id,))
        # Delete project
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
        return True

# Initialize on module load
init_db()
