import streamlit as st
import ollama
from PIL import Image
from io import BytesIO
from prompts import MESSAGE

st.set_page_config(
    page_title="LaTeX OCR with LLAMA",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("LaTeX OCR with LLAMA")

col1, col2 = st.columns(2)
with col2:
    if st.button("Clear 🕳️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
            st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract LaTeX code from images using Llama 3.2 Vision!</p>', unsafe_allow_html=True)

st.markdown("----------")

with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)
        if st.button("Extract LaTeX Code", type="primary"):
            with st.spinner("Extracting LaTeX code..."):
                try:
                    messages = [
                        {
                            'role': 'user',
                            'content': MESSAGE[0]['content'],
                            'images': [uploaded_file.getvalue()]
                        }
                    ]
                    response = ollama.chat(
                        model='llama3.2-vision',
                        messages=messages,
                        options={'temperature': 0.0, 'num_predict': 300}
                    )
                    raw_output = response['message']['content']
                    # Deduplicate repeated lines (model looping fix)
                    lines = raw_output.split('\n')
                    seen = []
                    for line in lines:
                        stripped = line.strip()
                        if stripped and stripped in [s.strip() for s in seen]:
                            break  # stop at first repeated line
                        seen.append(line)
                    st.session_state['ocr_result'] = '\n'.join(seen).strip()
                    # Close open environments if truncated
                    result = st.session_state['ocr_result']
                    for env in ['align*', 'align', 'equation*', 'equation']:
                        if r'\begin{' + env + '}' in result and r'\end{' + env + '}' not in result:
                            st.session_state['ocr_result'] = result + f'\n\\end{{{env}}}'
                            break
                except Exception as e:
                    st.error(f"An error occurred: {e}")


if 'ocr_result' in st.session_state:
    st.markdown("### Extracted LaTeX Code:")
    
    st.code(st.session_state['ocr_result'], language='latex')
    
    st.markdown("### Rendered Equation:")

    import re
    raw = st.session_state['ocr_result']
    # Fix unicode dashes
    raw = raw.replace('–', '-').replace('—', '-')
    # Strip document wrapper
    if r'\begin{document}' in raw:
        start = raw.find(r'\begin{document}') + len(r'\begin{document}')
        end = raw.find(r'\end{document}')
        raw = raw[start:end] if end != -1 else raw[start:]
    raw = raw.strip()
    # Fix broken \end{align } (spaces inside braces)
    raw = re.sub(r'\\end\{\s*(align\*?|equation\*?|gather\*?)\s*\}', lambda m: r'\end{' + m.group(1).strip() + '}', raw)
    # Remove duplicate/nested environment tags (e.g. \end{align} \end{align*})
    raw = re.sub(r'(\\end\{align\*?\})\s*\\end\{align\*?\}', r'\\end{align*}', raw)
    # Extract content inside the outermost environment
    env_match = re.search(r'\\begin\{(align\*?|equation\*?|gather\*?)\}(.*?)\\end\{\1\}', raw, re.DOTALL)
    if env_match:
        inner = env_match.group(2).strip()
        # Remove trailing incomplete lines (lines not ending with \\ or being the last)
        lines = [l for l in inner.split('\n') if l.strip()]
        cleaned_latex = r'\begin{align*}' + '\n' + '\n'.join(lines) + '\n' + r'\end{align*}'
        # resending it to model to fix any remaining issues
        try:
            response = ollama.chat(
                model='llama3.2-vision',
                messages=[{
                    'role': 'user',
                    'content': f"Here is the extracted LaTeX code:\n{cleaned_latex}\nPlease fix any syntax issues and output only the corrected LaTeX code without any explanations or extra text."
                }],
                options={'temperature': 0.0, 'num_predict': 300}
            )
            cleaned_latex = response['message']['content'].strip()

        except Exception as e:
            st.error(f"An error occurred during LaTeX cleanup: {e}")
    else:
        raw_clean = raw.replace(r'\[', '').replace(r'\]', '').strip()
        if r'\\' in raw_clean or '&' in raw_clean:
            cleaned_latex = r'\begin{align*}' + '\n' + raw_clean + '\n' + r'\end{align*}'
        else:
            cleaned_latex = raw_clean
            try:
                response = ollama.chat(
                    model='llama3.2-vision',
                    messages=[{
                        'role': 'user',
                        'content': f"Here is the extracted LaTeX code:\n{cleaned_latex}\nPlease fix any syntax issues and output only the corrected LaTeX code without any explanations or extra text."
                    }],
                    options={'temperature': 0.0, 'num_predict': 300}
                )
                cleaned_latex = response['message']['content'].strip()  
            except Exception as e:
                st.error(f"An error occurred during LaTeX cleanup: {e}")
    st.latex(cleaned_latex)

else:
     st.info("Upload an image and click 'Extract LaTeX' to see the results here.")

github_link = "https://github.com/mohdcodes"
linkedin_link = "https://www.linkedin.com/in/mohdcodes/"
st.markdown("----------")
st.markdown(f"Made by MOHD ARBAAZ - Data Science Engineer | Github:- {github_link} | LinkedIn:- {linkedin_link}")