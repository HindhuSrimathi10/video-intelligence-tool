import { useState } from "react";
import axios from "axios";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [companyName, setCompanyName] = useState("");
  const [competitors, setCompetitors] = useState(["", "", "", ""]);
  const [loading, setLoading] = useState(false);
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const [step, setStep] = useState("form");

  const handleCompetitorChange = (index, value) => {
    const updated = [...competitors];
    updated[index] = value;
    setCompetitors(updated);
  };

  const handleSubmit = async () => {
    if (!companyName.trim()) {
      setError("Please enter your company name");
      return;
    }
    const filteredCompetitors = competitors.filter((c) => c.trim() !== "");
    if (filteredCompetitors.length === 0) {
      setError("Please enter at least one competitor");
      return;
    }

    setLoading(true);
    setError(null);
    setStep("loading");

    try {
      const response = await axios.post(`${API_URL}/generate-report`, {
        company_name: companyName,
        competitors: filteredCompetitors,
      });

      if (response.data.success) {
        setReport(response.data);
        setStep("report");
      } else {
        setError("Failed to generate report. Please try again.");
        setStep("form");
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong. Make sure the backend is running.");
      setStep("form");
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = async () => {
    try {
      const filename = report.pptx_filename;
      const response = await axios.get(`${API_URL}/download-report/${filename}`, {
        responseType: "blob",
      });
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (err) {
      setError("Failed to download report. Please try again.");
    }
  };

  const handleReset = () => {
    setCompanyName("");
    setCompetitors(["", "", "", ""]);
    setReport(null);
    setError(null);
    setStep("form");
  };

  const formatNumber = (num) => {
    if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
    if (num >= 1000) return (num / 1000).toFixed(1) + "K";
    return num?.toString() || "0";
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <span className="logo-icon">▶</span>
            <span className="logo-text">VideoIntel</span>
          </div>
          <p className="header-subtitle">AI-Powered Video Competitor Intelligence</p>
        </div>
      </header>

      <main className="main">
        {/* FORM STEP */}
        {step === "form" && (
          <div className="form-container">
            <div className="form-header">
              <h1 className="form-title">Generate Your Competitor Report</h1>
              <p className="form-desc">
                Enter your company and up to 4 competitors. We'll analyze their
                YouTube presence and generate a full PowerPoint report.
              </p>
            </div>

            {error && <div className="error-box">⚠️ {error}</div>}

            <div className="form-card">
              <div className="input-group">
                <label className="input-label">Your Company Name</label>
                <input
                  className="input-field primary-input"
                  type="text"
                  placeholder="e.g. MrBeast, Nike, Apple..."
                  value={companyName}
                  onChange={(e) => setCompanyName(e.target.value)}
                />
              </div>

              <div className="divider">
                <span>VS</span>
              </div>

              <div className="input-group">
                <label className="input-label">Competitors (up to 4)</label>
                <div className="competitors-grid">
                  {competitors.map((comp, index) => (
                    <input
                      key={index}
                      className="input-field"
                      type="text"
                      placeholder={`Competitor ${index + 1}`}
                      value={comp}
                      onChange={(e) => handleCompetitorChange(index, e.target.value)}
                    />
                  ))}
                </div>
              </div>

              <button className="submit-btn" onClick={handleSubmit}>
                <span>🚀</span>
                <span>Generate Intelligence Report</span>
              </button>
            </div>

            <div className="features-row">
              <div className="feature-item">
                <span className="feature-icon">📊</span>
                <span>Real YouTube Data</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">🤖</span>
                <span>AI-Powered Insights</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">📑</span>
                <span>PowerPoint Export</span>
              </div>
              <div className="feature-item">
                <span className="feature-icon">⚡</span>
                <span>10+ Slide Report</span>
              </div>
            </div>
          </div>
        )}

        {/* LOADING STEP */}
        {step === "loading" && (
          <div className="loading-container">
            <div className="loading-card">
              <div className="spinner"></div>
              <h2 className="loading-title">Generating Your Report</h2>
              <div className="loading-steps">
                <div className="loading-step active">
                  <span className="step-icon">📡</span>
                  <span>Fetching YouTube data for all companies...</span>
                </div>
                <div className="loading-step active">
                  <span className="step-icon">🤖</span>
                  <span>Analyzing data with AI...</span>
                </div>
                <div className="loading-step active">
                  <span className="step-icon">📊</span>
                  <span>Building PowerPoint report...</span>
                </div>
              </div>
              <p className="loading-note">This may take 30-60 seconds. Please wait...</p>
            </div>
          </div>
        )}

        {/* REPORT STEP */}
        {step === "report" && report && (
          <div className="report-container">
            <div className="report-header">
              <div>
                <h1 className="report-title">✅ Report Ready!</h1>
                <p className="report-subtitle">
                  Analysis complete for {Object.keys(report.report_data).length} companies
                </p>
              </div>
              <div className="report-actions">
                <button className="download-btn" onClick={handleDownload}>
                  ⬇️ Download PowerPoint
                </button>
                <button className="reset-btn" onClick={handleReset}>
                  🔄 New Report
                </button>
              </div>
            </div>

            {/* Company Cards */}
            <div className="companies-grid">
              {Object.entries(report.report_data).map(([company, data], index) => {
                const stats = data.channel_stats || {};
                const colors = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#a855f7"];
                const color = colors[index % colors.length];
                return (
                  <div className="company-card" key={company} style={{ borderTopColor: color }}>
                    <div className="company-card-header">
                      <h3 className="company-name" style={{ color }}>
                        {company}
                      </h3>
                      {index === 0 && <span className="badge">Your Company</span>}
                    </div>
                    {data.error ? (
                      <p className="error-text">⚠️ {data.error}</p>
                    ) : (
                      <div className="stats-grid">
                        <div className="stat-item">
                          <span className="stat-value">
                            {formatNumber(stats.subscriber_count || 0)}
                          </span>
                          <span className="stat-label">Subscribers</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-value">
                            {formatNumber(stats.total_videos || 0)}
                          </span>
                          <span className="stat-label">Videos</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-value">
                            {formatNumber(data.avg_views || 0)}
                          </span>
                          <span className="stat-label">Avg Views</span>
                        </div>
                        <div className="stat-item">
                          <span className="stat-value">
                            {formatNumber(stats.total_views || 0)}
                          </span>
                          <span className="stat-label">Total Views</span>
                        </div>
                      </div>
                    )}
                    <div className="freq-badge">
                      📅 {data.upload_frequency || "N/A"}
                    </div>
                    {data.top_video && (
                      <div className="top-video">
                        <span className="top-video-label">🏆 Top Video:</span>
                        <span className="top-video-title">
                          {data.top_video.title?.substring(0, 60)}...
                        </span>
                        <span className="top-video-views">
                          {formatNumber(data.top_video.view_count)} views
                        </span>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            {/* AI Insights */}
            <div className="insights-card">
              <h2 className="insights-title">🤖 AI Analysis & Insights</h2>
              <div className="insights-content">
                <pre className="insights-text">{report.insights}</pre>
              </div>
            </div>

            <div className="download-section">
              <h3>Ready to present to your client?</h3>
              <p>Download the full professional PowerPoint report with charts and visualizations.</p>
              <button className="download-btn-large" onClick={handleDownload}>
                ⬇️ Download Full PowerPoint Report (.pptx)
              </button>
            </div>
          </div>
        )}
      </main>

      <footer className="footer">
        <p>VideoIntel — AI-Powered Video Competitor Intelligence Tool</p>
      </footer>
    </div>
  );
}

export default App;