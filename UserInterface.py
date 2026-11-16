import base64
from pathlib import Path

import gradio as gr


CSS = """
.gradio-container { width: 100% !important; max-width: 960px !important; margin: 0 auto !important;
    padding: 24px 24px 12px !important; }
.tuddy-brand { margin-bottom: 8px; }
.tuddy-brand h1 { margin: 0 !important; font-size: 30px !important; }
.tuddy-brand .tuddy-logo-heading { line-height: 0; }
.tuddy-logo { display: block; width: 180px; height: 180px;
    object-fit: contain; background: #fffaf4; border-radius: 18px; }
.tuddy-brand p { margin: 10px 0 0; }
#tuddy-chat { border-radius: 18px; overflow: hidden; }
#tuddy-question { border-radius: 16px; }
#tuddy-question textarea { font-size: 16px !important; }
.tuddy-welcome { text-align: center; padding: 20px 12px; }
.tuddy-welcome strong { display: block; font-size: 23px; margin-bottom: 8px; }
footer { display: none !important; }
@media (max-width: 600px) {
    .gradio-container { padding: 12px !important; }
    .tuddy-logo { width: 140px; height: 140px; }
}
"""


def restore_input():
    return gr.update(interactive=True, submit_btn="Send", stop_btn=False)


def create_interface():
    logo_path = Path(__file__).with_name("tuddy-logo.png")
    description = '<div class="tuddy-brand"><h1>Tuddy</h1><p>Your AI study buddy.</p></div>'
    if logo_path.is_file():
        logo_data = base64.b64encode(logo_path.read_bytes()).decode("ascii")
        description = (
            '<div class="tuddy-brand">'
            '<h1 class="tuddy-logo-heading">'
            f'<img class="tuddy-logo" src="data:image/png;base64,{logo_data}" alt="Tuddy bear logo">'
            '</h1>'
            '<p>Your AI study buddy.</p></div>'
        )

    interface = gr.load_chat(
        base_url="http://localhost:1234/v1",
        model="llama-3.2-3b-instruct",
        token="***",
        streaming=True,
        file_types=None,
        title=None,
        description=description,
        chatbot=gr.Chatbot(
            label="Conversation",
            show_label=False,
            layout="bubble",
            buttons=["copy", "copy_all"],
            height="min(58dvh, 620px)",
            min_height=240,
            elem_id="tuddy-chat",
            placeholder=(
                '<div class="tuddy-welcome"><strong>What are we studying?</strong>'
                'Ask a question, work through a problem, or review a concept.</div>'
            )
        ),
        textbox=gr.Textbox(
            placeholder="Ask a study question…",
            show_label=False,
            lines=1,
            max_lines=6,
            submit_btn="Send",
            stop_btn="Stop",
            autofocus=False,
            elem_id="tuddy-question"
        ),
        examples=["Explain a concept", "Help me practice", "Walk through a problem"],
        examples_label="Try a starting point",
        run_examples_on_click=False,
        autofocus=False,
        show_progress="hidden",
        fill_height=True,
        api_name="chat"
    )

    interface.title = "Tuddy"

    with interface:
        interface.textbox.stop(
            restore_input,
            inputs=None,
            outputs=interface.textbox,
            queue=False,
            api_visibility="private"
        )

    return interface


if __name__ == "__main__":
    create_interface().launch(
        server_name="0.0.0.0",
        server_port=7860,
        inbrowser=True,
        show_error=True,
        theme=gr.themes.Soft(primary_hue="teal", neutral_hue="slate"),
        css=CSS,
        footer_links=[]
    )
