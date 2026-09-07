import { useEffect, useState } from "react";
import { Activity, ArrowRight, BarChart3, Brain, CheckCircle2, CircleAlert, Database, ShieldCheck, Target } from "lucide-react";
import { getHealth, getStudentAnalytics, type StudentAnalytics } from "./api";

const emptyAnalytics: StudentAnalytics = {
  live_data: false,
  overall_readiness: null,
  assessed_skills: 0,
  critical_gaps: 0,
  skills: [],
  message: "No live data available yet. Connect the API and complete an assessment to begin."
};

function App() {
  const [analytics, setAnalytics] = useState<StudentAnalytics>(emptyAnalytics);
  const [apiStatus, setApiStatus] = useState("Checking API");

  useEffect(() => {
    void getHealth()
      .then((health) => {
        setApiStatus(`${health.api} / database ${health.database}`);
        if (health.database !== "healthy") {
          setAnalytics((current) => ({
            ...current,
            message: "FastAPI is running, but DATABASE_URL is not configured. Add your Supabase PostgreSQL URL to backend/.env.",
          }));
          return;
        }
        return getStudentAnalytics()
          .then(setAnalytics)
          .catch((error: Error) => {
            setAnalytics((current) => ({
              ...current,
              message: error.message.includes("401")
                ? "Sign in to load your competency details."
                : "Unable to load competency details from the backend.",
            }));
          });
      })
      .catch(() => setApiStatus("API unavailable / start FastAPI on port 8000"));
  }, []);

  const readiness = analytics.overall_readiness === null ? "--" : `${analytics.overall_readiness}%`;

  return (
    <main className="app-shell">
      <nav className="topbar">
        <a className="brand" href="/">Competency<span>IQ</span></a>
        <div className="nav-status"><span className="status-dot" /> {apiStatus}</div>
        <button className="outline-button">Sign in <ArrowRight size={16} /></button>
      </nav>
      <section className="hero-grid">
        <div className="hero-copy">
          <p className="eyebrow">WORKFORCE READINESS INTELLIGENCE</p>
          <h1>Turn capability into <em>direction.</em></h1>
          <p className="hero-lede">CompetencyIQ connects assessment evidence to the next skill, program, or policy decision that matters.</p>
          <div className="hero-actions"><button className="primary-button">Start assessment <ArrowRight size={18} /></button><button className="text-button">Explore the platform</button></div>
          <div className="trust-row"><ShieldCheck size={17} /> Backend-calculated insights <span /> <Database size={17} /> PostgreSQL source of truth</div>
        </div>
        <aside className="readiness-panel">
          <div className="panel-topline"><span>STUDENT READINESS</span><span className={analytics.live_data ? "live-badge" : "pending-badge"}>{analytics.live_data ? "LIVE DATA" : "AWAITING DATA"}</span></div>
          <div className="readiness-score">{readiness}<small>overall</small></div>
          <div className="meter"><span style={{ width: `${analytics.overall_readiness ?? 0}%` }} /></div>
          <div className="panel-stats"><div><strong>{analytics.assessed_skills}</strong><span>skills assessed</span></div><div><strong>{analytics.critical_gaps}</strong><span>critical gaps</span></div></div>
          {!analytics.live_data && <div className="empty-note"><CircleAlert size={17} /> {analytics.message}</div>}
        </aside>
      </section>
      <section className="workspace-section">
        <div className="section-heading"><div><p className="eyebrow">YOUR COMPETENCY PROFILE</p><h2>See what the evidence says.</h2></div><button className="icon-button" aria-label="View analytics"><BarChart3 size={19} /></button></div>
        <div className="skill-grid">
          {analytics.skills.length ? analytics.skills.map((skill) => <div className="skill-card" key={skill.name}><div className="skill-card-heading"><span>{skill.name}</span><strong>{skill.score}%</strong></div><div className="meter"><span style={{ width: `${skill.score}%` }} /></div></div>) : <div className="empty-profile"><Brain size={28} /><div><strong>Your profile will appear here</strong><p>Assessment results, gaps, and recommendations are loaded from the backend.</p></div></div>}
        </div>
      </section>
      <section className="feature-strip"><div><Target size={21} /><strong>Skills, not just scores</strong><span>Translate assessment evidence into targeted action.</span></div><div><Activity size={21} /><strong>Progress that compounds</strong><span>Reassess and see how your readiness changes.</span></div><div><CheckCircle2 size={21} /><strong>Trustworthy by design</strong><span>Empty database means empty state, never invented numbers.</span></div></section>
      <footer><span>CompetencyIQ</span><span>Student platform MVP · {new Date().getFullYear()}</span></footer>
    </main>
  );
}

export default App;
