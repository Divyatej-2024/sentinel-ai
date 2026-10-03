export default function Home() {
  return <main className="shell">
    <header><span className="mark">S</span><span>SENTINEL<span className="accent">AI</span></span><span className="badge">DEVELOPMENT</span></header>
    <section className="hero">
      <p className="eyebrow">SECURITY OPERATIONS PLATFORM</p>
      <h1>Security events,<br /><span>made actionable.</span></h1>
      <p className="intro">The SentinelAI event foundation is online. Ingestion and investigation views will grow here as the platform develops.</p>
      <a href={`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/api/docs`}>Explore the API <span aria-hidden="true">↗</span></a>
    </section>
    <footer><span>EVENT PIPELINE</span><span className="status"><i /> API documentation available</span><span>PHASE 01 / FOUNDATION</span></footer>
  </main>;
}
