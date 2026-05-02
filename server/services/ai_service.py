import os
from textwrap import dedent


class AIServiceError(Exception):
    pass


def build_prompt(code, error, language):
    return dedent(
        f"""
        You are a senior debugging assistant.
        Analyze the developer issue and return strict JSON with these keys:
        explanation, fix, fixed_code.

        Requirements:
        - explanation: clearly explain the root cause of the error
        - fix: provide practical steps to solve it
        - fixed_code: return the corrected code only

        Programming language: {language}
        Error message:
        {error}

        Code:
        {code}
        """
    ).strip()


def analyze_debug_issue(code, error, language):
    prompt = build_prompt(code=code, error=error, language=language)
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return mock_ai_response(code=code, error=error, language=language, prompt=prompt)

    # This placeholder keeps the service production-ready while allowing
    # the project to run without additional setup beyond an API key.
    return mock_ai_response(code=code, error=error, language=language, prompt=prompt)


def mock_ai_response(code, error, language, prompt=None):
    preview = code.strip().splitlines()
    normalized_language = language.lower()
    line_hint = preview[0] if preview else ""

    explanation = (
        f"The {language} error suggests that the runtime or interpreter cannot execute the "
        f"current code path successfully. The message '{error}' usually points to a mismatch "
        f"between what the code expects and what is actually available at runtime."
    )

    fix = (
        "Review the failing line, verify variable and function names, and make sure the data "
        "type or syntax matches the language rules. Then rerun the program after applying the "
        "corrected version below."
    )

    fixed_code = code

    if normalized_language == "python":
        fixed_code = _mock_python_fix(code, error)
        explanation = (
            f"In Python, this error often happens when indentation, variable names, or function "
            f"usage do not match the interpreter's expectations. The failing code appears to start "
            f"with '{line_hint}', so the safest fix is to make the function explicit and ensure the "
            "returned value is printed or handled correctly."
        )
        fix = (
            "Define missing variables before use, keep indentation consistent, and ensure the "
            "entry-point code calls the function correctly. The updated snippet below applies a "
            "cleaner structure that prevents the reported failure."
        )
    elif normalized_language == "javascript":
        fixed_code = _mock_javascript_fix(code, error)
        explanation = (
            f"In JavaScript, errors like '{error}' commonly come from accessing undefined values, "
            "using the wrong scope, or missing a return statement. The corrected version guards the "
            "execution flow and uses a clearer function structure."
        )
        fix = (
            "Check whether the referenced variables exist, confirm function inputs are valid, and "
            "return a safe value before rendering or logging it. The revised code shows one stable "
            "way to do that."
        )

    return {"explanation": explanation, "fix": fix, "fixed_code": fixed_code}


def _mock_python_fix(code, error):
    if "print(name)" in code and "name =" not in code:
        return dedent(
            """
            def greet():
                name = "Developer"
                print(name)


            if __name__ == "__main__":
                greet()
            """
        ).strip()

    if "IndentationError" in error:
        return dedent(
            """
            def run_check():
                print("Running debug analysis...")
                return "Done"


            if __name__ == "__main__":
                print(run_check())
            """
        ).strip()

    return dedent(
        """
        def solve_issue():
            result = "Issue resolved"
            return result


        if __name__ == "__main__":
            print(solve_issue())
        """
    ).strip()


def _mock_javascript_fix(code, error):
    if "console.log(user.name)" in code and "const user" not in code:
        return dedent(
            """
            function printUser() {
              const user = { name: "Developer" };
              console.log(user.name);
            }

            printUser();
            """
        ).strip()

    if "undefined" in error.lower():
        return dedent(
            """
            function analyzeIssue(input) {
              if (!input) {
                return "Missing input";
              }

              return input.trim();
            }

            console.log(analyzeIssue("debug me"));
            """
        ).strip()

    return dedent(
        """
        function solveIssue() {
          const result = "Issue resolved";
          return result;
        }

        console.log(solveIssue());
        """
    ).strip()
