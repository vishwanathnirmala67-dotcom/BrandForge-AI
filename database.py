import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "brandforge.db"


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables() -> None:
    conn = connect()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            creator_name TEXT NOT NULL,
            project_name TEXT NOT NULL,
            data_json TEXT NOT NULL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    conn.close()


def save_project(project: Dict[str, Any]) -> int:
    profile = project.get("profile", {}) or {}
    positioning = project.get("positioning", {}) or {}

    creator_name = profile.get("name") or "Creator"
    project_name = (
        positioning.get("brand_name")
        or positioning.get("niche")
        or "Personal Brand"
    )

    conn = connect()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO projects (creator_name, project_name, data_json) VALUES (?, ?, ?)",
        (
            creator_name,
            project_name,
            json.dumps(project, ensure_ascii=False),
        ),
    )
    project_id = int(cur.lastrowid)
    conn.commit()
    conn.close()
    return project_id


def get_project(project_id: int) -> Optional[Dict[str, Any]]:
    conn = connect()
    row = conn.execute(
        "SELECT id, creator_name, project_name, data_json, created_at FROM projects WHERE id = ?",
        (project_id,),
    ).fetchone()
    conn.close()

    if row is None:
        return None

    result = json.loads(row["data_json"])
    result["project_id"] = row["id"]
    result["created_at"] = row["created_at"]
    return result


def list_projects() -> List[Dict[str, Any]]:
    conn = connect()
    rows = conn.execute(
        "SELECT id, creator_name, project_name, created_at FROM projects ORDER BY id DESC"
    ).fetchall()
    conn.close()
    return [dict(row) for row in rows]


def delete_project(project_id: int) -> bool:
    conn = connect()
    cur = conn.cursor()
    cur.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
