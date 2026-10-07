import { useState, useEffect, useRef } from 'react'
import './App.css'
import DottedSurface from '@/components/ui/dotted-surface'

function App() {
  const [bgVisible, setBgVisible] = useState(false)
  const [authTab, setAuthTab] = useState('login')
  const punchlinesRef = useRef([])

  useEffect(() => {
    // Fade in background 3D effect after hero section renders
    const timer = setTimeout(() => {
      setBgVisible(true)
    }, 700)
    return () => clearTimeout(timer)
  }, [])

  useEffect(() => {
    // Intersection Observer for staggered scroll-reveal animations
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible')
          }
        })
      },
      { threshold: 0.25 }
    )

    punchlinesRef.current.forEach((el) => {
      if (el) observer.observe(el)
    })

    return () => observer.disconnect()
  }, [])

  const handleScrollToOptimize = () => {
    const el = document.getElementById('optimize-section')
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  }

  const handleScrollToAuth = () => {
    const el = document.getElementById('auth-section')
    if (el) el.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <div className="landing-page">
      <div className={`dotted-bg-wrapper ${bgVisible ? 'visible' : ''}`}>
        <DottedSurface />
      </div>

      {/* Top Header Navigation */}
      <header className="header animate-fade-in" style={{ paddingTop: '75px' }}></header>

      {/* Main Hero Section */}
      <main className="main-content">
        <div className="hero-container animate-hero">
          {/* Main Headline */}
          <div className="headline-wrapper">
            <h1 className="hero-title">
              <span className="whitespace-nowrap">
                <span className="electrify-wrapper">
                  <span>Electrify</span>
                  <span className="yellow-underline"></span>
                </span>
                {' '}your{' '}
                <span className="database-wrapper">
                  database
                  <img
                    src="/hero.png"
                    alt="Shinx mascot"
                    className="shinx-mascot"
                  />
                </span>
              </span>
              <br />
              <span className="inline">with </span>
              <span className="shinx-brand">Shinx</span>
            </h1>
          </div>

          {/* Install Widget */}
          <div className="install-widget-container">
            <div className="install-tabs-row">
              <div className="tab-install">INSTALL</div>
              <button className="btn-hop-in" onClick={handleScrollToAuth}>HOP IN</button>
              <a href="#" className="btn-docs">CHECK DOCUMENTATION</a>
            </div>
            <div className="code-box-container">
              <div className="code-box-inner">
                <div className="code-content">
                  <span className="code-prompt">$</span>
                  <span className="code-text">docker pull shinx && docker run shinx</span>
                </div>
                <button
                  className="copy-btn"
                  onClick={() => navigator.clipboard.writeText('docker pull shinx && docker run shinx')}
                >
                  <span className="material-symbols-outlined">content_copy</span>
                </button>
              </div>
            </div>
          </div>

          {/* Downward Scroll Arrow */}
          <div className="scroll-down-container">
            <button
              className="scroll-down-btn"
              onClick={handleScrollToOptimize}
              aria-label="Scroll to Optimize section"
            >
              <div className="scroll-arrow-circle">
                <span className="material-symbols-outlined scroll-arrow-icon">arrow_downward</span>
              </div>
            </button>
          </div>
        </div>

        {/* Curved Dome Section */}
        <div className="curved-dome-section" id="optimize-section">
          <div className="dome-content">
            {/* Subheader */}
            <div className="subheader-container">
              <h2 className="subheader">
                <span className="text-blue">Optimize</span>
                {' '}using{' '}
                <span className="ai-wrapper">
                  <span>AI</span>
                  <span className="yellow-underline-small"></span>
                </span>
              </h2>
            </div>

            {/* 3 Alternating Punchlines */}
            <div className="punchlines-container">
              {/* Punchline 1: Left Bracket */}
              <div
                className="punchline punchline-left animate-punchline"
                ref={(el) => (punchlinesRef.current[0] = el)}
              >
                <span className="card-number">01</span>
                <div className="bracket-wrapper bracket-left">
                  <div className="bracket-bar-vertical"></div>
                  <div className="bracket-bar-top"></div>
                  <div className="bracket-bar-bottom"></div>
                  <div className="punchline-text">Analyze</div>
                  <div className="punchline-text">Patterns</div>
                  <p className="punchline-desc">Continuous telemetry analysis detects slow queries and inefficient schema execution.</p>
                </div>
              </div>

              {/* Punchline 2: Right Bracket */}
              <div
                className="punchline punchline-right animate-punchline"
                ref={(el) => (punchlinesRef.current[1] = el)}
              >
                <div className="bracket-wrapper bracket-right">
                  <div className="bracket-bar-vertical"></div>
                  <div className="bracket-bar-top"></div>
                  <div className="bracket-bar-bottom"></div>
                  <div className="punchline-text">Shinx</div>
                  <div className="punchline-text">reviews your</div>
                  <div className="punchline-text">database</div>
                  <p className="punchline-desc">Automated AI index recommendations tune workloads without manual DBA overhead.</p>
                </div>
                <span className="card-number">02</span>
              </div>

              {/* Punchline 3: L-Bracket */}
              <div
                className="punchline punchline-left animate-punchline"
                ref={(el) => (punchlinesRef.current[2] = el)}
              >
                <span className="card-number">03</span>
                <div className="bracket-wrapper bracket-l">
                  <div className="bracket-bar-vertical"></div>
                  <div className="bracket-bar-horizontal"></div>
                  <div className="punchline-text">It is</div>
                  <div className="punchline-text">Electrified</div>
                  <p className="punchline-desc">Instant sub-millisecond query latency and zero-downtime database throughput.</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* ── Auth Section ──────────────────────────────────────── */}
        <section className="auth-section" id="auth-section">
          <div className="auth-section-inner">

            {/* Left: copy */}
            <div className="auth-section-copy">
              <h2 className="auth-section-heading">
                <span className="electrify-wrapper">
                  <span>Ready</span>
                  <span className="yellow-underline"></span>
                </span>{' '}
                to <span className="text-blue">electrify</span>?
              </h2>
              <p className="auth-section-desc">
                Connect your database in minutes. Shinx watches every query,
                recommends indexes, and tunes your workload — automatically.
              </p>
              <ul className="auth-perks">
                <li>
                  <span className="material-symbols-outlined perk-icon">bolt</span>
                  Sub-millisecond latency gains
                </li>
                <li>
                  <span className="material-symbols-outlined perk-icon">shield</span>
                  Zero-downtime tuning
                </li>
                <li>
                  <span className="material-symbols-outlined perk-icon">psychology</span>
                  AI-powered recommendations
                </li>
              </ul>
            </div>

            {/* Right: form card */}
            <div className="auth-card">

              {/* Tabs */}
              <div className="auth-tabs">
                <button
                  className={`auth-tab ${authTab === 'login' ? 'active' : ''}`}
                  onClick={() => setAuthTab('login')}
                >Log In</button>
                <button
                  className={`auth-tab ${authTab === 'register' ? 'active' : ''}`}
                  onClick={() => setAuthTab('register')}
                >Register</button>
              </div>

              {/* Login Form */}
              {authTab === 'login' && (
                <form className="auth-form" onSubmit={e => e.preventDefault()}>
                  <div className="auth-field">
                    <label className="auth-label" htmlFor="login-email">Email</label>
                    <input
                      id="login-email"
                      className="auth-input"
                      type="email"
                      placeholder="you@example.com"
                      autoComplete="email"
                    />
                  </div>
                  <div className="auth-field">
                    <label className="auth-label" htmlFor="login-password">Password</label>
                    <input
                      id="login-password"
                      className="auth-input"
                      type="password"
                      placeholder="••••••••"
                      autoComplete="current-password"
                    />
                  </div>
                  <div className="auth-forgot">
                    <a href="#" className="auth-link">Forgot password?</a>
                  </div>
                  <button type="submit" className="auth-submit">Log In</button>
                  <p className="auth-switch">
                    No account?{' '}
                    <button type="button" className="auth-link" onClick={() => setAuthTab('register')}>
                      Register here
                    </button>
                  </p>
                </form>
              )}

              {/* Register Form */}
              {authTab === 'register' && (
                <form className="auth-form" onSubmit={e => e.preventDefault()}>
                  <div className="auth-field">
                    <label className="auth-label" htmlFor="reg-name">Name</label>
                    <input
                      id="reg-name"
                      className="auth-input"
                      type="text"
                      placeholder="Your name"
                      autoComplete="name"
                    />
                  </div>
                  <div className="auth-field">
                    <label className="auth-label" htmlFor="reg-email">Email</label>
                    <input
                      id="reg-email"
                      className="auth-input"
                      type="email"
                      placeholder="you@example.com"
                      autoComplete="email"
                    />
                  </div>
                  <div className="auth-field">
                    <label className="auth-label" htmlFor="reg-password">Password</label>
                    <input
                      id="reg-password"
                      className="auth-input"
                      type="password"
                      placeholder="••••••••"
                      autoComplete="new-password"
                    />
                  </div>
                  <div className="auth-field">
                    <label className="auth-label" htmlFor="reg-confirm">Confirm Password</label>
                    <input
                      id="reg-confirm"
                      className="auth-input"
                      type="password"
                      placeholder="••••••••"
                      autoComplete="new-password"
                    />
                  </div>
                  <button type="submit" className="auth-submit">Create Account</button>
                  <p className="auth-switch">
                    Already have an account?{' '}
                    <button type="button" className="auth-link" onClick={() => setAuthTab('login')}>
                      Log in
                    </button>
                  </p>
                </form>
              )}

            </div>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="footer">
        <div className="footer-content">
          <div className="footer-grid">
            {/* Brand Column */}
            <div className="footer-col brand-col">
              <div className="brand-header">
                <img src="/hero.png" alt="Shinx logo" className="footer-mascot" />
                <span className="brand-name">SHINX</span>
              </div>
              <p className="brand-desc">The intelligent database optimization layer. Continuous query analysis, index recommendations, and automated performance tuning.</p>
            </div>

            {/* Product Column */}
            <div className="footer-col">
              <h3 className="footer-heading">Product</h3>
              <ul className="footer-links">
                <li><a href="#">Overview</a></li>
                <li><a href="#">Query Analyzer</a></li>
                <li><a href="#">Performance Index</a></li>
                <li><a href="#">Postgres & MySQL</a></li>
                <li><a href="#">Pricing</a></li>
              </ul>
            </div>

            {/* Resources Column */}
            <div className="footer-col">
              <h3 className="footer-heading">Resources</h3>
              <ul className="footer-links">
                <li><a href="#">Documentation</a></li>
                <li><a href="#">GitHub Repository</a></li>
                <li><a href="#">CLI Reference</a></li>
                <li><a href="#">Changelog</a></li>
                <li><a href="#">Community Discord</a></li>
              </ul>
            </div>

            {/* Legal Column */}
            <div className="footer-col">
              <h3 className="footer-heading">Legal & Trust</h3>
              <ul className="footer-links">
                <li><a href="#">Privacy Policy</a></li>
                <li><a href="#">Terms of Service</a></li>
                <li><a href="#">Security Architecture</a></li>
                <li><a href="#">System Status</a></li>
              </ul>
            </div>
          </div>

          {/* Footer Bottom Bar */}
          <div className="footer-bottom">
            <div className="copyright">© 2026 Shinx. All rights reserved.</div>
            <div className="footer-bottom-links">
              <a href="#" className="bottom-link">Privacy</a>
              <span className="link-divider">•</span>
              <a href="#" className="bottom-link">Terms</a>
              <span className="link-divider">•</span>
              <a href="#" className="bottom-link">Security</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
