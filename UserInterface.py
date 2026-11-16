import gradio as gr


class UserInterface:

    def __init__(self, ai_tutor, chat_session):

        self.ai_tutor = ai_tutor
        self.chat_session = chat_session

    def send_message(self, student_input):

        self.chat_session.append_message(
            "user",
            student_input
        )

        response = self.ai_tutor.generate_socratic_response(
            self.chat_session
        )

        self.chat_session.append_message(
            "assistant",
            response
        )

        return response

    def request_quiz(self, topic, question_count):

        quiz = self.ai_tutor.generate_quiz(
            topic,
            question_count
        )

        return quiz

    def launch(self):

        with gr.Blocks(title="Tuddy") as interface:

            gr.Markdown("# Tuddy - Your Academic AI Assistant")

            with gr.Tab("Ask Tuddy"):

                student_input = gr.Textbox(
                    label="Ask a question"
                )

                chat_output = gr.Textbox(
                    label="Tuddy's Response"
                )

                send_button = gr.Button("Send")

                send_button.click(
                    fn=self.send_message,
                    inputs=student_input,
                    outputs=chat_output
                )

            with gr.Tab("Generate a Quiz"):

                topic = gr.Textbox(
                    label="Quiz Topic"
                )

                question_count = gr.Number(
                    label = "Number of Questions",
                    value = 5,
                    precision = 0
                )

                quiz_output = gr.Textbox(
                    label = "Generated Quiz",
                    lines = 15
                )

                generate_button = gr.Button("Generate Quiz")

                generate_button.click(
                    fn = self.request_quiz,
                    inputs = [topic, question_count],
                    outputs = quiz_output
                )

        interface.launch()