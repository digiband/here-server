# CLAUDE.md - Here Server

> **Project:** Backend server for the Here App - finds interesting info about nearby points of interest based on location.

---

## Shortcut Commands

| User Says | Claude Does |
|-----------|-------------|
| `tasks` | Check for hereserver tasks, claim one, and start working |

---

## Task Manager Workflow

We use a shared task manager. **Your project name:** `hereserver`

### Critical Rules

> **RULE 1: ALL responses go in the TICKET, not the console.**
> Never answer questions or give updates in chat - put everything in ticket comments.

> **RULE 2: Every response requires TWO commands:**
> ```bash
> python task_api.py comment <id> <claude_id> "Your message"
> python task_api.py update <id> --queue user
> ```
> **NEVER skip the second command.** Moving to user queue is how the user knows you responded.

> **RULE 3: Claude can ONLY move tasks to `user` queue.**
> Never close, test, or archive tasks - only the user can do that.

> **RULE 4: One task at a time.** Claim one, complete it, then claim the next.

### When User Says `tasks`

1. **List tasks:**
   ```bash
   python "C:\Users\digib\OneDrive\python projects\taskman\task_api.py" list --project hereserver
   ```

2. **Claim a task** (pick one, don't ask):
   ```bash
   python task_api.py claim <task_id> <claude_id>
   ```
   Claude ID format: `opus-hereserver-1` or `sonnet-hereserver-2`

3. **Work on the task**, then comment + move to user:
   ```bash
   python task_api.py comment <task_id> <claude_id> "Your response here"
   python task_api.py update <task_id> --queue user
   ```

4. **Create new task** (for follow-ups or discovered issues):
   ```bash
   python task_api.py create hereserver "title" ["description"]
   ```

### Running Task Manager

```bash
cd "C:\Users\digib\OneDrive\python projects\taskman"
python task_manager.py
```
Then open: http://localhost:8889

---

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | This file - project workflow instructions |
| `PROJECT.md` | Technical details, architecture, etc. |

---

## Project Overview

Here Server is the backend for the Here App. It will:
- Accept location data from the mobile app
- Find nearby points of interest
- Gather interesting information about those locations
- Return enriched location data to the app

---

## Project-Specific Instructions

(To be filled in as the project develops)
