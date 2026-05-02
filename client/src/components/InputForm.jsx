import React, { useState } from "react";

const languageOptions = ["Python", "JavaScript", "TypeScript", "Java", "C#"];

const sampleCode = `def greet_user():
print(name)
`;

const sampleError = `NameError: name 'name' is not defined`;

function InputForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    code: sampleCode,
    error: sampleError,
    language: "Python",
  });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(formData);
  };

  return (
    <form className="input-form" onSubmit={handleSubmit}>
      <label className="field">
        <span>Programming Language</span>
        <select
          name="language"
          value={formData.language}
          onChange={handleChange}
          disabled={loading}
        >
          {languageOptions.map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </label>

      <label className="field">
        <span>Code Snippet</span>
        <textarea
          name="code"
          value={formData.code}
          onChange={handleChange}
          placeholder="Paste the code that failed..."
          rows={12}
          disabled={loading}
        />
      </label>

      <label className="field">
        <span>Error Message</span>
        <textarea
          name="error"
          value={formData.error}
          onChange={handleChange}
          placeholder="Paste the exact error output..."
          rows={5}
          disabled={loading}
        />
      </label>

      <button className="button" type="submit" disabled={loading}>
        {loading ? "Analyzing..." : "Analyze"}
      </button>
    </form>
  );
}

export default InputForm;
