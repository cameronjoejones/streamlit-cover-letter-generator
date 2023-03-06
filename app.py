import streamlit as st
import openai

st.set_page_config(page_title="Home Page", page_icon=":lemon:", layout="centered")

hide_menu_style = "<style> footer {visibility: hidden;} </style>"
st.markdown(hide_menu_style, unsafe_allow_html=True)

st.title("👩🏼‍💻 Cover Letter Generator")

class OpenAI_API:
    def __init__(self, api_key):
        self.api_key = api_key

    def __enter__(self):
        openai.api_key = self.api_key

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

def open_ai_response(cv, job_description, word_count):
    prompt = f'Using the following (CV and Job Description) information, write a cover letter in a conversational tone (with a limit of {word_count} words): \n\nJob Description: {job_description}\n\nCV: {cv}'
    model_engine = "text-davinci-002"

    response = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=10000
    )
    answer = response.choices[0].text.strip()

    return answer


api_key = st.secrets["api_key"]['open_ai']
if api_key is None:
    st.error('API key not found. Please set the open_ai .streamlit/secrets.toml')
else:
    with OpenAI_API(api_key):
        columns = st.columns((1, 1), gap='medium')

        cv = columns[0].text_area("Enter your CV: ")
        job_description = columns[1].text_area("Enter the job description: ")
        word_count = columns[0].radio("Select the number of words:", (200, 250))


        submit = st.button("Submit")

        if submit:
            text_input = open_ai_response(cv=cv, job_description=job_description, word_count=word_count)

            st.write(text_input)
