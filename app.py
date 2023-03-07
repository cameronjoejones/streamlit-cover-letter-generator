import streamlit as st
import openai
from example_data import example_cv, example_job_description

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

def open_ai_response(cv, job_description):
    prompt = f'Using the following (CV and Job Description) information, write a cover letter in a conversational tone (with a limit of 250 words): \n\nJob Description: {job_description}\n\nCV: {cv}'
    model_engine = "text-davinci-002"

    response = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1000
    )
    answer = response.choices[0].text.strip()

    return answer


api_key = st.secrets["api_key"]['open_ai']
if api_key is None:
    st.error('API key not found. Please set the api_key in the .streamlit/secrets.toml file.')
else:
    with OpenAI_API(api_key):

#         st.info("Please enter your CV and the job description in the text areas below. Then click the submit button to generate your cover letter. (Reponse has a limit of 250 words)", icon='ℹ️')
        
        checkbox = st.checkbox("Example CV and Job Description")

        if checkbox == False:

            columns = st.columns((1, 1))
            cv = columns[0].text_area("Enter your CV: ")
            job_description = columns[1].text_area("Enter the job description: ")

        else:
            columns = st.columns((1, 1))
            cv = columns[0].text_area("Enter your CV: ", example_cv)
            job_description = columns[1].text_area("Enter the job description: ", example_job_description)

        submit = st.button("Submit")

        if submit:
            text_input = open_ai_response(cv=cv, job_description=job_description)

            st.write(text_input)
            
            
st.sidebar.title("About")
st.sidebar.info("This app was created by Cameron Jones. You can find the source code on [GitHub] https://github.com/cameronjoejones/streamlit-cover-letter-generator.")
