import time
import random
from typing import Optional, Dict, Any, Iterable, Tuple

import requests
from Module import Logging
from Module.ConfigService import ConfigService


class NetUtils:
    def __init__(self):
        self.log = Logging.Log("NetUtils")
        self.timeout = ConfigService().get_value("Time", "request_timeout_sec", 10)
        self.default_retries = ConfigService().get_value("Time", "net_retries", 3)
        self.base_backoff_ms = ConfigService().get_value("Time", "net_backoff_ms", 500)
        self.max_backoff_ms = ConfigService().get_value("Time", "net_max_backoff_ms", 5000)
        self.jitter_ratio = 0.2

    def classify_error(self, response: Optional[requests.Response], exc: Optional[BaseException]) -> str:
        if exc is not None:
            # 常见网络异常分类
            if isinstance(exc, (requests.Timeout, requests.ConnectionError)):
                return "network"
            return "exception"
        if response is None:
            return "unknown"
        status = response.status_code
        if status == 401 or status == 403:
            return "auth"
        if status == 429:
            return "rate_limit"
        if 500 <= status <= 599:
            return "server"
        if 400 <= status <= 499:
            return "client"
        # 业务语义判定（文本）
        try:
            text = response.text
        except Exception:
            text = ""
        markers = {
            "capacity_full": ["容量已满", "人数已满", "满员"],
            "not_time": ["未到选课时间", "不在选课时间", "请在选课时间内"],
        }
        for label, kws in markers.items():
            for k in kws:
                if k in text:
                    return label
        return "ok"

    def request_with_retry(
        self,
        session: requests.Session,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None,
        timeout: Optional[float] = None,
        retries: Optional[int] = None,
        retry_on_status: Iterable[int] = (429, 500, 502, 503, 504),
    ) -> Tuple[Optional[requests.Response], Optional[str]]:
        """
        返回 (response, error_label)。error_label 为 None 表示成功。
        """
        t = timeout if timeout is not None else self.timeout
        r = retries if retries is not None else int(self.default_retries)
        backoff_ms = int(self.base_backoff_ms)

        for attempt in range(1, r + 1):
            resp = None
            exc: Optional[BaseException] = None
            try:
                resp = session.request(method=method.upper(), url=url, params=params, data=data, timeout=t)
                # 成功类状态直接返回
                if resp.status_code < 400 and self.classify_error(resp, None) in ("ok",):
                    return resp, None
                # 可重试状态码
                if resp.status_code in retry_on_status:
                    label = self.classify_error(resp, None)
                else:
                    # 非可重试错误，直接返回
                    label = self.classify_error(resp, None)
                    return resp, label
            except BaseException as e:
                exc = e
                label = self.classify_error(None, exc)

            # 需要重试
            if attempt >= r:
                return resp, label
            # 指数退避 + 抖动
            sleep_ms = min(backoff_ms, int(self.max_backoff_ms))
            jitter = random.uniform(1 - self.jitter_ratio, 1 + self.jitter_ratio)
            time.sleep(sleep_ms * jitter / 1000.0)
            backoff_ms = min(backoff_ms * 2, int(self.max_backoff_ms))
            self.log.main("DEBUG", f"重试[{attempt}/{r-1}] {method} {url}，原因: {label}")

        return None, "unknown"

    @staticmethod
    def parse_json_safe(resp: requests.Response) -> Optional[dict]:
        try:
            return resp.json()
        except Exception:
            return None
