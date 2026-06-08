import gradio as gr
from huggingface_hub import InferenceClient
import json
import re
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load .env from parent dir or current dir
load_dotenv(Path(__file__).resolve().parent.parent / ".env")
load_dotenv()

token = os.environ.get("HF_TOKEN") or os.environ.get("HF_API_KEY")

# Modal endpoint for NVIDIA Nemotron-Mini-4B-Instruct
MODAL_ENDPOINT = os.environ.get("MODAL_ENDPOINT", "")
# Fallback to HF Inference API if Modal is unavailable
text_client = InferenceClient(provider="together", token=token)
image_client = InferenceClient(provider="hf-inference", token=token)

STORY_MODEL = "nvidia/Nemotron-Mini-4B-Instruct"  # via Modal
FALLBACK_MODEL = "Qwen/Qwen2.5-7B-Instruct"  # via HF Inference
IMAGE_MODEL = "black-forest-labs/FLUX.1-schnell"


def call_llm(messages, temperature=0.8, max_tokens=1024):
    """Call Nemotron via Modal, fallback to Qwen via HF Inference."""
    if MODAL_ENDPOINT:
        try:
            r = requests.post(
                MODAL_ENDPOINT,
                json={"messages": messages, "temperature": temperature, "max_tokens": max_tokens},
                timeout=60,
            )
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"]
        except Exception:
            pass  # Fall through to HF Inference
    # Fallback
    response = text_client.chat_completion(
        model=FALLBACK_MODEL,
        messages=messages,
        max_tokens=max_tokens,
        temperature=temperature,
    )
    return response.choices[0].message.content

CSS = """
.storybook-header {
    text-align: center;
    background: linear-gradient(135deg, #1a0533 0%, #2d1b69 50%, #0f1b4d 100%);
    padding: 2rem;
    border-radius: 16px;
    margin-bottom: 1rem;
}
.storybook-header h1 {
    color: #f5e6ff;
    font-size: 2.5rem !important;
    margin-bottom: 0.3rem !important;
}
.storybook-header p {
    color: #c4b5fd;
    font-size: 1.1rem;
}
.scene-card {
    background: #fffbf0;
    border: 2px solid #e8d5b7;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
.scene-card img {
    border-radius: 8px;
}
.story-title {
    text-align: center;
    color: #4c1d95;
    font-family: 'Georgia', serif;
}
.scene-text {
    font-family: 'Georgia', serif;
    font-size: 1.1rem;
    line-height: 1.7;
    color: #3d2b1f;
}
.generate-btn {
    background: linear-gradient(135deg, #7c3aed, #4f46e5) !important;
    font-size: 1.1rem !important;
    padding: 12px 24px !important;
}
footer { display: none !important; }
"""


def generate_story(name, age, theme, extra_details, language="English"):
    """Generate a 4-scene bedtime story with image prompts."""
    age = int(age)
    lang_instruction = f"Write the story text in {language}." if language != "English" else ""
    prompt = f"""Write a short bedtime story for a {age}-year-old child named {name}.
Theme: {theme}
{f"Extra details: {extra_details}" if extra_details else ""}
{lang_instruction}

Requirements:
- Exactly 4 short scenes (3-4 sentences each)
- Gentle, calming tone appropriate for bedtime
- {name} is the main character
- Happy, peaceful ending where {name} falls asleep or feels safe
- Age-appropriate vocabulary for a {age}-year-old
- Story text MUST be in {language}
- Image prompts must remain in English

Return ONLY valid JSON in this exact format, no other text:
{{"title": "Story Title in {language}", "scenes": [{{"text": "Scene text in {language} here", "image_prompt": "A children's book illustration of: brief visual description in English, soft watercolor style, warm colors, whimsical"}}]}}"""

    response = call_llm(
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        temperature=0.8,
    )

    content = response.strip()
    match = re.search(r'\{.*\}', content, re.DOTALL)
    if match:
        content = match.group()
    return json.loads(content)


def generate_illustration(prompt):
    """Generate a single illustration."""
    return image_client.text_to_image(
        prompt=prompt,
        model=IMAGE_MODEL,
        width=768,
        height=512,
    )


def build_output(name, age, theme, extra_details, language, progress=gr.Progress()):
    """Generate full story with illustrations."""
    if not name.strip():
        raise gr.Error("Please enter the child's name!")
    if not theme.strip():
        raise gr.Error("Please choose a theme!")

    progress(0.1, desc="✨ Writing your story...")
    story = generate_story(name, age, theme, extra_details, language)
    title = story["title"]
    scenes = story["scenes"]

    scene_outputs = []
    for i, scene in enumerate(scenes):
        progress((0.2 + i * 0.2), desc=f"🎨 Painting scene {i+1} of {len(scenes)}...")
        img = generate_illustration(scene["image_prompt"])
        scene_outputs.append((img, scene["text"]))

    progress(1.0, desc="📖 Story complete!")

    # Build storybook markdown
    title_md = f"<div class='story-title'><h2>📖 {title}</h2></div>"
    imgs = [s[0] for s in scene_outputs]
    texts = [f"<div class='scene-text'>{s[1]}</div>" for s in scene_outputs]

    return (
        title_md,
        imgs[0] if len(imgs) > 0 else None, texts[0] if len(texts) > 0 else "",
        imgs[1] if len(imgs) > 1 else None, texts[1] if len(texts) > 1 else "",
        imgs[2] if len(imgs) > 2 else None, texts[2] if len(texts) > 2 else "",
        imgs[3] if len(imgs) > 3 else None, texts[3] if len(texts) > 3 else "",
    )


# --- UI ---
theme_config = gr.themes.Soft(
    primary_hue="purple",
    secondary_hue="blue",
    font=gr.themes.GoogleFont("Nunito"),
)

with gr.Blocks(theme=theme_config, css=CSS, title="🌙 Bedtime Story Machine") as demo:
    gr.HTML("""
    <div class="storybook-header">
        <h1>🌙 Bedtime Story Machine</h1>
        <p>Personalized illustrated bedtime stories, woven by AI just for your little one</p>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=1, min_width=300):
            gr.Markdown("### ✏️ Story Settings")
            name_input = gr.Textbox(label="Child's Name", placeholder="e.g. Luna, Max, Aria")
            age_input = gr.Slider(label="Age", minimum=2, maximum=10, value=5, step=1)
            theme_input = gr.Dropdown(
                label="Story Theme",
                choices=[
                    "A magical forest adventure",
                    "Friendly dragons and castles",
                    "Under the sea with talking fish",
                    "A trip to the moon and stars",
                    "Friendly animals in a cozy barn",
                    "A tiny fairy's garden party",
                    "Flying on a cloud to dreamland",
                    "Pirates finding treasure on a rainbow island",
                    "A rocket ship to a planet made of candy",
                ],
                value="A magical forest adventure",
                allow_custom_value=True,
            )
            extra_input = gr.Textbox(
                label="Extra Details (optional)",
                placeholder="e.g. loves dinosaurs, has a cat named Whiskers, favorite color is blue",
                lines=2,
            )
            language_input = gr.Dropdown(
                label="Language",
                choices=["English", "Français"],
                value="English",
            )
            generate_btn = gr.Button(
                "✨ Generate Bedtime Story",
                variant="primary",
                size="lg",
                elem_classes=["generate-btn"],
            )
            gr.Markdown("""
            ---
            **How it works:** AI writes a unique 4-scene story with your child as the hero, then paints a watercolor illustration for each scene.

            *~30 seconds to generate*
            """)

        with gr.Column(scale=2):
            title_output = gr.HTML()

            with gr.Group(elem_classes=["scene-card"]):
                with gr.Row():
                    img1 = gr.Image(show_label=False, container=False)
                    text1 = gr.HTML()
            with gr.Group(elem_classes=["scene-card"]):
                with gr.Row():
                    text2 = gr.HTML()
                    img2 = gr.Image(show_label=False, container=False)
            with gr.Group(elem_classes=["scene-card"]):
                with gr.Row():
                    img3 = gr.Image(show_label=False, container=False)
                    text3 = gr.HTML()
            with gr.Group(elem_classes=["scene-card"]):
                with gr.Row():
                    text4 = gr.HTML()
                    img4 = gr.Image(show_label=False, container=False)

    generate_btn.click(
        fn=build_output,
        inputs=[name_input, age_input, theme_input, extra_input, language_input],
        outputs=[title_output, img1, text1, img2, text2, img3, text3, img4, text4],
    )

    gr.HTML("""
    <div style="text-align:center; padding:1rem; color:#6b7280; font-size:0.85rem;">
        Built with 🤗 Hugging Face Inference API · Story: NVIDIA Nemotron-Mini-4B-Instruct (4B) · Art: FLUX.1-schnell (12B) · Total: ~16B params<br>
        <strong>Build Small Hackathon</strong> — Thousand Token Wood 🍄 · Powered by <strong>Modal</strong>
    </div>
    """)

if __name__ == "__main__":
    demo.launch()
