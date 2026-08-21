import os

from flask import Flask, render_template_string


app = Flask(__name__)


PAGE = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Veera Sir | Multi-Cloud DevOps CI/CD</title>
  <style>
    :root {
      --ink: #17212b;
      --muted: #5e6b78;
      --line: #d8e1ea;
      --paper: #f7fafc;
      --panel: #ffffff;
      --azure: #1478c8;
      --aws: #f39b21;
      --gcp: #29a260;
      --accent: #d83b5f;
      --deep: #243b53;
      --shadow: 0 18px 50px rgba(23, 33, 43, 0.14);
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      font-family: Inter, Segoe UI, Roboto, Arial, sans-serif;
      color: var(--ink);
      background: var(--paper);
      line-height: 1.55;
    }

    a {
      color: inherit;
      text-decoration: none;
    }

    .topbar {
      position: sticky;
      top: 0;
      z-index: 20;
      border-bottom: 1px solid rgba(216, 225, 234, 0.85);
      background: rgba(247, 250, 252, 0.92);
      backdrop-filter: blur(14px);
    }

    .nav {
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
      min-height: 72px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 20px;
    }

    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
      font-weight: 800;
      letter-spacing: 0;
    }

    .brand-mark {
      width: 44px;
      height: 44px;
      display: grid;
      place-items: center;
      border-radius: 8px;
      color: #fff;
      background: linear-gradient(135deg, var(--azure), var(--gcp));
      box-shadow: 0 10px 24px rgba(20, 120, 200, 0.26);
    }

    .links {
      display: flex;
      align-items: center;
      gap: 6px;
      color: var(--muted);
      font-size: 0.95rem;
      font-weight: 700;
    }

    .links a {
      padding: 10px 12px;
      border-radius: 7px;
    }

    .links a:hover {
      background: #eaf1f7;
      color: var(--ink);
    }

    .hero {
      overflow: hidden;
      background:
        linear-gradient(115deg, rgba(23, 33, 43, 0.92), rgba(36, 59, 83, 0.76)),
        url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='1400' height='760' viewBox='0 0 1400 760'%3E%3Crect width='1400' height='760' fill='%23243b53'/%3E%3Cg fill='none' stroke='%23ffffff' stroke-opacity='.25' stroke-width='2'%3E%3Cpath d='M123 174h180v104H123zM455 110h220v126H455zM835 160h190v108H835zM1092 96h182v118h-182zM210 456h220v126H210zM610 410h230v130H610zM1005 430h240v124h-240z'/%3E%3Cpath d='M303 226h152M675 173h160M1025 211h67M430 520h180M840 475h165M565 236v174M1168 214v216'/%3E%3Ccircle cx='303' cy='226' r='9' fill='%23f39b21' stroke='none'/%3E%3Ccircle cx='675' cy='173' r='9' fill='%231478c8' stroke='none'/%3E%3Ccircle cx='1025' cy='211' r='9' fill='%2329a260' stroke='none'/%3E%3Ccircle cx='610' cy='475' r='9' fill='%23d83b5f' stroke='none'/%3E%3Ccircle cx='1005' cy='475' r='9' fill='%23f39b21' stroke='none'/%3E%3C/g%3E%3Cg fill='%23ffffff' fill-opacity='.08'%3E%3Crect x='76' y='72' width='190' height='18' rx='4'/%3E%3Crect x='76' y='105' width='128' height='18' rx='4'/%3E%3Crect x='1092' y='614' width='210' height='18' rx='4'/%3E%3Crect x='1134' y='650' width='132' height='18' rx='4'/%3E%3C/g%3E%3C/svg%3E");
      background-size: cover;
      background-position: center;
      color: #fff;
    }

    .hero-inner {
      width: min(1180px, calc(100% - 32px));
      min-height: calc(100vh - 72px);
      margin: 0 auto;
      padding: 84px 0 54px;
      display: grid;
      grid-template-columns: minmax(0, 1.05fr) minmax(320px, 0.95fr);
      align-items: center;
      gap: 48px;
    }

    .eyebrow {
      width: fit-content;
      padding: 7px 11px;
      border: 1px solid rgba(255, 255, 255, 0.26);
      border-radius: 7px;
      background: rgba(255, 255, 255, 0.08);
      font-size: 0.78rem;
      font-weight: 800;
      text-transform: uppercase;
      letter-spacing: 0;
    }

    h1 {
      max-width: 760px;
      margin: 18px 0 16px;
      font-size: clamp(2.4rem, 6vw, 5.9rem);
      line-height: 0.97;
      letter-spacing: 0;
    }

    .hero p {
      max-width: 720px;
      margin: 0;
      color: rgba(255, 255, 255, 0.82);
      font-size: clamp(1rem, 2vw, 1.2rem);
    }

    .hero-actions {
      display: flex;
      flex-wrap: wrap;
      gap: 12px;
      margin-top: 30px;
    }

    .button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 46px;
      padding: 0 18px;
      border-radius: 7px;
      font-weight: 800;
      border: 1px solid rgba(255, 255, 255, 0.25);
    }

    .button.primary {
      color: var(--ink);
      background: #fff;
    }

    .button.secondary {
      color: #fff;
      background: rgba(255, 255, 255, 0.08);
    }

    .console {
      border: 1px solid rgba(255, 255, 255, 0.2);
      border-radius: 8px;
      overflow: hidden;
      background: rgba(10, 17, 24, 0.78);
      box-shadow: var(--shadow);
    }

    .console-head {
      display: flex;
      gap: 7px;
      padding: 14px 16px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.12);
      background: rgba(255, 255, 255, 0.06);
    }

    .dot {
      width: 11px;
      height: 11px;
      border-radius: 50%;
      background: var(--accent);
    }

    .dot:nth-child(2) {
      background: var(--aws);
    }

    .dot:nth-child(3) {
      background: var(--gcp);
    }

    .console-body {
      padding: 22px;
      font-family: Consolas, Monaco, monospace;
      font-size: 0.95rem;
      color: #dceaf7;
    }

    .line {
      display: flex;
      gap: 12px;
      padding: 8px 0;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .line:last-child {
      border-bottom: 0;
    }

    .prompt {
      color: #70d6a9;
      flex: 0 0 auto;
    }

    section {
      padding: 78px 0;
    }

    .wrap {
      width: min(1180px, calc(100% - 32px));
      margin: 0 auto;
    }

    .section-title {
      max-width: 760px;
      margin-bottom: 32px;
    }

    .section-title h2 {
      margin: 0 0 10px;
      font-size: clamp(2rem, 4vw, 3.1rem);
      line-height: 1.05;
      letter-spacing: 0;
    }

    .section-title p {
      margin: 0;
      color: var(--muted);
      font-size: 1.06rem;
    }

    .cloud-grid {
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 18px;
    }

    .card {
      min-height: 230px;
      padding: 24px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      box-shadow: 0 10px 30px rgba(23, 33, 43, 0.06);
    }

    .cloud-logo {
      width: 52px;
      height: 52px;
      display: grid;
      place-items: center;
      border-radius: 8px;
      color: #fff;
      font-weight: 900;
      margin-bottom: 18px;
    }

    .azure {
      background: var(--azure);
    }

    .aws {
      background: var(--aws);
    }

    .gcp {
      background: var(--gcp);
    }

    .card h3 {
      margin: 0 0 8px;
      font-size: 1.3rem;
    }

    .card p {
      margin: 0;
      color: var(--muted);
    }

    .pipeline {
      background: #fff;
      border-block: 1px solid var(--line);
    }

    .steps {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 12px;
      align-items: stretch;
    }

    .step {
      position: relative;
      min-height: 170px;
      padding: 22px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #f9fbfd;
    }

    .step strong {
      display: block;
      color: var(--azure);
      font-size: 0.84rem;
      text-transform: uppercase;
      letter-spacing: 0;
      margin-bottom: 10px;
    }

    .step h3 {
      margin: 0 0 8px;
      font-size: 1.1rem;
    }

    .step p {
      margin: 0;
      color: var(--muted);
      font-size: 0.94rem;
    }

    .tool-belt {
      display: grid;
      grid-template-columns: 0.8fr 1.2fr;
      gap: 28px;
      align-items: start;
    }

    .mentor-panel {
      padding: 30px;
      border-radius: 8px;
      color: #fff;
      background: linear-gradient(135deg, var(--deep), #0f766e);
      box-shadow: var(--shadow);
    }

    .mentor-panel h2 {
      margin: 0 0 12px;
      font-size: clamp(1.8rem, 3vw, 2.7rem);
      line-height: 1.1;
    }

    .mentor-panel p {
      color: rgba(255, 255, 255, 0.83);
      margin: 0 0 22px;
    }

    .badges {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
    }

    .badge {
      padding: 9px 11px;
      border-radius: 7px;
      background: rgba(255, 255, 255, 0.12);
      font-weight: 800;
      font-size: 0.9rem;
    }

    .tool-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 14px;
    }

    .tool {
      display: flex;
      gap: 14px;
      align-items: flex-start;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
    }

    .tool-icon {
      width: 38px;
      height: 38px;
      display: grid;
      place-items: center;
      flex: 0 0 auto;
      border-radius: 8px;
      color: #fff;
      background: var(--accent);
      font-weight: 900;
    }

    .tool h3 {
      margin: 0 0 4px;
      font-size: 1.02rem;
    }

    .tool p {
      margin: 0;
      color: var(--muted);
      font-size: 0.94rem;
    }

    .metrics {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 16px;
      margin-top: 36px;
    }

    .metric {
      padding: 22px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
    }

    .metric b {
      display: block;
      font-size: 2rem;
      line-height: 1;
      color: var(--deep);
    }

    .metric span {
      display: block;
      margin-top: 8px;
      color: var(--muted);
      font-weight: 700;
    }

    .cta {
      color: #fff;
      background: var(--ink);
    }

    .cta-box {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 24px;
      align-items: center;
    }

    .cta h2 {
      margin: 0 0 8px;
      font-size: clamp(2rem, 4vw, 3.4rem);
      line-height: 1.04;
    }

    .cta p {
      margin: 0;
      max-width: 780px;
      color: rgba(255, 255, 255, 0.76);
    }

    footer {
      padding: 24px 0;
      color: var(--muted);
      background: #eef3f8;
      border-top: 1px solid var(--line);
      text-align: center;
      font-weight: 700;
    }

    @media (max-width: 900px) {
      .links {
        display: none;
      }

      .hero-inner,
      .tool-belt,
      .cta-box {
        grid-template-columns: 1fr;
      }

      .hero-inner {
        min-height: auto;
      }

      .cloud-grid,
      .steps,
      .metrics {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 620px) {
      .nav {
        min-height: 64px;
      }

      .brand span {
        max-width: 210px;
      }

      .hero-inner {
        padding: 56px 0 36px;
      }

      .cloud-grid,
      .steps,
      .tool-grid,
      .metrics {
        grid-template-columns: 1fr;
      }

      section {
        padding: 56px 0;
      }
    }
  </style>
</head>
<body>
  <header class="topbar">
    <nav class="nav" aria-label="Primary">
      <a class="brand" href="#home">
        <span class="brand-mark">VS</span>
        <span>Veera Sir Multi-Cloud DevOps</span>
      </a>
      <div class="links">
        <a href="#clouds">Clouds</a>
        <a href="#pipeline">CI/CD</a>
        <a href="#tools">Tools</a>
        <a href="#mentor">Mentor</a>
      </div>
    </nav>
  </header>

  <main id="home">
    <section class="hero">
      <div class="hero-inner">
        <div>
          <div class="eyebrow">Azure CI/CD live deployment</div>
          <h1>Multi-Cloud DevOps, delivered with confidence.</h1>
          <p>
            A complete DevOps learning and delivery hub by Veera Sir, connecting
            Azure, AWS, GCP, Docker, Kubernetes, Terraform, monitoring, security,
            and automated CI/CD into one production-ready workflow.
          </p>
          <div class="hero-actions">
            <a class="button primary" href="#pipeline">Explore Pipeline</a>
            <a class="button secondary" href="#clouds">View Multi-Cloud Stack</a>
          </div>
        </div>

        <div class="console" aria-label="Deployment console preview">
          <div class="console-head">
            <span class="dot"></span>
            <span class="dot"></span>
            <span class="dot"></span>
          </div>
          <div class="console-body">
            <div class="line"><span class="prompt">$</span><span>git push origin main</span></div>
            <div class="line"><span class="prompt">1</span><span>Azure Pipeline validates code and tests</span></div>
            <div class="line"><span class="prompt">2</span><span>Docker image builds and pushes to ACR</span></div>
            <div class="line"><span class="prompt">3</span><span>VM pulls latest image and restarts safely</span></div>
            <div class="line"><span class="prompt">OK</span><span>Release live across DevOps environment</span></div>
          </div>
        </div>
      </div>
    </section>

    <section id="clouds">
      <div class="wrap">
        <div class="section-title">
          <h2>One DevOps mindset across every cloud.</h2>
          <p>
            Learn practical patterns that work in real environments: source control,
            image registries, infrastructure automation, runtime platforms, and
            observability across major cloud providers.
          </p>
        </div>

        <div class="cloud-grid">
          <article class="card">
            <div class="cloud-logo azure">AZ</div>
            <h3>Microsoft Azure</h3>
            <p>Azure DevOps, ACR, Azure VM, App Service, AKS, Key Vault, Monitor, and secure release automation.</p>
          </article>
          <article class="card">
            <div class="cloud-logo aws">AWS</div>
            <h3>Amazon Web Services</h3>
            <p>CodePipeline, ECR, EC2, ECS, EKS, IAM, CloudWatch, load balancers, and scalable deployments.</p>
          </article>
          <article class="card">
            <div class="cloud-logo gcp">GCP</div>
            <h3>Google Cloud</h3>
            <p>Cloud Build, Artifact Registry, Compute Engine, GKE, service accounts, logging, and release controls.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="pipeline" id="pipeline">
      <div class="wrap">
        <div class="section-title">
          <h2>CI/CD pipeline from commit to production.</h2>
          <p>
            Every release follows a clear path: validate, package, secure, deploy,
            and observe. This keeps delivery fast without losing discipline.
          </p>
        </div>

        <div class="steps">
          <article class="step">
            <strong>Stage 01</strong>
            <h3>Source</h3>
            <p>Developers push clean code to Git with branch strategy and review discipline.</p>
          </article>
          <article class="step">
            <strong>Stage 02</strong>
            <h3>Build</h3>
            <p>Pipeline installs dependencies, runs checks, and creates a versioned artifact.</p>
          </article>
          <article class="step">
            <strong>Stage 03</strong>
            <h3>Containerize</h3>
            <p>Docker packages the app into a repeatable image and pushes it to a registry.</p>
          </article>
          <article class="step">
            <strong>Stage 04</strong>
            <h3>Release</h3>
            <p>Automated deployment updates servers or clusters with minimal downtime.</p>
          </article>
          <article class="step">
            <strong>Stage 05</strong>
            <h3>Observe</h3>
            <p>Metrics, logs, alerts, and rollback plans keep the application dependable.</p>
          </article>
        </div>
      </div>
    </section>

    <section id="tools">
      <div class="wrap tool-belt">
        <aside class="mentor-panel" id="mentor">
          <h2>Guided by Veera Sir.</h2>
          <p>
            Training focused on real project delivery, interview confidence, and
            hands-on DevOps habits that students can use in live cloud environments.
          </p>
          <div class="badges">
            <span class="badge">Live Projects</span>
            <span class="badge">Docker</span>
            <span class="badge">Kubernetes</span>
            <span class="badge">Terraform</span>
            <span class="badge">Azure DevOps</span>
          </div>
        </aside>

        <div class="tool-grid">
          <article class="tool">
            <div class="tool-icon">G</div>
            <div>
              <h3>Git and GitHub</h3>
              <p>Branching, pull requests, tags, release notes, and source governance.</p>
            </div>
          </article>
          <article class="tool">
            <div class="tool-icon">D</div>
            <div>
              <h3>Docker and ACR</h3>
              <p>Clean images, registry pushes, version tags, and repeatable deployments.</p>
            </div>
          </article>
          <article class="tool">
            <div class="tool-icon">K</div>
            <div>
              <h3>Kubernetes</h3>
              <p>Pods, services, ingress, autoscaling, rolling updates, and health probes.</p>
            </div>
          </article>
          <article class="tool">
            <div class="tool-icon">T</div>
            <div>
              <h3>Terraform</h3>
              <p>Infrastructure as code for repeatable networks, compute, IAM, and policies.</p>
            </div>
          </article>
          <article class="tool">
            <div class="tool-icon">S</div>
            <div>
              <h3>DevSecOps</h3>
              <p>Secrets, scanning, least privilege, approvals, and secure deployment gates.</p>
            </div>
          </article>
          <article class="tool">
            <div class="tool-icon">M</div>
            <div>
              <h3>Monitoring</h3>
              <p>Dashboards, alerts, logs, traces, uptime checks, and incident response.</p>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section>
      <div class="wrap">
        <div class="section-title">
          <h2>Built for real-world DevOps outcomes.</h2>
          <p>
            The website running here is itself deployed through Azure CI/CD: code
            changes become a container image, the image moves to Azure Container
            Registry, and the Azure VM runs the latest release.
          </p>
        </div>
        <div class="metrics">
          <div class="metric"><b>3</b><span>Major clouds</span></div>
          <div class="metric"><b>5</b><span>Pipeline stages</span></div>
          <div class="metric"><b>24/7</b><span>Monitoring focus</span></div>
          <div class="metric"><b>100%</b><span>Hands-on learning</span></div>
        </div>
      </div>
    </section>

    <section class="cta">
      <div class="wrap cta-box">
        <div>
          <h2>Learn, build, automate, and deploy.</h2>
          <p>
            From a simple Flask app to enterprise-grade multi-cloud pipelines,
            Veera Sir's DevOps approach turns practice into production skill.
          </p>
        </div>
        <a class="button primary" href="#home">Back to Top</a>
      </div>
    </section>
  </main>

  <footer>
    Multi-Cloud DevOps CI/CD Website by Veera Sir | Powered by Azure DevOps, Docker, ACR, and Azure VM
  </footer>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(PAGE)


@app.route("/health")
def health():
    return {"status": "healthy", "service": "multicloud-devops-cicd"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "80"))
    app.run(host="0.0.0.0", port=port)
