MESSAGE = [{
    'role': 'user',
    'content': r"""Look at the mathematical equation in the image and output ONLY the raw LaTeX code for it.
Rules you MUST follow:
- Output ONLY the LaTeX equation code. Nothing else.
- NO \documentclass, NO \usepackage, NO \begin{document}, NO \end{document}.
- NO dollar signs ($) around the code.
- NO explanations, NO comments, NO extra text.
- Do NOT repeat any lines. Write each equation ONCE.
- Stop immediately after the equation is complete."""
}]
