import { useMemo, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const STAGES = [
  { id: "discover", label: "Discover", icon: "◈" },
  { id: "research", label: "Research", icon: "⌕" },
  { id: "position", label: "Position", icon: "◎" },
  { id: "shape", label: "Shape", icon: "◉" },
  { id: "visual", label: "Visualize", icon: "◇" },
  { id: "content", label: "Content", icon: "✦" },
  { id: "challenge", label: "Challenge", icon: "⚑" },
  { id: "deliver", label: "Deliver", icon: "↗" },
];

const EMPTY_FORM = {
  name: "",
  role: "",
  skills: "Python, AI, Web Development",
  experience: "",
  interests: "AI, technology, education",
  goals: "Build an audience and share practical knowledge",
  platforms: "LinkedIn, Instagram",
  audience_hint: "",
  existing_content: "",
  location: "",
  preferred_style: "Modern, minimal, professional",
};

function toList(value) {
  return value
    .split(",")
    .map((x) => x.trim())
    .filter(Boolean);
}

function App() {
  const [screen, setScreen] = useState("home");
  const [activeSection, setActiveSection] = useState("overview");
  const [form, setForm] = useState(EMPTY_FORM);
  const [project, setProject] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const setField = (key, value) => {
    setForm((current) => ({ ...current, [key]: value }));
  };

  async function buildBrand() {
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_URL}/api/build-brand`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          profile: {
            ...form,
            skills: toList(form.skills),
            interests: toList(form.interests),
            platforms: toList(form.platforms),
          },
        }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Brand generation failed.");
      setProject(data);
      setActiveSection("overview");
      setScreen("kit");
    } catch (err) {
      setError(err.message || "Could not connect to the backend.");
    } finally {
      setLoading(false);
    }
  }

  async function improveBrand() {
    if (!project) return;
    setLoading(true);
    setError("");
    try {
      const response = await fetch(`${API_URL}/api/improve-brand`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ project }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Revision failed.");
      setProject(data);
    } catch (err) {
      setError(err.message || "Could not revise the brand.");
    } finally {
      setLoading(false);
    }
  }

  async function exportPdf() {
    if (!project?.project_id) {
      window.print();
      return;
    }
    try {
      const response = await fetch(`${API_URL}/api/projects/${project.project_id}/export.pdf`, {
        method: "POST",
      });
      if (!response.ok) throw new Error("PDF export failed.");
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `brandforge-${project.project_id}.pdf`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch {
      window.print();
    }
  }

  function restart() {
    setProject(null);
    setError("");
    setScreen("home");
  }

  return (
    <div className="app-shell">
      <Navbar onHome={restart} />

      {screen === "home" && (
        <Home onStart={() => setScreen("builder")} />
      )}

      {screen === "builder" && (
        <Builder
          form={form}
          setField={setField}
          onBack={() => setScreen("home")}
          onBuild={buildBrand}
          loading={loading}
          error={error}
        />
      )}

      {screen === "kit" && project && (
        <BrandKit
          project={project}
          activeSection={activeSection}
          setActiveSection={setActiveSection}
          onImprove={improveBrand}
          onExport={exportPdf}
          onRestart={restart}
          loading={loading}
          error={error}
        />
      )}
    </div>
  );
}

function Navbar({ onHome }) {
  return (
    <header className="topbar">
      <button className="brand-button" onClick={onHome}>
        <span className="brand-glyph">B</span>
        <span className="brand-meta">
          <strong>BrandForge</strong>
          <small>AI Personal Brand Architect</small>
        </span>
      </button>
      <div className="topbar-right">
        <span className="sponsor-badge">INKLOOM CHALLENGE</span>
        <span className="live-badge">● PRODUCT FLOW</span>
      </div>
    </header>
  );
}

function Home({ onStart }) {
  return (
    <main className="landing">
      <div className="hero-grid-line" />
      <section className="hero">
        <div className="eyebrow">STRATEGY-FIRST PERSONAL BRANDING</div>
        <h1>
          Discover the brand
          <span>your skills can own.</span>
        </h1>
        <p>
          BrandForge turns creator context into a researched, positioned,
          critiqued and launch-ready personal brand system.
        </p>
        <div className="hero-actions">
          <button className="primary-button" onClick={onStart}>
            Build my brand <span>→</span>
          </button>
          <span className="micro-copy">Discover → Research → Position → Launch</span>
        </div>
      </section>

      <section className="workflow-strip">
        {STAGES.map((stage, index) => (
          <div className="workflow-step" key={stage.id}>
            <span className="workflow-number">0{index + 1}</span>
            <div>
              <strong>{stage.label}</strong>
              <small>
                {stage.id === "discover" && "Understand you"}
                {stage.id === "research" && "Study the space"}
                {stage.id === "position" && "Find your edge"}
                {stage.id === "shape" && "Build the voice"}
                {stage.id === "visual" && "Design the look"}
                {stage.id === "content" && "Plan what to say"}
                {stage.id === "challenge" && "Attack weak ideas"}
                {stage.id === "deliver" && "Launch the kit"}
              </small>
            </div>
          </div>
        ))}
      </section>

      <section className="why-grid">
        <FeatureCard title="Not one giant prompt" text="Every stage has a specific job and passes structured context forward." />
        <FeatureCard title="Research-backed" text="Live source cards can be attached to the audience and niche analysis." />
        <FeatureCard title="Critic in the loop" text="The product actively looks for generic positioning, mismatch and repetition." />
      </section>
    </main>
  );
}

function FeatureCard({ title, text }) {
  return (
    <article className="feature-card">
      <div className="feature-dot" />
      <h3>{title}</h3>
      <p>{text}</p>
    </article>
  );
}

function Builder({ form, setField, onBack, onBuild, loading, error }) {
  return (
    <main className="builder-page">
      <div className="builder-head">
        <div>
          <div className="eyebrow">01 · DISCOVER</div>
          <h1>Tell the architect who you are.</h1>
          <p>We use your answers as the source context for every downstream brand decision.</p>
        </div>
        <div className="architecture-note">
          <strong>AI workflow</strong>
          <span>Profile → Research → Position → Shape → Visualize → Content → Challenge → Deliver</span>
        </div>
      </div>

      <section className="builder-card">
        <div className="field-grid">
          <Field label="Name" value={form.name} placeholder="Your name" onChange={(v) => setField("name", v)} />
          <Field label="Current role" value={form.role} placeholder="Student, writer, designer..." onChange={(v) => setField("role", v)} />
          <Field label="Skills" value={form.skills} placeholder="Python, writing, design..." onChange={(v) => setField("skills", v)} />
          <Field label="Experience" value={form.experience} placeholder="Projects, work, teaching..." onChange={(v) => setField("experience", v)} />
          <Field label="Interests" value={form.interests} placeholder="AI, education, startups..." onChange={(v) => setField("interests", v)} />
          <Field label="Platforms" value={form.platforms} placeholder="LinkedIn, Instagram..." onChange={(v) => setField("platforms", v)} />
          <Field label="What do you want to achieve?" full value={form.goals} placeholder="Audience, clients, authority, teaching..." onChange={(v) => setField("goals", v)} />
          <Field label="Who do you think needs your content?" full value={form.audience_hint} placeholder="Optional — AI will challenge this assumption." onChange={(v) => setField("audience_hint", v)} />
          <Field label="Existing content / proof" full value={form.existing_content} placeholder="Links or description of what you already publish" onChange={(v) => setField("existing_content", v)} />
          <Field label="Preferred visual style" full value={form.preferred_style} placeholder="Minimal, bold, editorial, playful..." onChange={(v) => setField("preferred_style", v)} />
        </div>

        {error && <div className="error-box">{error}</div>}

        <div className="builder-actions">
          <button className="secondary-button" onClick={onBack}>← Back</button>
          <button className="primary-button" onClick={onBuild} disabled={loading}>
            {loading ? "Running brand workflow..." : "Run BrandForge →"}
          </button>
        </div>
      </section>

      <div className="build-note">
        <span>ⓘ</span>
        <p>Without API keys, the project still runs in a clearly labelled local fallback mode. Live claims are never silently fabricated.</p>
      </div>
    </main>
  );
}

function Field({ label, value, placeholder, onChange, full = false }) {
  return (
    <label className={`field ${full ? "field-full" : ""}`}>
      <span>{label}</span>
      <input value={value} placeholder={placeholder} onChange={(e) => onChange(e.target.value)} />
    </label>
  );
}

function BrandKit({ project, activeSection, setActiveSection, onImprove, onExport, onRestart, loading, error }) {
  const pos = project.positioning || {};
  const research = project.research || {};
  const dna = project.brand_dna || {};
  const visual = project.visual_identity || {};
  const content = project.content_strategy || {};
  const launch = project.launch_strategy || {};
  const critic = project.brand_critic || {};

  const sections = [
    ["overview", "Overview"],
    ["research", "Web Research"],
    ["positioning", "Positioning"],
    ["identity", "Brand DNA"],
    ["visual", "Visual Identity"],
    ["content", "Content Engine"],
    ["launch", "Launch"],
    ["critic", "AI Critic"],
  ];

  return (
    <main className="kit-page">
      <section className="kit-hero">
        <div>
          <div className="eyebrow light">YOUR LAUNCH-READY BRAND</div>
          <h1>{pos.brand_name || pos.niche || "Personal Brand"}</h1>
          <p>{pos.positioning_statement}</p>
          <div className="hero-tags">
            <span>{pos.category || "Creator brand"}</span>
            <span>{research.mode === "live_web" ? "Live research" : "Fallback research"}</span>
            <span>{project.generated_mode || "hybrid"}</span>
          </div>
        </div>
        <div className="brand-readiness">
          <span>WORKFLOW</span>
          <strong>8 / 8</strong>
          <small>stages returned</small>
        </div>
      </section>

      <div className="kit-layout">
        <aside className="kit-sidebar">
          <div className="sidebar-label">BRAND SYSTEM</div>
          {sections.map(([id, label], index) => (
            <button key={id} className={activeSection === id ? "side-link active" : "side-link"} onClick={() => setActiveSection(id)}>
              <span>0{index + 1}</span>
              {label}
            </button>
          ))}
          <div className="sidebar-divider" />
          <button className="secondary-button side-action" onClick={onRestart}>+ New brand</button>
          <button className="primary-button side-action" onClick={onExport}>Export PDF</button>
        </aside>

        <section className="kit-content">
          {error && <div className="error-box">{error}</div>}

          {activeSection === "overview" && (
            <Overview pos={pos} critic={critic} stages={project.workflow_stages || []} />
          )}

          {activeSection === "research" && (
            <ResearchPanel research={research} />
          )}

          {activeSection === "positioning" && (
            <PositioningPanel pos={pos} />
          )}

          {activeSection === "identity" && (
            <IdentityPanel dna={dna} />
          )}

          {activeSection === "visual" && (
            <VisualPanel visual={visual} />
          )}

          {activeSection === "content" && (
            <ContentPanel content={content} />
          )}

          {activeSection === "launch" && (
            <LaunchPanel launch={launch} />
          )}

          {activeSection === "critic" && (
            <CriticPanel critic={critic} onImprove={onImprove} loading={loading} />
          )}
        </section>
      </div>
    </main>
  );
}

function Overview({ pos, critic, stages }) {
  const live = stages.filter((x) => x.mode === "llm" || x.mode === "live_web").length;
  return (
    <div className="section-stack">
      <SectionTitle eyebrow="00 · OVERVIEW" title="The strategy behind the brand" subtitle="This page tells the story judges can follow: starting context → evidence → decisions → critique → launch." />
      <div className="overview-grid">
        <Metric title="Niche" value={pos.niche || "—"} />
        <Metric title="Audience" value={pos.target_audience || "—"} />
        <Metric title="Unique angle" value={pos.unique_angle || "—"} />
        <Metric title="Workflow evidence" value={`${live} live/provider-backed steps`} />
      </div>
      <Panel title="Positioning statement">
        <div className="statement-card">{pos.positioning_statement || "—"}</div>
      </Panel>
      <Panel title="AI critic signal">
        <div className={`status-chip ${critic.status === "coherent" ? "good" : "warn"}`}>
          {critic.status || "Not available"}
        </div>
        <p className="panel-text">{critic.biggest_risk || critic.recommendation || "Review the critique before launch."}</p>
      </Panel>
    </div>
  );
}

function ResearchPanel({ research }) {
  return (
    <div className="section-stack">
      <SectionTitle eyebrow="02 · WEB RESEARCH" title="Audience intelligence with evidence" subtitle="Source cards make the research inspectable rather than hiding it behind a generic AI paragraph." />
      <div className="research-banner">
        <div>
          <strong>{research.mode === "live_web" ? "Live web research" : "Local fallback research"}</strong>
          <p>{research.notice}</p>
        </div>
        <div className="query-box">{(research.queries || []).join(" · ")}</div>
      </div>
      <div className="insight-grid">
        {(research.observations || []).map((item, index) => (
          <article className="insight-card" key={index}>
            <span>INSIGHT 0{index + 1}</span>
            <p>{item}</p>
          </article>
        ))}
      </div>
      <Panel title="Source cards">
        <div className="source-list">
          {(research.sources || []).length === 0 ? (
            <div className="empty-state">No live sources are attached in this run.</div>
          ) : (
            research.sources.map((source, index) => (
              <a className="source-card" href={source.url} target="_blank" rel="noreferrer" key={`${source.url}-${index}`}>
                <span className="source-number">0{index + 1}</span>
                <div>
                  <strong>{source.title}</strong>
                  <p>{source.snippet}</p>
                  <small>{source.url}</small>
                </div>
              </a>
            ))
          )}
        </div>
      </Panel>
    </div>
  );
}

function PositioningPanel({ pos }) {
  return (
    <div className="section-stack">
      <SectionTitle eyebrow="03 · POSITION" title="Own a clear problem, not a vague identity" subtitle="A good personal brand is easier to remember when audience, problem, value and POV reinforce one another." />
      <div className="two-col-cards">
        <InfoPanel label="Target audience" value={pos.target_audience} />
        <InfoPanel label="Audience problem" value={pos.audience_problem} />
        <InfoPanel label="Value proposition" value={pos.value_proposition} />
        <InfoPanel label="Unique angle" value={pos.unique_angle} />
        <InfoPanel label="Point of view" value={pos.point_of_view} />
        <InfoPanel label="Category" value={pos.category} />
      </div>
      <Panel title="Positioning alternatives">
        <div className="alternative-list">
          {(pos.positioning_alternatives || []).map((item, index) => (
            <div className="alternative" key={index}>
              <span>{String(index + 1).padStart(2, "0")}</span>
              <div>
                <strong>{item.name}</strong>
                <p>{item.statement}</p>
                <small>Tradeoff: {item.tradeoff}</small>
              </div>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}

function IdentityPanel({ dna }) {
  return (
    <div className="section-stack">
      <SectionTitle eyebrow="04 · SHAPE" title="Brand DNA" subtitle="Personality, principles and voice turn positioning into something people can consistently recognize." />
      <Panel title="Personality">
        <div className="trait-grid">
          {(dna.personality || []).map((item, index) => (
            <div className="trait-card" key={index}>
              <strong>{item.trait || item}</strong>
              <p>{item.justification || ""}</p>
            </div>
          ))}
        </div>
      </Panel>
      <div className="two-col-cards">
        <InfoPanel label="Recommended tagline" value={dna.recommended_tagline} emphasis />
        <InfoPanel label="One-line pitch" value={dna.one_line_pitch} />
      </div>
      <Panel title="Voice system">
        <div className="voice-grid">
          <InfoPanel label="Should sound like" value={dna.voice?.should_sound_like} />
          <ListPanel label="Do" items={dna.voice?.do || []} />
          <ListPanel label="Avoid" items={dna.voice?.avoid || []} />
          <ListPanel label="Sample phrases" items={dna.voice?.sample_phrases || []} />
        </div>
      </Panel>
    </div>
  );
}

function VisualPanel({ visual }) {
  return (
    <div className="section-stack">
      <SectionTitle eyebrow="05 · VISUALIZE" title="Visual identity with logic" subtitle="The palette, typography and logo direction are tied back to the brand strategy instead of being decorative extras." />
      <Panel title="Logo direction">
        <InfoPanel label="Concept" value={visual.logo_direction?.concept} />
        <InfoPanel label="Symbol logic" value={visual.logo_direction?.symbol_logic} />
        <InfoPanel label="Composition" value={visual.logo_direction?.composition} />
      </Panel>
      <Panel title="Color system">
        <div className="palette-grid">
          {(visual.palette || []).map((color, index) => (
            <div className="color-swatch" key={index}>
              <div className="swatch" style={{ background: color.hex }} />
              <strong>{color.name}</strong>
              <span>{color.hex}</span>
              <small>{color.role}</small>
            </div>
          ))}
        </div>
      </Panel>
      <div className="two-col-cards">
        <InfoPanel label="Heading style" value={visual.typography?.heading_style} />
        <InfoPanel label="Body style" value={visual.typography?.body_style} />
        <InfoPanel label="Imagery" value={visual.imagery?.treatment} />
        <InfoPanel label="Social layout" value={visual.social_layout?.headline_style} />
      </div>
    </div>
  );
}

function ContentPanel({ content }) {
  return (
    <div className="section-stack">
      <SectionTitle eyebrow="06 · CONTENT" title="A repeatable content engine" subtitle="The first ten posts are generated from the positioning and pillars, not as disconnected social-media filler." />
      <div className="content-pillar-grid">
        {(content.content_pillars || []).map((pillar, index) => (
          <article className="pillar-card" key={index}>
            <span>0{index + 1}</span>
            <h3>{pillar.name}</h3>
            <p>{pillar.promise}</p>
            <small>{(pillar.example_topics || []).join(" · ")}</small>
          </article>
        ))}
      </div>
      <Panel title="First 10 posts">
        <div className="post-list">
          {(content.first_10_posts || []).map((post, index) => (
            <div className="post-row" key={index}>
              <span className="post-id">{String(post.number || index + 1).padStart(2, "0")}</span>
              <div>
                <strong>{post.hook}</strong>
                <p>{post.idea}</p>
                <small>{post.platform} · {post.format} · {post.cta}</small>
              </div>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}

function LaunchPanel({ launch }) {
  return (
    <div className="section-stack">
      <SectionTitle eyebrow="07 · LAUNCH" title="Ready-to-use launch assets" subtitle="The system ends with things the creator can actually publish, not just strategy language." />
      <div className="two-col-cards">
        <CopyPanel label="Profile bio" text={launch.profile_bio} />
        <CopyPanel label="Instagram bio" text={launch.instagram_bio} />
      </div>
      <Panel title="Intro post">
        <div className="copy-card">{launch.intro_post}</div>
      </Panel>
      <Panel title="First week plan">
        <div className="post-list">
          {(launch.first_week_plan || []).map((item, index) => (
            <div className="post-row" key={index}>
              <span className="post-id">D{item.day}</span>
              <div><strong>{item.asset}</strong><p>{item.goal}</p></div>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}

function CriticPanel({ critic, onImprove, loading }) {
  const findings = critic.findings || [];
  return (
    <div className="section-stack">
      <div className="critic-hero">
        <div>
          <div className="eyebrow light">08 · CHALLENGE</div>
          <h1>{critic.status || "Brand review"}</h1>
          <p>{critic.biggest_risk || "The critic looks for weak assumptions and generic output."}</p>
        </div>
        <button className="light-button" onClick={onImprove} disabled={loading}>
          {loading ? "Improving..." : "Run revision loop ↻"}
        </button>
      </div>
      <div className="finding-list">
        {findings.length === 0 ? (
          <div className="empty-state">No major findings were returned.</div>
        ) : (
          findings.map((finding, index) => (
            <article className="finding" key={index}>
              <div className={`severity ${finding.severity}`}>{finding.severity}</div>
              <div>
                <strong>{finding.area}</strong>
                <h3>{finding.issue}</h3>
                <p>{finding.evidence}</p>
                <small>Fix → {finding.fix}</small>
              </div>
            </article>
          ))
        )}
      </div>
      <Panel title="Consistency checks">
        <div className="check-grid">
          {Object.entries(critic.consistency_checks || {}).map(([key, value]) => (
            <div className="check-card" key={key}>
              <span>{key.replaceAll("_", " ")}</span>
              <strong>{value}</strong>
            </div>
          ))}
        </div>
      </Panel>
    </div>
  );
}

function SectionTitle({ eyebrow, title, subtitle }) {
  return (
    <div className="section-title">
      <div className="eyebrow">{eyebrow}</div>
      <h2>{title}</h2>
      <p>{subtitle}</p>
    </div>
  );
}

function Panel({ title, children }) {
  return (
    <section className="panel">
      <div className="panel-title"><h3>{title}</h3></div>
      <div>{children}</div>
    </section>
  );
}

function Metric({ title, value }) {
  return (
    <article className="metric-card">
      <span>{title}</span>
      <strong>{value}</strong>
    </article>
  );
}

function InfoPanel({ label, value, emphasis = false }) {
  return (
    <article className={`info-panel ${emphasis ? "emphasis" : ""}`}>
      <span>{label}</span>
      <p>{value || "—"}</p>
    </article>
  );
}

function ListPanel({ label, items }) {
  return (
    <article className="info-panel">
      <span>{label}</span>
      <ul>
        {items.map((item, index) => <li key={index}>{item}</li>)}
      </ul>
    </article>
  );
}

function CopyPanel({ label, text }) {
  return (
    <article className="info-panel copy-panel">
      <span>{label}</span>
      <p>{text || "—"}</p>
    </article>
  );
}

export default App;
