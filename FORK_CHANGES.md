# Fork Integration Changelog

This file tracks all changes made to integrate features from the `sora2api_beta-main` fork.
Use this when merging upstream updates to avoid losing customizations.

---

## Date: 2026-01-19

### Files Added (New - No Conflict Risk)

| File/Folder | Source | Description |
|-------------|--------|-------------|
| `chatgpt_token_extractor/` | Fork | Chrome extension for token extraction |
| `local_proxy_server.py` | Fork | CORS proxy for Chrome extension |
| `scripts/examples_async_video.py` | Fork | Async video generation example |
| `scripts/verify_async.py` | Fork | Async API verification script |
| `scripts/debug_db.py` | Fork | Database debug utility |
| `scripts/fix_db_schema.py` | Fork | Schema migration helper |

### Files Modified (Merge Carefully)

| File | Changes Made | How to Merge Upstream |
|------|--------------|----------------------|
| `src/api/routes.py` | Added `X-Sora2-Async` header, `/v1/tasks/{task_id}` endpoint | Keep our async additions, merge other changes |
| `src/core/database.py` | Added `tasks` table and related methods | Add task table code to new version |
| `src/services/generation_handler.py` | Added `submit_background_task()` method | Add background task method to new version |
| `src/services/load_balancer.py` | Added round-robin mode, usage caching | Add round-robin methods to new version |
| `src/api/__init__.py` | Added sentinel router (if integrated) | Check if needed |

### Translation Notes

The following files were previously translated to English and should **NOT** be overwritten by upstream:

- `static/manage.html` - Management panel UI
- `static/login.html` - Login page UI  
- `static/generate.html` - Generation panel UI

When merging upstream, compare changes but keep English translations.

---

## Merge Checklist (For Future Upstream Updates)

1. **Backup current project** before merging
2. **Check FORK_CHANGES.md** for our customizations
3. **Diff new files** against our modified versions:
   - `src/api/routes.py`
   - `src/core/database.py`
   - `src/services/generation_handler.py`
   - `src/services/load_balancer.py`
4. **Keep translations** in `static/*.html` files
5. **Keep added folders** that don't conflict:
   - `chatgpt_token_extractor/`
   - `scripts/`
   - `local_proxy_server.py`
6. **Test after merge** to ensure everything works

---

## Detailed Change Log

### `src/api/routes.py`

**Added imports:**
```python
from fastapi import Header
```

**Added to `create_chat_completion` function:**
- New parameters: `x_sora2_async` and `x_sora2_no_stream` headers
- Async task submission block (lines ~141-169)

**Added new endpoint:**
```python
@router.get("/v1/tasks/{task_id}")
async def get_task_status(task_id: str, api_key: str = Depends(verify_api_key_header)):
    # Returns task status, progress, result_urls
```

---

### `src/core/database.py`

**Added table:**
```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT UNIQUE NOT NULL,
    status TEXT DEFAULT 'pending',
    progress REAL DEFAULT 0,
    model TEXT,
    prompt TEXT,
    result_urls TEXT,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

**Added methods:**
- `create_task(task_id, model, prompt)`
- `get_task(task_id)`
- `update_task_status(task_id, status, progress, result_urls, error_message)`

---

### `src/services/generation_handler.py`

**Added method:**
```python
async def submit_background_task(self, model, prompt, image=None, video=None, remix_target_id=None) -> str:
    # Creates task in DB
    # Starts background generation
    # Returns task_id immediately
```

---

### `src/services/load_balancer.py`

**Added attributes:**
```python
self._usage_cache: Dict[int, int] = {}
self._usage_lock = asyncio.Lock()
```

**Added methods:**
- `_get_cached_usage(token_id, db_usage)`
- `sync_usage_cache_from_db()`
- `reset_usage_cache()`
- `_select_round_robin(available_tokens, for_image, for_video)`
- `_async_increment_db_usage(token_id)`
