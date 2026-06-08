# 🌙 Building the Bedtime Story Machine: Small Models, Big Imagination

## The Spark

This weekend, while playing with my son before bedtime, he asked me the same thing he asks every night: *"Dad, tell me a story!"* And like every night, I scrambled to come up with something new.

That's when it hit me — what if AI could generate a unique, personalized bedtime story every single night, with my son as the hero? Not a generic story from a database, but something fresh, illustrated, and tailored to him.

So I built the **Bedtime Story Machine** for the Hugging Face Build Small Hackathon.

## The Concept

The app takes four inputs:
- Your child's **name** (they become the protagonist)
- Their **age** (vocabulary adapts)
- A **story theme** (dragons, ocean, space, etc.)
- **Optional details** (favorite pet, hobby, etc.)

Then it generates a 4-scene bedtime story with watercolor-style illustrations for each scene. Every story is unique. Every night is a new adventure.

## Technical Choices

### Story Generation: NVIDIA Nemotron-Mini-4B-Instruct

I chose Nemotron-Mini-4B for story generation. At just 4 billion parameters, it's genuinely tiny — but surprisingly capable at creative writing when given the right prompts. The model runs on Modal with a T4 GPU, keeping costs minimal.

The key was prompt engineering: I ask for structured JSON output with both story text and image prompts, specify the child's age for vocabulary calibration, and insist on a calming, sleep-friendly tone.

### Illustrations: FLUX.1-schnell

For illustrations, FLUX.1-schnell (12B params) generates beautiful images fast. The trick was crafting image prompts that consistently produce a "children's book illustration" style — I append "soft watercolor style, warm colors, whimsical" to every scene description.

### Total: ~16B parameters

Well under the 32B hackathon limit. The whole pipeline could theoretically run on a single consumer GPU.

### Multi-language Support

Since I'm in a French-speaking household, I added a language toggle. Nemotron handles French surprisingly well — the story text generates in French while image prompts stay in English (FLUX works better with English prompts).

## Deployment Stack

- **Modal** — Serves Nemotron-4B with cold-start optimization
- **HF Inference API** — FLUX.1-schnell for image generation
- **Gradio** — Frontend with custom CSS for a storybook feel
- **Hugging Face Spaces** — Hosting

## Challenges & Learnings

1. **JSON reliability from small models** — 4B models sometimes break JSON formatting. I added regex extraction as a safety net, pulling the JSON object even if the model adds extra text around it.

2. **Provider availability** — Not all models are available on all inference providers. Nemotron wasn't available on any free provider, which pushed me toward Modal — a blessing in disguise for the Modal prize track.

3. **Image consistency** — Getting FLUX to produce a consistent "storybook" art style required careful prompt suffixes. Without them, the style varied wildly between scenes.

4. **Keeping it calming** — The prompt engineering for bedtime-appropriate content was crucial. Specifying "gentle, calming tone" and "peaceful ending where the child falls asleep" made a real difference.

## What I'd Add Next

- Audio narration (TTS reading the story aloud)
- A "story history" to save favorites
- PDF export for printing
- Fine-tuned model on children's literature for better narrative structure

## Try It

→ [Bedtime Story Machine on HF Spaces](https://huggingface.co/spaces/build-small-hackathon/bedtime-story-machine)

Built with ❤️ for the Build Small Hackathon — Thousand Token Wood track 🍄
