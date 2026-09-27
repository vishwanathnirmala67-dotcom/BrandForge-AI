from typing import Any, Dict, List

import httpx

from config import TAVILY_API_KEY, TAVILY_BASE_URL


def _query_terms(profile: Dict[str, Any], discovery: Dict[str, Any]) -> List[str]:
    skills = [str(x) for x in profile.get("skills", []) if str(x).strip()]
    interests = [str(x) for x in profile.get("interests", []) if str(x).strip()]

    primary = skills[:2] + interests[:1]
    base = " ".join(primary).strip() or "personal branding creators"

    return [
        f"{base} creator audience problems",
        f"{base} content trends creator economy",
        f"{base} beginner audience pain points",
    ]


def _fallback(profile: Dict[str, Any], discovery: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "mode": "fallback",
        "queries": _query_terms(profile, discovery),
        "observations": [
            "Narrow audiences are easier to describe than a generic 'everyone interested in X' audience.",
            "Practical examples can help a creator differentiate educational content.",
            "Repeated content pillars are more useful when each one maps to a distinct audience problem.",
        ],
        "audience_problems": [
            "Choosing a focused niche",
            "Explaining expertise clearly",
            "Finding repeatable content topics",
            "Maintaining consistent positioning",
        ],
        "sources": [],
        "notice": "No live search provider is configured. These are workflow assumptions, not live web findings.",
    }


def run_research(profile: Dict[str, Any], discovery: Dict[str, Any]) -> Dict[str, Any]:
    if not TAVILY_API_KEY:
        return _fallback(profile, discovery)

    queries = _query_terms(profile, discovery)
    sources = []
    observations = []

    try:
        with httpx.Client(timeout=45.0) as client:
            for query in queries:
                response = client.post(
                    f"{TAVILY_BASE_URL}/search",
                    json={
                        "api_key": TAVILY_API_KEY,
                        "query": query,
                        "search_depth": "advanced",
                        "topic": "general",
                        "max_results": 5,
                        "include_answer": True,
                        "include_raw_content": False,
                    },
                )
                response.raise_for_status()
                data = response.json()

                answer = data.get("answer")
                if isinstance(answer, str) and answer.strip():
                    observations.append(answer.strip())

                for result in data.get("results", []) or []:
                    if not isinstance(result, dict):
                        continue
                    sources.append(
                        {
                            "title": result.get("title") or "Untitled source",
                            "url": result.get("url") or "",
                            "snippet": result.get("content") or "",
                            "score": result.get("score"),
                        }
                    )

        return {
            "mode": "live_web",
            "queries": queries,
            "observations": observations[:12],
            "audience_problems": [
                "Validated from the returned research; inspect source cards before treating them as universal.",
            ],
            "sources": sources[:12],
            "notice": "Live search results were collected through the configured web-search provider.",
        }

    except Exception as exc:
        fallback = _fallback(profile, discovery)
        fallback["mode"] = "fallback_after_error"
        fallback["notice"] = f"Live research failed and was safely downgraded: {exc}"
        return fallback
