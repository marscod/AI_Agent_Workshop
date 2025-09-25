# AI Agent Workshop Setup Guide
Checkout latest slides [here](https://github.com/marscod/AI_Agent_Workshop/tree/main/slides).

Hands-on Session Requirements:

Today, we will utilize LLM via API by signing up for GROQ Inference (which offers a free trial) or XAI-Grok2 API (which provides a free tier in exchange for sharing content).
Alternatively, you can run an LLM locally, but you'll also need to run the Colab Notebook locally. (Optional Tools: ollama, LLM Studio)


Colab is available here: https://gist.github.com/marscod/9e1cd2dfd07d8448d52214a63851a394

Follow these steps to set up your environment:  

## 1. Fork the Repository  
Click the **Fork** button on GitHub to create your own copy of the repository.  

## 2. Get an API Key (XAI Grok2)
1. Visit the [X.AI API Documentation](https://docs.x.ai/docs/overview) to obtain your API key.
2. Use the provided [`.env_sample` file](https://github.com/marscod/AI_Agent_Workshop/blob/main/Agents/.env_sample) as a template to create your own `.env` file at `Agents/.env`.
3. Add your API key(s) to the new `.env` file. You can leave the `GROQ_API_KEY` as is if you're using Grok2.
```bash
GROQ_API_KEY="YOUR GROQ KEY"
XAI_API_KEY="YOUR XAI KEY"
```

## 3. Open the Forked Repository in GitHub Codespaces  
Modify the URL by replacing `github.com` with `github.dev`.  

## 4. Sign in to GitHub  
Sign in using your GitHub account to proceed.  

## 5. Select a Deployment  
A minimal resource allocation (e.g., **2 cores**) is sufficient.  

> ⚠️ **Note:** To avoid unnecessary charges, stop the server once you complete the task, even if it is idle.  
> Open [GitHub Codespaces](https://github.com/codespaces), select `...` for the codespace, and choose **Stop**.

## 6. Wait for VS Code to Launch  
The environment will open in **Visual Studio Code**, and Python installation will begin automatically.  

## 7. Open the Terminal  
Access the terminal from the **VS Code** interface.  

## 8. Run the Required Commands  
Follow the instructions in the repository to set up your environment.  

```bash
./setup.sh 
source venv/bin/activate
```

### Run Server
```bash
./run.sh
```

8. (Optional) Make the Server Public  
If needed, you can expose the port to the public, allowing others to access your AI Agent.  

# Contribution
We welcome contributions! Feel free to submit a Pull Request (PR) from your forked repository.
