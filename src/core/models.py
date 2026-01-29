"""Data models"""
from datetime import datetime
from typing import Optional, List, Union
from pydantic import BaseModel

class Token(BaseModel):
    """Token model"""
    id: Optional[int] = None
    token: str
    email: str
    name: Optional[str] = ""
    st: Optional[str] = None
    rt: Optional[str] = None
    client_id: Optional[str] = None
    proxy_url: Optional[str] = None
    remark: Optional[str] = None
    expiry_time: Optional[datetime] = None
    is_active: bool = True
    cooled_until: Optional[datetime] = None
    created_at: Optional[datetime] = None
    last_used_at: Optional[datetime] = None
    use_count: int = 0
    # Subscription Info
    plan_type: Optional[str] = None  # Account type, e.g. chatgpt_team
    plan_title: Optional[str] = None  # Plan name, e.g. ChatGPT Business
    subscription_end: Optional[datetime] = None  # Subscription end time
    # Sora2 Support Info
    sora2_supported: Optional[bool] = None  # Is Sora2 supported
    sora2_invite_code: Optional[str] = None  # Sora2 invite code
    sora2_redeemed_count: int = 0  # Sora2 used count
    sora2_total_count: int = 0  # Sora2 total count
    # Sora2 Remaining Count
    sora2_remaining_count: int = 0  # Sora2 remaining available count
    sora2_cooldown_until: Optional[datetime] = None  # Sora2 cooldown time
    # Feature Toggles
    image_enabled: bool = True  # Enable image generation
    video_enabled: bool = True  # Enable video generation
    # Concurrency Limits
    image_concurrency: int = -1  # Image concurrency limit, -1 for no limit
    video_concurrency: int = -1  # Video concurrency limit, -1 for no limit
    # Expiry Flag
    is_expired: bool = False  # Is token expired (401 token_invalidated)

class TokenStats(BaseModel):
    """Token statistics"""
    id: Optional[int] = None
    token_id: int
    image_count: int = 0
    video_count: int = 0
    error_count: int = 0  # Historical total errors (never reset)
    last_error_at: Optional[datetime] = None
    today_image_count: int = 0
    today_video_count: int = 0
    today_error_count: int = 0
    today_date: Optional[str] = None
    consecutive_error_count: int = 0  # Consecutive errors for auto-disable

class Task(BaseModel):
    """Task model"""
    id: Optional[int] = None
    task_id: str
    token_id: int
    model: str
    prompt: str
    status: str = "processing"  # processing/completed/failed
    progress: float = 0.0
    result_urls: Optional[str] = None  # JSON array
    error_message: Optional[str] = None
    retry_count: int = 0  # 当前重试次数
    created_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class RequestLog(BaseModel):
    """Request log model"""
    id: Optional[int] = None
    token_id: Optional[int] = None
    task_id: Optional[str] = None  # Link to task for progress tracking
    operation: str
    request_body: Optional[str] = None
    response_body: Optional[str] = None
    status_code: int  # -1 for in-progress
    duration: float  # -1.0 for in-progress
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class AdminConfig(BaseModel):
    """Admin configuration"""
    id: int = 1
    admin_username: str  # Read from database, initialized from setting.toml on first startup
    admin_password: str  # Read from database, initialized from setting.toml on first startup
    api_key: str  # Read from database, initialized from setting.toml on first startup
    error_ban_threshold: int = 3
    task_retry_enabled: bool = True  # 是否启用任务失败重试
    task_max_retries: int = 3  # 任务最大重试次数
    auto_disable_on_401: bool = True  # 遇到401错误自动禁用token
    updated_at: Optional[datetime] = None

class ProxyConfig(BaseModel):
    """Proxy configuration"""
    id: int = 1
    proxy_enabled: bool  # Read from database, initialized from setting.toml on first startup
    proxy_url: Optional[str] = None  # Read from database, initialized from setting.toml on first startup
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class WatermarkFreeConfig(BaseModel):
    """Watermark-free mode configuration"""
    id: int = 1
    watermark_free_enabled: bool  # Read from database, initialized from setting.toml on first startup
    parse_method: str  # Read from database, initialized from setting.toml on first startup
    custom_parse_url: Optional[str] = None  # Read from database, initialized from setting.toml on first startup
    custom_parse_token: Optional[str] = None  # Read from database, initialized from setting.toml on first startup
    fallback_on_failure: bool = True  # Auto fallback to watermarked video on failure, default True
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CacheConfig(BaseModel):
    """Cache configuration"""
    id: int = 1
    cache_enabled: bool  # Read from database, initialized from setting.toml on first startup
    cache_timeout: int  # Read from database, initialized from setting.toml on first startup
    cache_base_url: Optional[str] = None  # Read from database, initialized from setting.toml on first startup
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class GenerationConfig(BaseModel):
    """Generation timeout configuration"""
    id: int = 1
    image_timeout: int  # Read from database, initialized from setting.toml on first startup
    video_timeout: int  # Read from database, initialized from setting.toml on first startup
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class TokenRefreshConfig(BaseModel):
    """Token refresh configuration"""
    id: int = 1
    at_auto_refresh_enabled: bool  # Read from database, initialized from setting.toml on first startup
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class CallLogicConfig(BaseModel):
    """Call logic configuration"""
    id: int = 1
    call_mode: str = "default"  # "default" or "polling"
    polling_mode_enabled: bool = False  # Read from database, initialized from setting.toml on first startup
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class PowProxyConfig(BaseModel):
    """POW proxy configuration"""
    id: int = 1
    pow_proxy_enabled: bool = False  # Whether to enable POW proxy
    pow_proxy_url: Optional[str] = None  # POW proxy URL (e.g., http://127.0.0.1:7890)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

# API Request/Response models
class ChatMessage(BaseModel):
    role: str
    content: Union[str, List[dict]]  # Support both string and array format (OpenAI multimodal)

class ChatCompletionRequest(BaseModel):
    model: str
    messages: List[ChatMessage]
    image: Optional[str] = None
    video: Optional[str] = None  # Base64 encoded video file
    remix_target_id: Optional[str] = None  # Sora share link video ID for remix
    stream: bool = False
    max_tokens: Optional[int] = None

class ChatCompletionChoice(BaseModel):
    index: int
    message: Optional[dict] = None
    delta: Optional[dict] = None
    finish_reason: Optional[str] = None

class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[ChatCompletionChoice]
