import json

SYSTEM = """
You are BrandForge AI, a strategy-first personal brand architect.
Your job is to make concrete branding decisions from creator context.
Do not invent biographical facts. Separate facts, hypotheses, and recommendations.
Prefer narrow, specific positioning over vague creator language.
Avoid generic phrases such as 'passionate about', 'empowering people',
'building a community', 'unlock your potential', unless the evidence truly requires them.
Return valid JSON only when requested. No markdown fences.
""".strip()


def jdump(value) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2)


def discovery_prompt(profile: dict) -> str:
    return f"""
Stage: DISCOVER.
Analyze the creator profile and identify evidence-backed strengths, patterns, possible niches,
and questions that still need testing. Do not decide the final brand yet.

Creator profile:
{jdump(profile)}

Return JSON with exactly these keys:
- strengths: array of 3-7 items, each object with name, evidence, usefulness
- interests: array of strings
- possible_niches: array of 4-6 objects with niche, why_fit, risk
- audience_hypotheses: array of 2-4 strings
- open_questions: array of 3-6 strings
- discovery_summary: string
""".strip()


def positioning_prompt(profile: dict, discovery: dict, research: dict) -> str:
    return f"""
Stage: POSITION.
Use the creator profile, discovery analysis, and research evidence to produce a focused positioning.
Do not simply repeat generic content-creator language.
Prefer a clear audience + problem + skill/approach + distinct point of view.

Profile:
{jdump(profile)}

Discovery:
{jdump(discovery)}

Research:
{jdump(research)}

Return JSON with exactly these keys:
- brand_name: short working brand descriptor, not necessarily a registered business name
- category: category of personal brand
- niche: specific niche
- target_audience: specific audience
- audience_problem: primary problem
- value_proposition: one concise sentence
- unique_angle: differentiated angle
- point_of_view: strong belief that can guide content
- positioning_statement: one sentence beginning with 'I help'
- positioning_alternatives: array of 3 objects with name, statement, tradeoff
""".strip()


def brand_dna_prompt(positioning: dict, profile: dict) -> str:
    return f"""
Stage: SHAPE.
Create a coherent brand personality and voice from the approved positioning.

Positioning:
{jdump(positioning)}

Creator profile:
{jdump(profile)}

Return JSON with exactly these keys:
- personality: array of 3-5 objects with trait and justification
- traits_to_avoid: array of 3-6 strings
- principles: array of 4-6 practical brand principles
- voice: object with tone, should_sound_like, do, avoid, sample_phrases
- tagline_options: array of 5 objects with tagline and rationale
- recommended_tagline: string
- one_line_pitch: string
""".strip()


def visual_prompt(positioning: dict, dna: dict) -> str:
    return f"""
Stage: VISUALIZE.
Translate the strategy into a visual system, not a random aesthetic.

Positioning:
{jdump(positioning)}

Brand DNA:
{jdump(dna)}

Return JSON with exactly these keys:
- logo_direction: object with concept, symbol_logic, composition, avoid
- palette: array of exactly 5 objects with name, hex, role
- typography: object with heading_style, body_style, optional_font_examples
- imagery: object with subjects, treatment, composition, avoid
- visual_mood: 4-6 descriptive words
- social_layout: object with card_style, spacing, headline_style
""".strip()


def content_prompt(positioning: dict, dna: dict, research: dict) -> str:
    return f"""
Stage: CONTENT.
Build a repeatable content system that reinforces the positioning.

Positioning:
{jdump(positioning)}

Brand DNA:
{jdump(dna)}

Research:
{jdump(research)}

Return JSON with exactly these keys:
- content_pillars: array of 4-5 objects with name, audience_problem, promise, example_topics
- formats: array of 5-7 strings
- first_10_posts: array of 10 objects with number, platform, format, hook, idea, cta
- content_rules: array of 5-7 strings
""".strip()


def launch_prompt(profile: dict, positioning: dict, dna: dict, content: dict) -> str:
    return f"""
Stage: LAUNCH.
Turn the brand strategy into practical launch assets.

Profile:
{jdump(profile)}

Positioning:
{jdump(positioning)}

Brand DNA:
{jdump(dna)}

Content:
{jdump(content)}

Return JSON with exactly these keys:
- profile_bio: string, concise
- linkedin_about: string, 80-140 words
- instagram_bio: string, 1-3 lines
- launch_headline: string
- intro_post: string
- launch_cta: string
- first_week_plan: array of 7 objects with day, asset, goal
""".strip()


def critic_prompt(positioning: dict, dna: dict, visual: dict, content: dict, research: dict) -> str:
    return f"""
Stage: CHALLENGE.
Act as a skeptical brand critic. Test genericness, audience mismatch, contradictions,
weak differentiation, visual mismatch, repetition and unsupported assumptions.
Do not praise everything.

Positioning:
{jdump(positioning)}

Brand DNA:
{jdump(dna)}

Visual:
{jdump(visual)}

Content:
{jdump(content)}

Research:
{jdump(research)}

Return JSON with exactly these keys:
- status: one of 'needs_refinement', 'coherent', 'strong_but_specificity_needed'
- findings: array of 4-8 objects with severity (high/medium/low), area, issue, evidence, fix
- consistency_checks: object with positioning_voice, positioning_visual, voice_content, content_audience
- strongest_asset: string
- biggest_risk: string
- revision_plan: array of 3-6 concrete actions
""".strip()


def improve_prompt(project: dict) -> str:
    return f"""
Stage: REVISE.
Use the critic findings to produce an improved brand. Preserve creator facts and preserve strong parts.
Only change areas that have a reason to change.

Project:
{jdump(project)}

Return JSON with these keys:
- positioning
- brand_dna
- visual_identity
- content_strategy
- launch_strategy
- revision_notes

Each object should keep the same overall schema as the original project sections.
""".strip()
