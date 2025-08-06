Hi!
You have landed on an automated job finder app. Based on the prompts (example prompts provided), it then crawls the web using Tavily which is a search engine specifically designed for AI agents and LLMs using playwright which is a framework for interacting with the web.

---

## Steps to run locally
* Host a model locally like me (Model used -> https://huggingface.co/TheBloke/deepseek-coder-6.7B-instruct-GGUF), or use OpenAI directly after signing up on https://platform.openai.com/account
* Once you have the model downloaded add it to the models directory and update the docker-compose file to point to this model. Then add its service in the docker compose file, host it on the same network and communicate with it by providing the base url in the ChatOpenAI class
* To run this, I have written an orchestrator step that runs the services sequentially. They can also be run partially from docker compose. To run them in the correct order, run `bash orchestrator.sh`, or make the file an executable by runnin `chmod +x orchestrator.sh` and then run `./orchestrator.sh`