import streamlit as st
import openai

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai"]["api_key"]

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Main Dashboard", "Knowledge Base", "Consulting & Questioning Tools", "SPM Consultant Tool for NSA Requests"])

# Welcome Guide (Shown only once)
if "welcome_shown" not in st.session_state:
    st.session_state["welcome_shown"] = True
    st.title("Welcome to the SPM Megazord Platform!")
    st.write("""
        The SPM Megazord is a high-performance platform designed to provide insights, guidance, and tools for 
        a variety of roles including Athletes, Coaches, and Managers. Here's a quick overview of what you can do:
        - **Q&A Module**: Ask any question related to performance, strategy, or general information.
        - **Summarization Module**: Summarize lengthy content, such as reports or articles.
        - **Content Generation Module**: Get ideas, suggestions, or plans based on a topic you specify.
    """)
    st.button("Got it! Let’s get started.")

# Main Dashboard Page
if page == "Main Dashboard":
    st.title("SPM Megazord Dashboard")
    st.subheader("Welcome to the SPM Megazord platform!")

    # User Greeting and Role Selection
    user_name = st.text_input("Enter your name:")
    if user_name:
        st.write(f"Hello, {user_name}! Welcome to the Megazord.")
        role_options = ["NSA", "SPM", "Management", "Athlete", "Coach", "HPM", "HP Staff", "Other"]
        user_role = st.selectbox("Select your role:", role_options)
        if user_role == "Other":
            user_role_other = st.text_input("Please specify your role:")
            st.write(f"Role: {user_role_other}")
        else:
            st.write(f"Role: {user_role}")

        # Role-Specific Modules Introduction
        st.subheader(f"Modules Available for {user_role}")
        if user_role == "Athlete":
            st.write("As an Athlete, you can use the following modules:")
            st.write("- **Q&A Module**: Ask questions about training or performance.")
            st.write("- **Summarization Module**: Summarize long training reports or articles.")
            st.write("- **Content Generation Module**: Generate training tips and recovery advice.")
        elif user_role == "Coach":
            st.write("As a Coach, the following modules are available to you:")
            st.write("- **Q&A Module**: Ask questions about strategy, motivation, and team management.")
            st.write("- **Summarization Module**: Summarize game analysis or performance reports.")
            st.write("- **Content Generation Module**: Generate team-building ideas or motivational tips.")
        elif user_role == "Management":
            st.write("As a Management professional, you have access to:")
            st.write("- **Q&A Module**: Ask questions related to performance metrics and team productivity.")
            st.write("- **Summarization Module**: Summarize strategic reports or data analysis.")
            st.write("- **Content Generation Module**: Generate insights and performance improvement ideas.")

# Knowledge Base Page
elif page == "Knowledge Base":
    st.title("Centralized Knowledge Base")
    st.write("""
    The Knowledge Base provides easy access to frequently asked questions, best practices, policies, rules, 
    terms and conditions, and other documentation relevant to your role and region.
    """)
    kb_content = {
        "FAQs": ["What is the SPM Megazord?", "How does the Q&A Module work?", "Can I customize content generation?"],
        "Policies": ["Privacy Policy", "Data Protection Policy", "Terms and Conditions"],
        "Best Practices": ["Effective Training Techniques", "Management Strategies", "Motivation Tips for Coaches"]
    }
    kb_section = st.selectbox("Select a Knowledge Base section:", kb_content.keys())
    st.write(f"**{kb_section}:**")
    st.write("\n".join(kb_content[kb_section]))

# Consulting & Questioning Tools Page
elif page == "Consulting & Questioning Tools":
    st.title("AI-Powered Consulting & Questioning Tools")

    # SPM Consultant Tool
    st.write("### SPM Consultant Tool")
    consultant_prompt = st.text_area("Enter your query for AI-powered consulting:")
    if consultant_prompt:
        consultant_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"As an SPM Consultant, {consultant_prompt}"}]
        )
        st.write("SPM Consultant's AI-Powered Answer:", consultant_response.choices[0].message['content'].strip())
        st.write("*Note: Answers are reviewed by human experts for accuracy.*")

    # SPM Question Tool
    st.write("### SPM Question Tool")
    user_query = st.text_area("Enter a structured question for SPM support:")
    if user_query:
        breakdown_prompt = f"Analyze the question '{user_query}' into categories, prompt for clarifying information, and provide recommendations."
        question_tool_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": breakdown_prompt}]
        )
        st.write("SPM Question Tool's Structured Response:", question_tool_response.choices[0].message['content'].strip())
        st.write("*Automated recommendations based on historical cases and sports-specific guidelines.*")

# SPM Consultant Tool for NSA Requests Page
elif page == "SPM Consultant Tool for NSA Requests":
    st.title("SPM Consultant Tool for NSA Requests")
    st.write("**Purpose**: This tool helps NSA representatives submit structured requests to SPMs, ensuring all necessary details are captured.")

    # Step 1: Initial Information Collection
    st.subheader("Step 1: Basic Information")
    sport = st.text_input("Sport/NSA you represent:")
    spm_contact = st.text_input("SPM you wish to contact:")
    escalation_level = st.selectbox("Level of escalation:", ["SPM", "Team Lead", "HOD", "Chief"])

    # Initialize variables that may not be set depending on user actions
    suggested_answer = ""
    satisfied = "N/A"
    judgement = ""

    if sport and spm_contact and escalation_level:
        # Step 2: Define Request
        st.subheader("Step 2: Define Your Request")
        request_title = st.text_input("Title of your query/request:")
        request_type = st.selectbox("Type of query/request:", ["Information Request", "Service/Resource Request", "Other"])

        # AI Interaction if Information Request
        if request_type == "Information Request":
            info_query = st.text_area("Describe your question in detail:")
            if info_query:
                st.write("Suggested Answer:")
                suggested_answer = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": f"As an SPM Consultant, answer this: {info_query}"}]
                ).choices[0].message['content'].strip()
                st.write(suggested_answer)

                satisfied = st.radio("Is this answer sufficient?", ["Yes", "No"])
                if satisfied == "Yes":
                    st.write("Thank you! This answer will be recorded in the summary document.")
                else:
                    st.write("Let's gather further details.")

        # Further Information for Requests or Unanswered Queries
        if request_type != "Information Request" or satisfied == "No":
            st.subheader("Step 4: Provide Additional Details")
            purpose = st.text_area("Purpose and justification for the request:")
            expected_outcomes = st.text_area("Expected outcomes or goals:")
            resources_needed = st.text_area("Resources or support needed:")
            timeframe = st.text_input("Deadline or timeframe for the request:")

        # Preliminary Judgement by AI
        st.subheader("Step 5: Preliminary Judgement")
        if st.button("Generate Judgement"):
            judgement_prompt = f"""
            Based on the following details, provide a preliminary judgement on approval likelihood:
            - Sport: {sport}
            - SPM Contact: {spm_contact}
            - Escalation Level: {escalation_level}
            - Request Type: {request_type}
            - Purpose: {purpose}
            - Expected Outcomes: {expected_outcomes}
            - Resources Needed: {resources_needed}
            - Timeframe: {timeframe}
            """
            judgement = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": judgement_prompt}]
            ).choices[0].message['content'].strip()
            st.write("Preliminary Judgement:", judgement)

        # Generate Summary Document
        st.subheader("Step 6: Summary Document")
        if st.button("Generate Summary Document"):
            # Fallback for missing values if the buttons weren't clicked
            purpose = purpose if 'purpose' in locals() else ""
            expected_outcomes = expected_outcomes if 'expected_outcomes' in locals() else ""
            resources_needed = resources_needed if 'resources_needed' in locals() else ""
            timeframe = timeframe if 'timeframe' in locals() else ""

            summary_content = f"""
            **SPM Consultant Tool Summary Document**

            - **Sport/NSA**: {sport}
            - **SPM Contact**: {spm_contact}
            - **Escalation Level**: {escalation_level}

            ### Query/Request Details
            - **Title**: {request_title}
            - **Type**: {request_type}
            - **Purpose**: {purpose}
            - **Expected Outcomes**: {expected_outcomes}
            - **Resources Needed**: {resources_needed}
            - **Timeframe**: {timeframe}

            ### Suggested Answer
            - **Answer**: {suggested_answer if request_type == 'Information Request' else 'N/A'}
            - **Satisfaction**: {satisfied if request_type == 'Information Request' else 'N/A'}

            ### Preliminary Judgement
            {judgement}

            *This document is shared with the NSA representative and the SPM for record and further action.*
            """
            st.write(summary_content)
            st.success("Summary document generated and shared with NSA and SPM.")