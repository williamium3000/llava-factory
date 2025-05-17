from transformers import LlamaForCausalLM, AutoTokenizer

from . import register_llm

@register_llm('tinyllama')
@register_llm('vicuna')
def return_tinyllamaclass():
    def tokenizer_and_post_load(tokenizer):
        tokenizer.pad_token = tokenizer.unk_token
        return tokenizer
    return LlamaForCausalLM, (AutoTokenizer, tokenizer_and_post_load)
