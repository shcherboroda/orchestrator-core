from __future__ import annotations

import os
import pytest
import httpx


def isOllamaUp(baseUrl: str) -> bool:
    try:
        with httpx.Client(timeout=1.0) as client:
            response = client.get(f"{baseUrl}/api/tags")
            return response.status_code == 200
    except Exception:
        return False


@pytest.mark.integration
def testOllamaSmoke() -> None:
    baseUrl = os.getenv("DTOollamaBaseUrl", "http://127.0.0.1:11434").rstrip("/")

    if not isOllamaUp(baseUrl):
        pytest.skip("Ollama is not running")

    model = os.getenv("DTOollamaModel", "qwen2.5:3b")
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": "Reply with exactly one word: Hello",
            }
        ],
        "stream": False,
        "options": {
            "num_predict": 8,
            "temperature": 0.0,
        },
    }

    with httpx.Client(timeout=30.0) as client:
        response = client.post(f"{baseUrl}/api/chat", json=payload)

    assert response.status_code == 200
    data = response.json()
    content = data["message"]["content"].strip()

    assert len(content) > 0
