import streamlit as st
import google.generativeai as genai


genai.configure(api_key="AIzaSyDKcxALky8LiROaxb0RGMw8TLLOcujMRMY")
model = genai.GenerativeModel(model_name="gemini-pro")
def prompt0():
  prompt_parts=[f'''generate a passage/story of 500 words to test a child's comprehensive and understanding ability.Return the generated passage''',]
  return prompt_parts

def prompt1(passage):
  prompt_parts=[f'''
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
   the ouput should a dictionary where each key is the question and its value must be python dictionary of the form {{options,answer,feedback}}
    where options correspond to a comma-seperated list of 4 options(a,b,c,d) to choose from(for example: what as the name? a)lucas  b)maua c) peter d)Ian
  and answer in the right option (either 0 or 1 or 2 or 3 representing the index of the right answer in the list) and feedback is the feedback.
   i want the output to be a python code of the datatype dict.
  ''' ,]
  return prompt_parts
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def generate(prompt0, prompt1, model):
    human_prompt1 = prompt0()
    response1 = model.generate_content(human_prompt1)
    passage = response1.text
    st.markdown(passage)

    human_prompt2 = prompt1(passage)
    response2 = model.generate_content(human_prompt2)
    comprehension_questions = response2.text
    return comprehension_questions

def main():
    st.title("Comprehension Question-Answering")
    a = generate(prompt0, prompt1, model)
    st.subheader("Answer the questions:")
    i=a.find('{')
    extracted_string = a[i-1:-4]
    st.write(extracted_string)
    d=eval(extracted_string)
    c=1
    for i in d:
      st.write("question: ",i)
      st.write("options: ",d[i]['options'])
      options1=d[i]['options']
      options=','.split(options1)
      st.write(options1,options)
      user_answer=st.text_input(f"enter answer {c}: ")
      correct_answer_index = d[i]['answer']
      correct_answer_index=int(correct_answer_index)
      correct_answer = options[correct_answer_index]
      feedback = d[i]['feedback']
      c+=1
      if user_answer.strip().lower() == correct_answer.strip().lower():
        st.write("Correct!")
      else:
        st.write("Incorrect. Feedback:", feedback)

if __name__ == "__main__":
    main()
