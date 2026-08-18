import logging
import time
from uuid import uuid4

from fastapi import Request

from core.logging_config import correlation_id_var


logger = logging.getLogger("http")


async def correlation_id_middleware(
    request: Request,
    call_next
):

    # -------------------------
    # الحصول على Correlation ID
    # -------------------------

    correlation_id = request.headers.get(
        "X-Correlation-ID"
    )

    # إذا العميل لم يرسل ID، ننشئ واحداً
    if not correlation_id:
        correlation_id = str(uuid4())

    # تخزينه في ContextVar
    token = correlation_id_var.set(correlation_id)

    # بداية الطلب
    start_time = time.perf_counter()

    try:

        # تنفيذ الـ endpoint
        response = await call_next(request)

        # حساب مدة الطلب
        duration = time.perf_counter() - start_time

        # تسجيل الطلب
        logger.info(
            "%s %s | status=%s | duration=%.3fs",
            request.method,
            request.url.path,
            response.status_code,
            duration
        )

        # إرسال Correlation ID للـ client
        response.headers["X-Correlation-ID"] = correlation_id

        return response

    except Exception:

        duration = time.perf_counter() - start_time

        logger.exception(
            "%s %s | status=500 | duration=%.3fs",
            request.method,
            request.url.path,
            duration
        )

        raise

    finally:

        # تنظيف ContextVar
        correlation_id_var.reset(token)