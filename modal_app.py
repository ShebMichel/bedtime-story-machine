"""Modal deployment for NVIDIA Nemotron-Mini-4B-Instruct.

Deploy: modal deploy modal_app.py
Test:   modal run modal_app.py
"""
import modal

app = modal.App("bedtime-story-machine")

image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install("vllm==0.8.5", "huggingface_hub")
)

MODEL_NAME = "nvidia/Nemotron-Mini-4B-Instruct"

@app.cls(
    image=image,
    gpu="T4",
    timeout=300,
    container_idle_timeout=120,
    secrets=[modal.Secret.from_name("huggingface-secret")],
)
class NemotronModel:
    @modal.enter()
    def load_model(self):
        from vllm import LLM, SamplingParams
        self.llm = LLM(model=MODEL_NAME, max_model_len=2048)
        self.sampling_params = SamplingParams(temperature=0.8, max_tokens=1024)

    @modal.method()
    def generate(self, prompt: str) -> str:
        from vllm import SamplingParams
        params = SamplingParams(temperature=0.8, max_tokens=1024)
        outputs = self.llm.generate([prompt], params)
        return outputs[0].outputs[0].text

    @modal.web_endpoint(method="POST")
    def chat(self, request: dict) -> dict:
        from vllm import SamplingParams
        messages = request.get("messages", [])
        # Format as chat
        prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "user":
                prompt += f"<|im_start|>user\n{content}<|im_end|>\n"
            elif role == "assistant":
                prompt += f"<|im_start|>assistant\n{content}<|im_end|>\n"
        prompt += "<|im_start|>assistant\n"

        params = SamplingParams(
            temperature=request.get("temperature", 0.8),
            max_tokens=request.get("max_tokens", 1024),
        )
        outputs = self.llm.generate([prompt], params)
        text = outputs[0].outputs[0].text
        return {"choices": [{"message": {"content": text}}]}


@app.local_entrypoint()
def main():
    model = NemotronModel()
    result = model.generate.remote("Write a 2-sentence bedtime story about a cat.")
    print(f"Result: {result}")
