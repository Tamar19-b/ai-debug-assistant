import React, { useState } from "react";
import InputForm from "./components/InputForm.jsx";
import ResultDisplay from "./components/ResultDisplay.jsx";

const API_BASE_URL =
  import.meta.env.VITE_API_URL || (import.meta.env.DEV ? "http://localhost:5000" : "");

const initialResult = {
  explanation: "",
  fix: "",
  fixed_code: "",
};

function App() {
  const [result, setResult] = useState(initialResult);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleAnalyze = async (formValues) => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE_URL}/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formValues),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "The analysis request failed.");
      }

      setResult({
        explanation: data.explanation || "",
        fix: data.fix || "",
        fixed_code: data.fixed_code || "",
      });
    } catch (requestError) {
      setError(requestError.message || "Unable to analyze the issue.");
      setResult(initialResult);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <header className="hero">
        <div className="hero__content">
          <span className="eyebrow">Developer Productivity</span>
          <h1>AI Debug Assistant</h1>
          <p>
            Paste your code, add the error message, and get a focused explanation,
            a practical fix, and a cleaned-up version of the code.
          </p>
        </div>
      </header>

      <main className="layout">
        <section className="panel panel--form">
          <div className="section-heading">
            <h2>Analyze an Issue</h2>
            <p>Submit a failing snippet and let the assistant break it down.</p>
          </div>

          <InputForm onSubmit={handleAnalyze} loading={loading} />

          {error ? <div className="alert alert--error">{error}</div> : null}
        </section>

        <section className="panel panel--results">
          <div className="section-heading">
            <h2>Analysis Result</h2>
            <p>Readable output designed for quick debugging decisions.</p>
          </div>

          <ResultDisplay result={result} loading={loading} />
        </section>
      </main>
    </div>
  );
}

export default App;
