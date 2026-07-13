#!/usr/bin/env python3
"""
Quxuan Enterprise Shared Module 趣选企业级共享模块
Version: 2.1.0

提供所有Skill共用的基础设施：
- QuxuanConfig: 统一API配置
- QuxuanLogger: 结构化日志
- InputSanitizer: 输入清洗（防注入/XSS/命令注入）
- RateLimiter: 令牌桶限流
- SecurityHeaders: 安全工具
- PerformanceOptimizer: HTTP连接池+重试
- LLMCaller: 统一LLM调用（含重试、降级、日志）
- CrossPromotionEngine: 交叉推荐引流
- AtomicFileWriter: 原子文件写入
"""
import re, hashlib, time, os, logging, json, tempfile
from typing import Optional, Dict, Any, List, Tuple
from collections import defaultdict

import httpx


# ============================================================
# 1. 统一配置管理 Centralized Config
# ============================================================

class QuxuanConfig:
    """API提供商配置 - 集中管理，不散落在各文件"""
    PROVIDERS = {
        "dashscope": {
            "url": "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions",
            "default_model": "qwen-plus",
            "env_key": "DASHSCOPE_API_KEY",
        },
        "openai": {
            "url": "https://api.openai.com/v1/chat/completions",
            "default_model": "gpt-4o-mini",
            "env_key": "OPENAI_API_KEY",
        },
        "deepseek": {
            "url": "https://api.deepseek.com/v1/chat/completions",
            "default_model": "deepseek-chat",
            "env_key": "DEEPSEEK_API_KEY",
        },
    }

    # 版本信息
    VERSION = "2.1.0"
    USER_AGENT = f"Quxuan-Skill/{VERSION}"

    @classmethod
    def get_provider(cls, provider: str) -> Dict[str, str]:
        """获取provider配置，不存在时返回dashscope"""
        return cls.PROVIDERS.get(provider, cls.PROVIDERS["dashscope"])

    @classmethod
    def get_api_key(cls, provider: str) -> str:
        """从环境变量获取API Key"""
        cfg = cls.get_provider(provider)
        return os.environ.get(cfg["env_key"], "")

    @classmethod
    def validate_provider(cls, provider: str) -> bool:
        """校验provider是否合法"""
        return provider in cls.PROVIDERS


# ============================================================
# 2. 结构化日志 Structured Logger
# ============================================================

class QuxuanLogger:
    """统一日志 - 替代散落的print，支持结构化输出"""

    _initialized = False

    @classmethod
    def setup(cls, name: str = "quxuan", level: int = logging.INFO) -> logging.Logger:
        """初始化并返回logger"""
        if not cls._initialized:
            logging.basicConfig(
                level=level,
                format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            cls._initialized = True
        return logging.getLogger(name)

    @staticmethod
    def error(msg: str, exc: Optional[Exception] = None) -> None:
        """错误日志"""
        detail = f"{msg}: {exc}" if exc else msg
        logging.error(detail)

    @staticmethod
    def warn(msg: str) -> None:
        """警告日志"""
        logging.warning(msg)

    @staticmethod
    def info(msg: str) -> None:
        """信息日志"""
        logging.info(msg)


# ============================================================
# 3. 安全层 Security
# ============================================================

class InputSanitizer:
    """输入清洗器 - 防注入/XSS/恶意内容"""

    DANGEROUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',    # XSS
        r'javascript:',                   # JS注入
        r'on\w+\s*=',                     # 事件处理器注入
        r'eval\s*\(',                     # eval注入
        r'exec\s*\(',                     # exec注入
        r';\s*(rm|del|drop|truncate)',    # 命令注入
        r'\$\{.*?\}',                     # 模板注入
        r'__import__',                    # Python注入
        r'os\.system',                    # 系统调用
        r'subprocess',                    # 子进程
    ]

    MAX_INPUT_LENGTH = 5000

    @classmethod
    def sanitize(cls, text: str) -> str:
        """清洗输入，移除危险内容"""
        if not text:
            return ""
        text = text[:cls.MAX_INPUT_LENGTH]
        for pattern in cls.DANGEROUS_PATTERNS:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE | re.DOTALL)
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        return text.strip()

    @classmethod
    def validate(cls, text: str, field_name: str = "input") -> Tuple[bool, str]:
        """验证输入，返回(is_valid, error_message)"""
        if not text or not text.strip():
            return False, f"{field_name} 不能为空 / {field_name} cannot be empty"
        if len(text) > cls.MAX_INPUT_LENGTH:
            return False, f"{field_name} 超过最大长度{cls.MAX_INPUT_LENGTH} / exceeds max length"
        return True, ""


class RateLimiter:
    """基于内存的令牌桶限流器"""

    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        self.max_requests = max_requests
        self.window = window_seconds
        self._requests: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, key: str = "default") -> bool:
        now = time.time()
        self._requests[key] = [t for t in self._requests[key] if now - t < self.window]
        if len(self._requests[key]) >= self.max_requests:
            return False
        self._requests[key].append(now)
        return True

    def remaining(self, key: str = "default") -> int:
        now = time.time()
        active = [t for t in self._requests[key] if now - t < self.window]
        return max(0, self.max_requests - len(active))


class SecurityHeaders:
    """安全相关工具"""

    @staticmethod
    def hash_content(text: str) -> str:
        return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]

    @staticmethod
    def mask_api_key(key: str) -> str:
        if not key or len(key) < 8:
            return "***"
        return key[:4] + "***" + key[-4:]

    @staticmethod
    def log_security_event(event: str, details: str = ""):
        QuxuanLogger.warn(f"[SECURITY] {event}: {details}")


# ============================================================
# 4. 性能层 Performance
# ============================================================

class PerformanceOptimizer:
    """HTTP连接池 + 重试配置"""

    RETRY_COUNT = 3
    RETRY_BACKOFF = [1, 2, 4]
    TIMEOUT = 60.0
    MAX_POOL_SIZE = 10
    MAX_KEEPALIVE = 20

    @classmethod
    def get_httpx_client(cls) -> httpx.Client:
        return httpx.Client(
            timeout=cls.TIMEOUT,
            limits=httpx.Limits(
                max_connections=cls.MAX_POOL_SIZE,
                max_keepalive_connections=cls.MAX_KEEPALIVE,
            ),
        )


# ============================================================
# 5. 统一LLM调用 Unified LLM Caller
# ============================================================

class LLMCallError(Exception):
    """LLM调用异常基类"""
    def __init__(self, message: str, code: str = "LLM_ERROR"):
        super().__init__(message)
        self.code = code


class LLMCaller:
    """
    统一LLM调用 - 所有Skill共享
    含：重试、错误分类、日志、降级
    """

    @classmethod
    def call(
        cls,
        system_prompt: str,
        user_prompt: str,
        provider: str = "dashscope",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4000,
        fallback: Optional[str] = None,
    ) -> str:
        """
        调用LLM并返回结果

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词
            provider: API提供商 (dashscope/openai/deepseek)
            model: 模型名称（None则用默认）
            temperature: 温度参数
            max_tokens: 最大token数
            fallback: 失败时的降级响应（None则抛异常）

        Returns:
            LLM生成的文本内容

        Raises:
            LLMCallError: 调用失败且无fallback时抛出
        """
        logger = QuxuanLogger.setup("quxuan.llm")

        # 校验provider
        if not QuxuanConfig.validate_provider(provider):
            if fallback is not None:
                logger.warning(f"Unknown provider '{provider}', using fallback")
                return fallback
            raise LLMCallError(f"无效的provider: {provider}", code="INVALID_PROVIDER")

        # 获取配置
        cfg = QuxuanConfig.get_provider(provider)
        api_key = QuxuanConfig.get_api_key(provider)
        if not api_key:
            if fallback is not None:
                logger.warning(f"Missing API key for {provider}, using fallback")
                return fallback
            raise LLMCallError(
                f"缺少{provider}的API Key，请设置环境变量 {cfg['env_key']}",
                code="MISSING_API_KEY"
            )

        model_name = model or cfg["default_model"]
        url = cfg["url"]

        # 构造请求
        payload = {
            "model": model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
            "User-Agent": QuxuanConfig.USER_AGENT,
        }

        # 重试循环 - 复用同一个连接池
        last_error = None
        client = PerformanceOptimizer.get_httpx_client()
        try:
            for attempt in range(PerformanceOptimizer.RETRY_COUNT):
                try:
                    logger.info(f"LLM call attempt {attempt+1}/{PerformanceOptimizer.RETRY_COUNT}")
                    resp = client.post(url, headers=headers, json=payload)
                    resp.raise_for_status()

                    # 验证响应体非空
                    body = resp.text
                    if not body or not body.strip():
                        raise LLMCallError("API返回空响应", code="EMPTY_RESPONSE")

                    result = resp.json()

                    # 安全提取LLM响应
                    choices = result.get("choices", [])
                    if not choices:
                        raise LLMCallError(
                            f"LLM返回空choices: {str(result)[:200]}",
                            code="EMPTY_CHOICES"
                        )
                    content = choices[0].get("message", {}).get("content", "")
                    if not content or not content.strip():
                        raise LLMCallError("LLM返回空内容", code="EMPTY_CONTENT")
                    logger.info(f"LLM call success, length={len(content)}")
                    return content.strip()

                except (httpx.TimeoutException, httpx.ConnectError, httpx.NetworkError,
                        httpx.HTTPStatusError, json.JSONDecodeError) as e:
                    last_error = e
                    wait = PerformanceOptimizer.RETRY_BACKOFF[
                        min(attempt, len(PerformanceOptimizer.RETRY_BACKOFF) - 1)
                    ]
                    logger.warning(f"LLM call failed (attempt {attempt+1}): {e}")
                    if attempt < PerformanceOptimizer.RETRY_COUNT - 1:
                        time.sleep(wait)
                    continue

                except LLMCallError:
                    raise
        finally:
            try:
                client.close()
            except (ConnectionError, OSError):
                pass  # 关闭连接时的网络错误可安全忽略

        # 所有重试都失败
        if fallback is not None:
            logger.warning(f"All retries failed, using fallback")
            return fallback

        error_msg = str(last_error) if last_error else "Unknown error"
        raise LLMCallError(
            f"LLM调用失败（已重试{PerformanceOptimizer.RETRY_COUNT}次）: {error_msg}",
            code="MAX_RETRIES_EXCEEDED"
        )


# ============================================================
# 6. 原子文件写入 Atomic File Writer
# ============================================================

class AtomicFileWriter:
    """安全文件写入 - 先写临时文件，成功后原子替换"""

    @staticmethod
    def write(filepath: str, content: str) -> bool:
        """
        原子写入文件

        Args:
            filepath: 目标文件路径
            content: 写入内容

        Returns:
            True表示成功，False表示失败

        Raises:
            PermissionError: 无写入权限
            OSError: 其他IO错误
        """
        dirpath = os.path.dirname(os.path.abspath(filepath)) or "."
        os.makedirs(dirpath, exist_ok=True)
        tmp_fd = None
        tmp_path = None
        try:
            tmp_fd, tmp_path = tempfile.mkstemp(dir=dirpath, suffix=".tmp")
            with os.fdopen(tmp_fd, "w", encoding="utf-8") as f:
                f.write(content)
            tmp_fd = None  # fd已关闭，防止double-close
            os.replace(tmp_path, filepath)
            return True
        except PermissionError:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise
        except OSError:
            if tmp_path and os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise
        finally:
            if tmp_fd is not None:
                try:
                    os.close(tmp_fd)
                except OSError:
                    pass


# ============================================================
# 7. 交叉推荐引流 Cross Promotion
# ============================================================

class CrossPromotionEngine:
    """Skill间交叉推荐引擎"""

    RELATION_MAP = {
        "quxuan-travel":        ["quxuan-daily", "quxuan-copywriter"],
        "quxuan-daily":         ["quxuan-travel", "quxuan-copywriter"],
        "quxuan-workplace":     ["quxuan-professional", "quxuan-copywriter"],
        "quxuan-copywriter":    ["quxuan-daily", "quxuan-workplace"],
        "quxuan-professional":  ["quxuan-workplace", "quxuan-revenue-engine"],
        "quxuan-revenue-engine":["quxuan-professional", "quxuan-workplace"],
    }

    BRAND_BANNER = "✨ Powered by Quxuan 趣选 · AI智能服务平台 ✨"

    @classmethod
    def get_recommendation(cls, current_skill: str, language: str = "zh") -> str:
        related = cls.RELATION_MAP.get(current_skill, [])
        if not related:
            return ""
        skill_names_zh = {
            "quxuan-travel": "趣选旅行", "quxuan-daily": "趣选日常",
            "quxuan-workplace": "趣选职场", "quxuan-copywriter": "趣选文案",
            "quxuan-professional": "趣选专业", "quxuan-revenue-engine": "趣选收益",
        }
        skill_names_en = {
            "quxuan-travel": "Quxuan Travel", "quxuan-daily": "Quxuan Daily",
            "quxuan-workplace": "Quxuan Workplace", "quxuan-copywriter": "Quxuan Copywriter",
            "quxuan-professional": "Quxuan Professional", "quxuan-revenue-engine": "Quxuan Revenue",
        }
        skill_names = skill_names_en if language.startswith("en") else skill_names_zh
        names = [skill_names.get(s, s) for s in related[:2]]
        if language.startswith("en"):
            return f"💡 You may also like: {', '.join(names)} | {cls.BRAND_BANNER}"
        return f"💡 你可能还需要：{'、'.join(names)} | {cls.BRAND_BANNER}"

    @classmethod
    def get_closing_banner(cls, current_skill: str) -> str:
        """生成结尾品牌横幅"""
        return f"\n---\n{cls.BRAND_BANNER}\n更多能力请访问 https://clawhub.ai"


# ============================================================
# 8. 统一错误码 Error Codes
# ============================================================

class ErrorCode:
    """统一错误码体系"""
    SUCCESS = "OK"
    MISSING_API_KEY = "MISSING_API_KEY"
    INVALID_PROVIDER = "INVALID_PROVIDER"
    INVALID_INPUT = "INVALID_INPUT"
    EMPTY_RESPONSE = "EMPTY_RESPONSE"
    EMPTY_CHOICES = "EMPTY_CHOICES"
    EMPTY_CONTENT = "EMPTY_CONTENT"
    PARSE_ERROR = "PARSE_ERROR"
    MAX_RETRIES_EXCEEDED = "MAX_RETRIES_EXCEEDED"
    FILE_WRITE_ERROR = "FILE_WRITE_ERROR"
    RATE_LIMITED = "RATE_LIMITED"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    UNKNOWN_MODE = "UNKNOWN_MODE"

    @classmethod
    def to_json(cls, code: str, message: str, details: str = "") -> str:
        """生成标准错误JSON"""
        return json.dumps({
            "error": True,
            "code": code,
            "message": message,
            "details": details,
        }, ensure_ascii=False)
