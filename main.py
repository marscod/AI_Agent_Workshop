import streamlit as st

# Add an icon to the app
st.set_page_config(
    page_title="AI Agent Workshop",
    page_icon="src/acm_logo_tablet.png",
)

# Add custom CSS to handle overflow
st.markdown("""
<style>
.stMarkdown {
    word-wrap: break-word;
    overflow-wrap: break-word;
    max-width: 100%;
}
pre {
    white-space: pre-wrap !important;
    word-break: break-word !important;
    overflow-x: auto !important;
}
code {
    white-space: pre-wrap !important;
    word-break: break-word !important;
}
</style>
""", unsafe_allow_html=True)

# import the SearchAgent class from the Agents module
from Agents.websearchagent import SearchAgent

# a simple streamlit app to interact with the SearchAgent
# using the SearchAgent to get search results for a query
# and displaying the results in a streamlit app
# the SearchAgent uses the LiteLLMModel to generate completions
# for the search
# the SearchAgent also has a delay before making a request
# to simulate the time taken to think
st.markdown("# Welcome to Agent Workshop!\n\n")
st.markdown("## Search Agent\n")

if 'input' not in st.session_state:
    st.session_state.input = ""

with st.form(key='search_form'):
    # Split the screen into 3 columns
    col1, col2, col3 = st.columns([10, 1,2])
    with col1:
        # st.write("") 
        input_query = st.text_input(">", value=st.session_state.input, key='input_query', label_visibility="collapsed")  
    
    with col2:
        # st.write("")  # Spacer for alignment
        search_button = st.form_submit_button("🔍", use_container_width=True)
    
    with col3:
        # Select a host for the SearchAgent
        host = st.selectbox("Select a host", ["xAI", "Groq", "Grok", "HF"], index=0, label_visibility="collapsed")
        host = host.lower()
        if host=="HF":
            os.environ["HF_API"]=None

if search_button:
    # create a SearchAgent instance with a delay of 0 seconds
    # the SearchAgent uses the "xai" host by default, you may update it to "groq" or "grok"
    # by setting the host parameter
    agent=SearchAgent(host=host, delay=0)

    # show a progress bar
    updated_agent = None
    with st.spinner("Calling Agent...", show_time=True):
        try:
            # call the SearchAgent with the input query
            updated_agent = agent.call(query= st.session_state.input_query)
        except Exception as e:
            # display an error message if there is an exception
            st.toast(f"API Provider is not available. Check API key.:{e}")
            updated_agent = None

    # display the search results
    for i, step in enumerate(updated_agent.memory.steps):
        try:
            # display the step number and the model output details
            st.markdown(f"Step ({i}): (thinking for {step.timing.duration:.2f} seconds)\n")

            with st.expander(f"Facts for Step ({i})", expanded=False):
                # display the facts for the step such as the query, model name, and model output
                st.json(step.dict())
            
            # display the model output
            st.markdown(step.model_output)

        except Exception as e:
            # display an error message if there is an exception
            # uncomment the following line to see the error message
            st.markdown(f"Error: {e}")

            pass
    
    

