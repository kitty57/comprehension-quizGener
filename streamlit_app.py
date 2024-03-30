import streamlit as st
import google.generativeai as genai
import ast
import re

# Configure GenerativeAI
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel(model_name="gemini-pro")

# Function to prompt for passage generation
def prompt0():
    return [f'''Generate a passage/story of 500 words to test a child's comprehension and understanding ability. Return the generated passage.''']

# Function to prompt for comprehension questions generation
def prompt1(passage):
    return [f'''
    Given the following passage/story:

    {passage}

    Generate comprehension multiple-choice questions to test a child's understanding. Provide feedback and explanations for each question.

    Instructions:
    1. Generate multiple-choice questions only based on the content of the passage/story.
    2. Ensure that the questions cover various aspects such as main ideas, details, inference, vocabulary, and author's purpose.
    3. Provide feedback and explanations for each question to help the child learn from their mistakes.
    4. Aim for a mix of easy, moderate, and challenging questions to cater to different levels of comprehension.

    Example questions:
    1. What is the main idea of the passage/story?
       A) Option 1
       B) Option 2
       C) Option 3
       D) Option 4

    2. What does the word "_____" mean in the context of the passage/story?
       A) Option 1
       B) Option 2
       C) Option 3
       D) Option 4

    3. Based on the passage/story, what can you infer about ____?
       A) Option 1
       B) Option 2
       C) Option 3
       D) Option 4

    The output should be a list of dictionaries where each dictionary represents a question with the following format:
    {{'question': question_text, 'options': options_list, 'answer': correct_answer_index, 'feedback': feedback_text}}

    where options correspond to a comma-separated list of 4 options (a, b, c, d) to choose from and answer is the index of the correct option (0, 1, 2, or 3) and feedback is the feedback.
    ''']

# Function to generate content
def generate(prompt0, prompt1, model):
    passage_prompt = prompt0()
    response1 = model.generate_content(passage_prompt)
    passage = response1.text
    st.markdown(passage)
    
    comprehension_prompt = prompt1(passage)
    response2 = model.generate_content(comprehension_prompt)
    comprehension_questions = response2.text

    try:
        pattern = r"{.*}"  
        match = re.search(pattern, comprehension_questions)
        if match:
            extracted_string = match.group(0)
        else:
            st.error("No comprehension question dictionary found in the output.")
            return None
        if extracted_string:
            try:
                comprehension_question_list = ast.literal_eval(extracted_string)
                return comprehension_question_list
            except (IndentationError, SyntaxError):
                st.error("Error parsing comprehension question string. Please check the model output.")
                return None

    except (ValueError, SyntaxError):
        st.error("Error parsing comprehension questions string. Please check the model output.")
        return None

# Streamlit app
st.title("Comprehension Question-Answering")
comprehension_questions = generate(prompt0, prompt1, model)

if comprehension_questions:
    for question in comprehension_questions:
        st.subheader(question['question'])
        options = question['options'].split(',')
        user_answer = st.radio("Select your answer:", options=options, key=question['question'])
        correct_answer_index = int(question['answer'])
        correct_answer = options[correct_answer_index]
        feedback = question['feedback']

        if user_answer.strip() != '':
            if user_answer.lower().strip() == correct_answer.lower().strip():
                st.write("Correct!")
            else:
                st.error("Incorrect. The correct answer is:", correct_answer)
                st.write("Feedback:", feedback)
else:
    st.error("No comprehension questions generated. Please check the model output.")
