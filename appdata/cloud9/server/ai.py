from llama_cpp import Llama

from paths import MODELS_DIR

MODEL_PATH = MODELS_DIR / "qwen2.5-1.5b-instruct-q4_k_m.gguf"

SYSTEM_PROMPT = (
    "You are the AI Assistant on Cloud9, a learning dashboard for a curious kid. "
    "Talk like a friendly, patient helper, not a corporate assistant. "
    "Keep replies short - a few sentences at most - and use plain, simple words. "
    "You help with reading, writing, spelling, and coding small scripts, and you're happy to just chat. "
    "If asked to explain an error or a new word, break it into small, encouraging steps. "
    "Never discuss violence, weapons, drugs, dating, or other adult topics - if asked, gently steer back "
    "to something fun to learn or build instead. If you don't know something, say so plainly."
)

_llm = None


def _get_llm():
    global _llm
    if _llm is None:
        _llm = Llama(
            model_path=str(MODEL_PATH),
            n_ctx=4096,
            n_threads=8,
            verbose=False,
        )
    return _llm


def is_model_ready():
    return MODEL_PATH.exists()


def chat_stream(message, history=None):
    history = history or []
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for turn in history:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": message})

    llm = _get_llm()
    stream = llm.create_chat_completion(
        messages=messages,
        max_tokens=300,
        temperature=0.7,
        stream=True,
    )
    for chunk in stream:
        content = chunk["choices"][0]["delta"].get("content")
        if content:
            yield content
