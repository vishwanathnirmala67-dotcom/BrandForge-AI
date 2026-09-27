from typing import Any, Dict, List

from ai_service import call_llm_json
from prompts import (
    brand_dna_prompt,
    content_prompt,
    critic_prompt,
    discovery_prompt,
    improve_prompt,
    launch_prompt,
    positioning_prompt,
    visual_prompt,
)
from research_service import run_research


def clean_list(values: List[str]) -> List[str]:
    return [str(v).strip() for v in values if str(v).strip()]


def fallback_discovery(profile: Dict[str, Any]) -> Dict[str, Any]:
    skills = clean_list(profile.get("skills", [])) or ["Problem solving"]
    interests = clean_list(profile.get("interests", []))

    niches = []
    for skill in skills[:3]:
        niches.append(
            {
                "niche": f"Practical {skill} for beginners",
                "why_fit": f"Connects the creator's skill in {skill} with a teachable audience need.",
                "risk": "May remain broad if the audience is not narrowed.",
            }
        )
        niches.append(
            {
                "niche": f"{skill} project-based learning",
                "why_fit": "Naturally creates practical demonstrations and content.",
                "risk": "Requires consistent proof through projects or examples.",
            }
        )

    return {
        "strengths": [
            {
                "name": skill,
                "evidence": "Listed in creator profile",
                "usefulness": "Potential content and positioning asset",
            }
            for skill in skills[:5]
        ],
        "interests": interests,
        "possible_niches": niches[:6],
        "audience_hypotheses": [
            "Beginners seeking simple explanations",
            "Students or early-stage learners seeking practical outcomes",
            "People exploring the creator's primary skill",
        ],
        "open_questions": [
            "Which audience segment has the strongest recurring need?",
            "Which problems can the creator solve from real experience?",
            "What proof can the creator consistently show?",
        ],
        "discovery_summary": "Local fallback discovery based only on the submitted creator profile.",
    }


def fallback_positioning(profile: Dict[str, Any], discovery: Dict[str, Any], research: Dict[str, Any]) -> Dict[str, Any]:
    primary = (discovery.get("strengths") or [{}])[0]
    skill = primary.get("name") or "useful skills"
    audience = profile.get("audience_hint") or "beginners and students"

    return {
        "brand_name": f"{skill} in Practice",
        "category": "Practical knowledge creator",
        "niche": f"Practical {skill} for beginners",
        "target_audience": audience,
        "audience_problem": "People need simpler, more actionable guidance than generic advice provides.",
        "value_proposition": f"Helping {audience.lower()} learn {skill.lower()} through simple, practical content.",
        "unique_angle": "Teach by showing real use, experiments and outcomes rather than only theory.",
        "point_of_view": "Useful learning should end in something the learner can do.",
        "positioning_statement": f"I help {audience.lower()} learn {skill.lower()} through practical, beginner-friendly content.",
        "positioning_alternatives": [
            {
                "name": "Practical Tutor",
                "statement": f"I help {audience.lower()} turn {skill.lower()} into practical skills.",
                "tradeoff": "Clear but less distinctive.",
            },
            {
                "name": "Build-in-Public Teacher",
                "statement": f"I teach {skill.lower()} by building projects in public.",
                "tradeoff": "Needs visible project proof.",
            },
            {
                "name": "Beginner Simplifier",
                "statement": f"I simplify {skill.lower()} for people who are just starting.",
                "tradeoff": "Strong clarity, weaker differentiation without a signature method.",
            },
        ],
    }


def fallback_dna(positioning: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "personality": [
            {"trait": "Practical", "justification": "The positioning promises usable outcomes."},
            {"trait": "Clear", "justification": "The audience is beginner-oriented."},
            {"trait": "Curious", "justification": "Experiments and learning support ongoing content."},
            {"trait": "Friendly", "justification": "Beginner audiences benefit from approachable language."},
            {"trait": "Experimental", "justification": "Build-and-test content creates credible proof."},
        ],
        "traits_to_avoid": ["Corporate", "Generic motivational", "Overly technical", "Clickbait"],
        "principles": [
            "Show before telling",
            "Prefer practical examples",
            "Keep claims specific",
            "Explain jargon",
            "Document real learning",
        ],
        "voice": {
            "tone": ["Friendly", "Clear", "Confident", "Practical"],
            "should_sound_like": "A knowledgeable creator explaining something useful to a peer.",
            "do": ["Use examples", "Explain simply", "Be concrete"],
            "avoid": ["Buzzwords", "Fake urgency", "Empty inspiration"],
            "sample_phrases": ["Here is the practical version.", "Let's build it.", "The mistake I would avoid is..."],
        },
        "tagline_options": [
            {"tagline": "Learn it. Build it. Share it.", "rationale": "Connects learning with visible outcomes."},
            {"tagline": "Less theory. More doing.", "rationale": "Directly expresses the practical angle."},
            {"tagline": "Make knowledge useful.", "rationale": "Short and strategy-aligned."},
            {"tagline": "Learn by building.", "rationale": "Strong if projects are central."},
            {"tagline": "Simple ideas. Real outcomes.", "rationale": "Balances clarity and practicality."},
        ],
        "recommended_tagline": "Learn it. Build it. Share it.",
        "one_line_pitch": positioning.get("positioning_statement", ""),
    }


def fallback_visual(profile: Dict[str, Any], positioning: Dict[str, Any]) -> Dict[str, Any]:
    style = profile.get("preferred_style") or "Modern, minimal, energetic"
    return {
        "logo_direction": {
            "concept": "Personal monogram + subtle build/knowledge symbol",
            "symbol_logic": "The mark should connect identity with practical creation.",
            "composition": "Compact icon that works at social-avatar size.",
            "avoid": "Over-detailed mascots or generic lightbulbs.",
        },
        "palette": [
            {"name": "Ink", "hex": "#0F172A", "role": "Primary text and dark surfaces"},
            {"name": "Electric Blue", "hex": "#2563EB", "role": "Primary action"},
            {"name": "Violet", "hex": "#7C3AED", "role": "Secondary accent"},
            {"name": "Cloud", "hex": "#F8FAFC", "role": "Background"},
            {"name": "Slate", "hex": "#64748B", "role": "Secondary text"},
        ],
        "typography": {
            "heading_style": "Bold geometric sans-serif",
            "body_style": "Neutral, highly readable sans-serif",
            "optional_font_examples": ["Inter", "Manrope", "Plus Jakarta Sans"],
        },
        "imagery": {
            "subjects": ["real workspaces", "projects", "screens", "learning moments"],
            "treatment": "Clean crops, subtle gradients and clear focal points.",
            "composition": "Human + work artifact, not abstract stock imagery.",
            "avoid": "Unrelated corporate stock photos and cluttered collages.",
        },
        "visual_mood": style.split(",") if isinstance(style, str) else ["Modern", "Minimal"],
        "social_layout": {
            "card_style": "Large headline, one visual idea, small source/CTA footer",
            "spacing": "Generous whitespace and consistent margins",
            "headline_style": "Short, high-contrast, sentence-case",
        },
    }


def fallback_content(positioning: Dict[str, Any]) -> Dict[str, Any]:
    niche = positioning.get("niche", "your niche")
    audience = positioning.get("target_audience", "your audience")
    pillars = [
        {"name": "Learn", "audience_problem": "Confusion", "promise": "Make complex ideas simple", "example_topics": [f"3 {niche} concepts explained simply", "Beginner mistakes"]},
        {"name": "Build", "audience_problem": "No practice", "promise": "Show practical outcomes", "example_topics": ["Weekend project", "Build breakdown"]},
        {"name": "Tools", "audience_problem": "Tool overload", "promise": "Recommend useful workflows", "example_topics": ["Tools I actually use", "Workflow comparison"]},
        {"name": "Lessons", "audience_problem": "Repeated mistakes", "promise": "Share what experience teaches", "example_topics": ["What failed", "What I would do differently"]},
        {"name": "Journey", "audience_problem": "Low trust", "promise": "Show the real process", "example_topics": ["Build in public", "Monthly progress"]},
    ]
    ideas = [
        f"Why I chose {niche}",
        f"3 mistakes {audience.lower()} should avoid",
        "The simplest roadmap I would use today",
        "A tool that saved me time",
        "Build this instead of only watching tutorials",
        "One difficult idea explained simply",
        "A small project you can build this week",
        "What I learned from my latest experiment",
        "A mistake I made and what it taught me",
        "What this personal brand will stand for",
    ]
    posts = [
        {"number": i + 1, "platform": "LinkedIn", "format": "Text + visual", "hook": idea, "idea": idea, "cta": "Follow for practical ideas."}
        for i, idea in enumerate(ideas)
    ]
    return {
        "content_pillars": pillars,
        "formats": ["Carousel", "Short video", "Text post", "Tutorial", "Case study", "Build update"],
        "first_10_posts": posts,
        "content_rules": [
            "Every post should support one content pillar.",
            "Prefer specific examples over broad advice.",
            "Use a consistent point of view.",
            "Show proof whenever possible.",
            "Do not repeat the same insight in different words.",
        ],
    }


def fallback_launch(profile: Dict[str, Any], positioning: Dict[str, Any], dna: Dict[str, Any], content: Dict[str, Any]) -> Dict[str, Any]:
    name = profile.get("name") or "Creator"
    statement = positioning.get("positioning_statement", "")
    return {
        "profile_bio": statement,
        "linkedin_about": f"{name} creates practical content around {positioning.get('niche', 'useful ideas')}. The focus is on helping {positioning.get('target_audience', 'learners').lower()} turn knowledge into action. The brand prioritizes clear explanations, real examples and visible learning.",
        "instagram_bio": f"{positioning.get('niche', 'Practical learning')}\nSimple ideas → real outcomes\n👇 Build with me",
        "launch_headline": f"Building a practical brand around {positioning.get('niche', 'useful skills')}",
        "intro_post": f"Hi, I'm {name}. I'm building a personal brand around {positioning.get('niche', 'practical learning')}. My goal is simple: make useful knowledge easier to understand and easier to apply. I’ll share what I learn, build and improve along the way.",
        "launch_cta": "Follow the journey for practical ideas, experiments and lessons.",
        "first_week_plan": [
            {"day": 1, "asset": "Introduction post", "goal": "Explain who you are and who you help"},
            {"day": 2, "asset": "Educational post", "goal": "Demonstrate clarity"},
            {"day": 3, "asset": "Practical tutorial", "goal": "Demonstrate usefulness"},
            {"day": 4, "asset": "Tool/workflow post", "goal": "Show practical judgment"},
            {"day": 5, "asset": "Lesson post", "goal": "Build trust through honesty"},
            {"day": 6, "asset": "Build update", "goal": "Show proof in public"},
            {"day": 7, "asset": "Weekly recap", "goal": "Create continuity"},
        ],
    }


def fallback_critic(positioning: Dict[str, Any], dna: Dict[str, Any], visual: Dict[str, Any], content: Dict[str, Any], research: Dict[str, Any]) -> Dict[str, Any]:
    findings = []
    audience = positioning.get("target_audience", "")
    niche = positioning.get("niche", "")

    if not audience or len(audience.split()) > 14:
        findings.append({
            "severity": "high",
            "area": "Audience",
            "issue": "Audience definition is missing or too broad.",
            "evidence": audience or "No audience provided",
            "fix": "Choose one primary audience before publishing consistently.",
        })

    if not positioning.get("unique_angle"):
        findings.append({
            "severity": "high",
            "area": "Differentiation",
            "issue": "Unique angle is not explicit.",
            "evidence": "No unique angle field",
            "fix": "Define a repeatable method, proof pattern or point of view.",
        })

    if niche and "for beginners" in niche.lower():
        findings.append({
            "severity": "low",
            "area": "Specificity",
            "issue": "'For beginners' is useful but still generic.",
            "evidence": niche,
            "fix": "Add a distinctive problem, outcome or method once evidence supports it.",
        })

    return {
        "status": "needs_refinement" if findings else "coherent",
        "findings": findings,
        "consistency_checks": {
            "positioning_voice": "aligned",
            "positioning_visual": "aligned",
            "voice_content": "aligned",
            "content_audience": "needs ongoing validation",
        },
        "strongest_asset": positioning.get("point_of_view", "Clear practical POV"),
        "biggest_risk": "Positioning may become generic if the content does not show specific proof.",
        "revision_plan": [
            "Narrow the audience if performance evidence suggests a smaller segment.",
            "Turn the point of view into repeatable post formats.",
            "Show real projects, examples or case studies to support the promise.",
        ],
    }


def run_workflow(profile: Dict[str, Any]) -> Dict[str, Any]:
    stages = []

    try:
        discovery = call_llm_json(discovery_prompt(profile))
        stages.append({"name": "Discover", "mode": "llm", "status": "complete"})
    except Exception as exc:
        discovery = fallback_discovery(profile)
        stages.append({"name": "Discover", "mode": "fallback", "status": "complete", "reason": str(exc)})

    research = run_research(profile, discovery)
    stages.append({"name": "Research", "mode": research.get("mode"), "status": "complete"})

    try:
        positioning = call_llm_json(positioning_prompt(profile, discovery, research))
        stages.append({"name": "Position", "mode": "llm", "status": "complete"})
    except Exception as exc:
        positioning = fallback_positioning(profile, discovery, research)
        stages.append({"name": "Position", "mode": "fallback", "status": "complete", "reason": str(exc)})

    try:
        dna = call_llm_json(brand_dna_prompt(positioning, profile))
        stages.append({"name": "Shape", "mode": "llm", "status": "complete"})
    except Exception as exc:
        dna = fallback_dna(positioning)
        stages.append({"name": "Shape", "mode": "fallback", "status": "complete", "reason": str(exc)})

    try:
        visual = call_llm_json(visual_prompt(positioning, dna))
        stages.append({"name": "Visualize", "mode": "llm", "status": "complete"})
    except Exception as exc:
        visual = fallback_visual(profile, positioning)
        stages.append({"name": "Visualize", "mode": "fallback", "status": "complete", "reason": str(exc)})

    try:
        content = call_llm_json(content_prompt(positioning, dna, research))
        stages.append({"name": "Content", "mode": "llm", "status": "complete"})
    except Exception as exc:
        content = fallback_content(positioning)
        stages.append({"name": "Content", "mode": "fallback", "status": "complete", "reason": str(exc)})

    try:
        launch = call_llm_json(launch_prompt(profile, positioning, dna, content))
        stages.append({"name": "Launch", "mode": "llm", "status": "complete"})
    except Exception as exc:
        launch = fallback_launch(profile, positioning, dna, content)
        stages.append({"name": "Launch", "mode": "fallback", "status": "complete", "reason": str(exc)})

    try:
        critic = call_llm_json(critic_prompt(positioning, dna, visual, content, research))
        stages.append({"name": "Challenge", "mode": "llm", "status": "complete"})
    except Exception as exc:
        critic = fallback_critic(positioning, dna, visual, content, research)
        stages.append({"name": "Challenge", "mode": "fallback", "status": "complete", "reason": str(exc)})

    final_kit = {
        "brand_name": positioning.get("brand_name") or positioning.get("niche") or "Personal Brand",
        "summary": "A strategy-first personal brand system built from creator context, research, positioning, identity, content and critique.",
        "positioning": positioning,
        "brand_dna": dna,
        "visual_identity": visual,
        "content_strategy": content,
        "launch_strategy": launch,
        "brand_critic": critic,
    }

    return {
        "profile": profile,
        "discovery": discovery,
        "research": research,
        "positioning": positioning,
        "brand_dna": dna,
        "visual_identity": visual,
        "content_strategy": content,
        "launch_strategy": launch,
        "brand_critic": critic,
        "final_kit": final_kit,
        "workflow_stages": stages,
        "generated_mode": "hybrid",
    }


def improve_project(project: Dict[str, Any]) -> Dict[str, Any]:
    try:
        improved = call_llm_json(improve_prompt(project))
        updated = dict(project)
        for key in ["positioning", "brand_dna", "visual_identity", "content_strategy", "launch_strategy"]:
            if key in improved:
                updated[key] = improved[key]
        updated["revision_notes"] = improved.get("revision_notes", [])
        updated["brand_critic"] = fallback_critic(
            updated.get("positioning", {}),
            updated.get("brand_dna", {}),
            updated.get("visual_identity", {}),
            updated.get("content_strategy", {}),
            updated.get("research", {}),
        )
        updated["generated_mode"] = "revised_llm"
        updated["final_kit"] = {
            "brand_name": updated.get("positioning", {}).get("brand_name") or "Personal Brand",
            "summary": "Revised after an explicit critique pass.",
            "positioning": updated.get("positioning", {}),
            "brand_dna": updated.get("brand_dna", {}),
            "visual_identity": updated.get("visual_identity", {}),
            "content_strategy": updated.get("content_strategy", {}),
            "launch_strategy": updated.get("launch_strategy", {}),
            "brand_critic": updated.get("brand_critic", {}),
        }
        return updated
    except Exception:
        updated = dict(project)
        critic = dict(updated.get("brand_critic", {}))
        critic["revision_plan"] = [
            "Make the target audience narrower.",
            "Turn the point of view into recurring content formats.",
            "Add specific proof through projects or case studies.",
        ]
        updated["brand_critic"] = critic
        updated["revision_notes"] = [
            "Local improvement fallback applied because a live model revision was unavailable."
        ]
        return updated
