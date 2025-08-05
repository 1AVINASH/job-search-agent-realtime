* Model used -> https://huggingface.co/TheBloke/deepseek-coder-6.7B-instruct-GGUF


## Steps to run locally
* Host a model locally like me, or use OpenAI directly (but it will cost you money)
* Once you have the model downloaded (example link is provided above), add it to the models directory and update the docker-compose file to point to this model
* To run this, just run `docker compose up --build -d`