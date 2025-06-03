# Using the vLLM API Client

YourBench can talk to a self-hosted [vLLM](https://github.com/vllm-project/vllm) server by setting
`provider: vllm` and providing the server URL via `base_url` in your configuration.

```yaml
model_list:
  - model_name: Qwen/Qwen3-4B
    provider: vllm
    base_url: "http://localhost:8000/v1"
    api_key: $VLLM_API_KEY  # optional if your server does not require one
```

The vLLM server exposes an OpenAI-compatible `/chat/completions` endpoint. The new
client will be used automatically when `provider` is set to `vllm`.
