import React from "react";

function ResultCard({ title, content, isCode = false }) {
  return (
    <article className="result-card">
      <h3>{title}</h3>
      {content ? (
        isCode ? <pre>{content}</pre> : <p>{content}</p>
      ) : (
        <p className="placeholder">Your analysis result will appear here.</p>
      )}
    </article>
  );
}

function ResultDisplay({ result, loading }) {
  if (loading) {
    return (
      <div className="loading-state">
        <div className="loader" />
        <p>Analyzing the error and preparing a cleaner fix...</p>
      </div>
    );
  }

  return (
    <div className="result-grid">
      <ResultCard title="Explanation" content={result.explanation} />
      <ResultCard title="Fix" content={result.fix} />
      <ResultCard title="Fixed Code" content={result.fixed_code} isCode />
    </div>
  );
}

export default ResultDisplay;
