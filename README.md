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
---

# 🌙 Bedtime Story Machine

A personalized illustrated bedtime story generator, crafted just for your little one.

## Demo

https://github.com/user-attachments/assets/bedtime_story.mp4

https://github.com/ShebMichel/bedtime-story-machine/raw/main/bedtime_story.mp4

## How it works

1. Enter your child's name, age, and pick a theme
2. AI writes a gentle 4-scene bedtime story with your child as the protagonist
3. Each scene gets a beautiful watercolor-style illustration
4. Read it together at bedtime! 🛏️

## Models Used (≤32B total)

- **Story Generation**: [Qwen/Qwen2.5-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-7B-Instruct) (7B params)
- **Illustrations**: [black-forest-labs/FLUX.1-schnell](https://huggingface.co/black-forest-labs/FLUX.1-schnell) (12B params)
- **Total**: ~19B parameters ✅

## Track

🍄 **Thousand Token Wood** — Build something delightful that wouldn't exist without AI.

## Built for

[Build Small Hackathon](https://huggingface.co/build-small-hackathon) by Gradio & Hugging Face
