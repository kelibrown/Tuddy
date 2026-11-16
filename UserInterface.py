# ui css and html, user interface logic
import base64
from pathlib import Path
from AiTutorEngine import Document


import gradio as gr


CSS = """
.gradio-container {
    width: 100% !important;
    max-width: 960px !important;
    margin: 0 auto !important;
    padding: 24px 24px 12px !important;
}

.tuddy-brand {
    margin-bottom: 8px;
}

.tuddy-brand h1 {
    margin: 0 !important;
    font-size: 30px !important;
}

.tuddy-brand .tuddy-logo-heading {
    line-height: 0;
}

.tuddy-logo {
    display: block;
    width: 180px;
    height: 180px;
    object-fit: contain;
    border-radius: 18px;
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

@media (max-width: 600px) {
    .gradio-container {
        padding: 12px !important;
    }

    .tuddy-logo {
        width: 140px;
        height: 140px;
    }
}
"""


class UserInterface:
# constructor needs to recieve the study doc to later be displayed.
    def __init__(self, ai_tutor, chat_session):

        self.ai_tutor = ai_tutor
        self.chat_session = chat_session

    def send_message(self, student_input):

        if not student_input.strip():
            return self.chat_session.get_formatted_history(), ""

        # Store the student's message
        self.chat_session.append_message(
            "user",
            student_input
        )

        # Ask the AI tutor for a response
        response = self.ai_tutor.generate_socratic_response(
            self.chat_session
        )

        # Store Tuddy's response
        self.chat_session.append_message(
            "assistant",
            response
        )

        # Return the complete conversation to Gradio
        return self.chat_session.get_formatted_history(), ""


    # class / presentation demo
    def generate_demo_quiz(self, topic):
            quiz = self.ai_tutor.generateQuiz(topic)
            return quiz.content

    def clear_chat(self):

        self.chat_session.clear_history()

        return [], ""

    def launch(self):

        # Load the logo if it exists
        logo_path = Path(__file__).with_name("tuddy-logo-transparent.png")

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
                <h1 class="tuddy-logo-heading">
                    <img class="tuddy-logo"
                    src="data:image/png;base64,{logo_data}"
                    alt="Tuddy bear logo">
                </h1>
                <p>Your AI study buddy.</p>
            </div>
            """

        with gr.Blocks(
                title="Tuddy"
        ) as interface:

            gr.HTML(description)

            # CHAT TAB
            with gr.Tab("Ask Tuddy"):

                chatbot = gr.Chatbot(
                    label="Conversation",
                    show_label=False,
                    layout="bubble",
                    buttons=["copy", "copy_all"],
                    height="min(58dvh, 620px)",
                    min_height=240,
                    elem_id="tuddy-chat",
                    placeholder=(
                        '<div class="tuddy-welcome">'
                        '<strong>What are we studying?</strong>'
                        'Ask a question, work through a problem, '
                        'or review a concept.'
                        '</div>'
                    )
                )

                question = gr.Textbox(
                    placeholder="Ask a study question…",
                    show_label=False,
                    lines=1,
                    max_lines=6,
                    autofocus=False,
                    elem_id="tuddy-question"
                )

                with gr.Row():

                    send_button = gr.Button(
                        "Send",
                        variant="primary"
                    )

                    clear_button = gr.Button("Clear chat")

                gr.Examples(
                    examples=[
                        "Explain a concept",
                        "Help me practice",
                        "Walk through a problem"
                    ],
                    inputs=question,
                    label="Try a starting point"
                )

                # Send using the button
                send_button.click(
                    fn=self.send_message,
                    inputs=question,
                    outputs=[chatbot, question]
                )

                # Send by pressing Enter
                question.submit(
                    fn=self.send_message,
                    inputs=question,
                    outputs=[chatbot, question]
                )

                # Clear conversation
                clear_button.click(
                    fn=self.clear_chat,
                    inputs=None,
                    outputs=[chatbot, question]
                )

            # QUIZ TAB


            # CLASS DEMO
            with gr.Tab("Generate a Quiz"):
                gr.Markdown("## Create a Quiz")
                gr.Markdown(
                    "Generate a practice quiz using your uploaded study material."
                )

                topic = gr.Textbox(
                    label="Quiz Topic",
                    value="Cellular Respiration",
                    placeholder="Enter a topic..."
                )

                generate_button = gr.Button(
                    "Generate Quiz",
                    variant="primary"
                )

                quiz_output = gr.Textbox(
                    label="Your Generated Quiz",
                    lines=20,
                    interactive=False
                )

                generate_button.click(
                    fn=self.generate_demo_quiz,
                    inputs=topic,
                    outputs=quiz_output
                )

        interface.launch(
            server_name="0.0.0.0",
            server_port=7860,
            inbrowser=True,
            show_error=True,
            theme=gr.themes.Soft(
                primary_hue="teal",
                neutral_hue="slate"
            ),
            css=CSS,
            footer_links=[]
        )