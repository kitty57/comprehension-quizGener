import streamlit as st
import google.generativeai as genai
import ast

genai.configure(api_key="AIzaSyDKcxALky8LiROaxb0RGMw8TLLOcujMRMY")
model = genai.GenerativeModel(model_name="gemini-pro")


def prompt0():
    prompt_parts = [f'''generate a passage/story of 500 words to test a child's comprehensive and understanding ability.Return the generated passage''', ]
    return prompt_parts


def prompt1(passage):
    prompt_parts = [f'''
    Given the following passage/story {passage}, generate comprehension mutiple choice questions to test a child's understanding. Provide feedback and explanations for each question.

    Passage/Story:
    [Insert the passage or story here.]

    Instructions:
    1. Generate multiple-choice only based on the content of the passage/story.
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
       D) Optilon 4

    The output should be a list of dictionaries where each dictionary represents a question with the following format:
        {{'question': question_text, 'options': options_list, 'answer': correct_answer_index, 'feedback': feedback_text}}

    where options correspond to a comma-separated list of 4 options (a, b, c, d) to choose from (for example: what as the name? a)lucas , b)maua ,c) peter, d)Ian)
    and answer is the right option index (0, 1, 2, or 3) and feedback is the feedback.
    '''
                 ]
    return prompt_parts


def to_markdown(text):
    text = text.replace('•', ' *')
    return st.markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


def generate(prompt0, prompt1, model):
    human_prompt1 = prompt0()
    response1 = model.generate_content(human_prompt1)
    passage = response1.text
    st.markdown(passage)
    human_prompt2 = prompt1(passage)
    response2 = model.generate_content(human_prompt2)
    comprehension_questions = response2.text
    return comprehension_questions


st.title("Comprehension Question-Answering")
comprehension_questions = generate(prompt0, prompt1, model)
i=comprehension_questions.find('{')
extracted_string =comprehension_questions[i:-5]
st.write("Extracted string:", extracted_string)
comprehension_question=eval(extracted_string)
for question in comprehension_question:
  st.subheader(question['question'])
  options = question['options'].split(',')
  user_answer = st.text_input(f"Enter answer: ", key=question['question'])
  correct_answer_index = int(question['answer'])
  correct_answer = options[correct_answer_index]
  feedback = question['feedback']
  if user_answer.lower().strip() == correct_answer.lower().strip() and user_answer.strip() != '':
    st.write("Correct!")
  elif user_answer.strip() != '':
    st.write("Incorrect. Feedback:", feedback)
