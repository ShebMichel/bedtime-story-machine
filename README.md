---
title: Bedtime Story Machine
emoji: 🌙
colorFrom: indigo
colorTo: purple
sdk: gradio
sdk_version: 5.29.0
app_file: app.py
pinned: false
license: mit
short_description: Personalized illustrated bedtime stories for kids
tags:
  - hackathon
  - thousand-token-wood
  - storytelling
  - children
  - nvidia
  - nemotron
  - modal
---

# 🌙 Bedtime Story Machine

A personalized illustrated bedtime story generator, crafted just for your little one.

## Demo








<video src="https://github.com/user-attachments/assets/835aab78-4e4b-47b6-a3ae-2a1e5015d0cb" controls autoplay muted loop width="100%"></video>

## How it works

1. Enter your child's name, age, and pick a theme
2. Choose a language (English or Français)
3. AI writes a gentle 4-scene bedtime story with your child as the protagonist
4. Each scene gets a beautiful watercolor-style illustration
5. Read it together at bedtime! 🛏️

## Models Used (≤32B total)

- **Story Generation**: [nvidia/Nemotron-Mini-4B-Instruct](https://huggingface.co/nvidia/Nemotron-Mini-4B-Instruct) (4B params) — via Modal
- **Illustrations**: [black-forest-labs/FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) (12B params)
- **Total**: ~16B parameters ✅

## Infrastructure

- **Modal** — Serves Nemotron-4B on T4 GPU with vLLM
- **HF Inference API** — FLUX.1-schnell for image generation
- **Gradio** — Custom-styled frontend
- **Hugging Face Spaces** — Hosting

## Track

🍄 **Thousand Token Wood** — Build something delightful that wouldn't exist without AI.

## Badges Targeted

| Badge | Status |
|-------|--------|
| 🟩 NVIDIA Nemotron Quest | ✅ Uses Nemotron-Mini-4B |
| 🐜 Tiny Titan (≤4B) | ✅ Story model is 4B params |
| 🟢 Modal Awards | ✅ Deployed on Modal |
| 📓 Field Notes | ✅ [Blog post](https://huggingface.co/spaces/build-small-hackathon/bedtime-story-machine/discussions/1) |
| 📡 Sharing is Caring | ✅ [Agent trace](https://huggingface.co/datasets/build-small-hackathon/bedtime-story-machine-trace) |

## Links

- 🚀 [Live App](https://huggingface.co/spaces/build-small-hackathon/bedtime-story-machine)
- 📓 [Blog Post](https://huggingface.co/spaces/build-small-hackathon/bedtime-story-machine/discussions/1)
- 📡 [Agent Trace](https://huggingface.co/datasets/build-small-hackathon/bedtime-story-machine-trace)
- 💻 [GitHub](https://github.com/ShebMichel/bedtime-story-machine)

## Built for

[Build Small Hackathon](https://huggingface.co/build-small-hackathon) by Gradio & Hugging Face
