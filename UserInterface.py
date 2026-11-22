import json
import re


import base64
from pathlib import Path


import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI


# Load OpenAI key from .env
load_dotenv()


client = OpenAI()
MODEL = "gpt-6-luna"




# sample notes for the classroom demonstration
STUDY_NOTES = """
Cellular respiration is the process by which
cells convert energy from glucose into ATP.


Glycolysis occurs in the cytoplasm and produces
two molecules of pyruvate.


The citric acid cycle takes place in the
mitochondrial matrix and produces NADH and FADH2.


The electron transport chain is located in
the inner mitochondrial membrane.


Oxygen is the final electron acceptor.
ATP synthase uses the proton gradient to
produce ATP.
"""




# lion's styling
CSS = """
.gradio-container {
   width: 100% !important;
   max-width: 960px !important;
   margin: 0 auto !important;
   padding: 24px 24px 12px !important;
}


.tuddy-brand {
   margin-bottom: 8px;
   text-align: left;
}


.tuddy-brand h1 {
   margin: 0 !important;
   font-size: 30px !important;
}


.tuddy-logo {
   display: block;
   width: 180px;
   height: 180px;
   object-fit: contain;
   background: transparent;
   border-radius: 0;
   margin: 0;
}


.tuddy-brand p {
   margin: 10px 0 0;
}


#tuddy-chat {
   border-radius: 18px;
   overflow: hidden;
}


#tuddy-question {
   border-radius: 16px;
}


#tuddy-question textarea {
   font-size: 16px !important;
}


.tuddy-welcome {
   text-align: center;
   padding: 20px 12px;
}


.tuddy-welcome strong {
   display: block;
   font-size: 23px;
   margin-bottom: 8px;
}


footer {
   display: none !important;
}
"""




# Temporary AI callback for the interface


def read_message_content(content):
   """Handle both plain and structured Gradio messages."""
   if isinstance(content, str):
       return content


   if isinstance(content, list):
       return " ".join(
           block.get("text", "")
           for block in content
           if isinstance(block, dict)
           and block.get("type") == "text"
       )


   return ""




def parse_answers(message):
   """Recognize answers such as 1A, 2C, 3B, 4A, 5D."""
   matches = re.findall(
       r"([1-5])\s*[\.\):\-]?\s*([A-D])\b",
       message.upper()
   )


   answers = {}


   for number, letter in matches:
       answers[int(number)] = letter


   return answers




def create_quiz(topic):
   """Ask the AI to return a structured quiz."""

 # quiz instructions/guidelines

   prompt = f"""
   Create exactly five multiple-choice questions
   about this topic: {topic}
 
    

   Use ONLY these study notes:


   {STUDY_NOTES}


   Return ONLY a valid JSON object with this structure:


   {{
     "questions": [
       {{
         "question": "Question text",
         "options": {{
           "A": "First option",
           "B": "Second option",
           "C": "Third option",
           "D": "Fourth option"
         }},
         "correct": "A",
         "explanation": "Why this answer is correct"
       }}
     ]
   }}


   Requirements:
   - Exactly five questions.
   - Four answer options per question.
   - Exactly one correct answer per question.
   - Correct must be A, B, C, or D.
   - Include an explanation for each answer.
   - Return JSON only, no Markdown code fences.
   - Do not invent information outside the notes.
   """


   response = client.responses.create(
       model=MODEL,
       instructions=(
           "You are Tuddy, an educational AI tutor. "
           "Generate accurate, structured study quizzes. "
           "Follow the requested JSON format."
       ),
       input=prompt
   )


   raw_text = response.output_text.strip()


   # Remove code fences if the AI includes them
   if raw_text.startswith("```"):
       raw_text = re.sub(
           r"^```(?:json)?\s*",
           "",
           raw_text
       )
       raw_text = re.sub(
           r"\s*```$",
           "",
           raw_text
       )


   quiz = json.loads(raw_text)


   questions = quiz["questions"]


   if len(questions) != 5:
       raise ValueError(
           "The AI did not generate five questions."
       )


   for question in questions:
       if not isinstance(question["question"], str):
           raise ValueError("Invalid question text.")


       if set(question["options"]) != {
           "A", "B", "C", "D"
       }:
           raise ValueError("Invalid answer options.")


       if question["correct"] not in (
           "A", "B", "C", "D"
       ):
           raise ValueError("Invalid answer key.")


       if not question["explanation"]:
           raise ValueError("Missing explanation.")


   return quiz




def display_quiz(quiz):
   """Show questions without revealing correct answers."""


   output = "## Your Tuddy Practice Quiz\n\n"


   for number, question in enumerate(
       quiz["questions"], start=1
   ):
       output += (
           f"**{number}. {question['question']}**\n\n"
       )


       for letter, option in question["options"].items():
           output += f"{letter}. {option}\n\n"


   output += (
       "---\n"
       "**Your turn!** Submit your answers like this:\n\n"
       "`1A, 2C, 3B, 4A, 5D`\n\n"
       "I'll grade your answers when you're finished!"
   )


   return output




def grade_quiz(quiz, answers):
   """Compare student answers with the saved answer key."""


   questions = quiz["questions"]
   score = 0
   feedback = "## Your Quiz Results\n\n"


   for number, question in enumerate(
       questions, start=1
   ):
       student_answer = answers[number]
       correct_answer = question["correct"]


       if student_answer == correct_answer:
           score += 1
           feedback += (
               f"**Question {number}: Correct!** ✅\n\n"
           )
       else:
           feedback += (
               f"**Question {number}: Not quite!**\n\n"
               f"Your answer: {student_answer}\n\n"
               f"Correct answer: {correct_answer}\n\n"
               f"**Explanation:** "
               f"{question['explanation']}\n\n"
           )


   feedback = (
       f"## You scored {score}/5 "
       f"({score * 20}%)!\n\n" + feedback.split(
           "## Your Quiz Results\n\n", 1
       )[1]
   )


   if score == 5:
       feedback += (
           "\nExcellent work! You got every question right!"
       )
   else:
       feedback += (
           "\nKeep practicing! Every mistake is "
           "an opportunity to understand the topic better."
       )


   feedback += (
       "\n\nYou can ask for another quiz whenever "
       "you're ready."
   )


   return feedback




def tuddy_response(message, history, quiz_state):


   quiz_state = quiz_state or {}
   message = message.strip()


   if not message:
       return "Please enter a question.", quiz_state


   try:


       # STEP 1: Check if the student submitted quiz answers
       answers = parse_answers(message)


       if quiz_state.get("questions") and answers:


           if len(answers) != 5:
               return (
                   "Please submit all five answers, "
                   "for example: 1A, 2C, 3B, 4A, 5D.",
                   quiz_state
               )


           result = grade_quiz(quiz_state, answers)


           # Quiz completed; clear active quiz state
           return result, {}


       # STEP 2: Check if the student requested a new quiz
       lower_message = message.lower()


       wants_quiz = any(
           phrase in lower_message
           for phrase in [
               "quiz",
               "test me",
               "practice questions"
           ]
       )


       if wants_quiz:


           quiz = create_quiz(message)


           # Save the complete quiz, including answer key
           return display_quiz(quiz), quiz


       # STEP 3: Handle ordinary tutoring conversations
       messages = []


       for item in history[-10:]:
           role = item.get("role")
           content = read_message_content(
               item.get("content")
           )


           if role in ("user", "assistant") and content:
               messages.append({
                   "role": role,
                   "content": content
               })


       messages.append({
           "role": "user",
           "content": message
       })


       response = client.responses.create(
           model=MODEL,
           instructions=(
               "You are Tuddy, a friendly AI tutor. "
               "Explain concepts clearly and encourage "
               "critical thinking through guiding questions. "
               "Use these study notes as context:\n"
               + STUDY_NOTES
           ),
           input=messages
       )


       return (
           response.output_text
           or "Sorry, I could not generate a response.",
           quiz_state
       )


   except Exception as error:
       print("Tuddy error:", repr(error))


       return (
           "Sorry, something went wrong. "
           "Please check the PyCharm console.",
           quiz_state
       )






# Build the visual interface

# Build the visual interface
def create_interface():

    logo_path = Path(__file__).with_name(
        "tuddy-logo-transparent.png"
    )

    description = """
    <div class="tuddy-brand">
        <h1>Tuddy</h1>
        <p>Your AI study buddy.</p>
    </div>
    """

    if logo_path.is_file():

        logo_data = base64.b64encode(
            logo_path.read_bytes()
        ).decode("ascii")

        description = f"""
        <div class="tuddy-brand">
            <img class="tuddy-logo"
                 src="data:image/png;base64,{logo_data}"
                 alt="Tuddy bear logo">
            <p>Your AI study buddy.</p>
        </div>
        """

    with gr.Blocks(
        theme=gr.themes.Soft(
            primary_hue="teal",
            neutral_hue="slate"
        ),
        css=CSS
    ) as demo:

        gr.HTML(description)

        chatbot = gr.Chatbot(
            label="Conversation",
            show_label=False,
            layout="bubble",
            height=500,
            elem_id="tuddy-chat",
            placeholder=(
                '<div class="tuddy-welcome">'
                '<strong>What are we studying?</strong>'
                'Ask a question, work through a problem, '
                'or review a concept.'
                '</div>'
            )
        )

        textbox = gr.Textbox(
            placeholder="Ask a study question...",
            show_label=False,
            lines=1,
            max_lines=6,
            elem_id="tuddy-question"
        )

        quiz_state = gr.State(value={})

        gr.ChatInterface(
            fn=tuddy_response,
            chatbot=chatbot,
            textbox=textbox,
            additional_inputs=[quiz_state],
            additional_outputs=[quiz_state],
            run_examples_on_click=False,
            submit_btn="Send",
            stop_btn="Stop",
            fill_height=True,
            api_name="chat"
        )

    return demo





if __name__ == "__main__":
   create_interface().launch(
       server_name="127.0.0.1",
       server_port=7860,
       inbrowser=True,
       show_error=True
   )

