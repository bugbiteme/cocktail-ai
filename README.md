# cocktail-ai-api

RestAPI integration to openAI and DALL-E to create a cocktail recipe based on a prompt.  

API call will also return a DALL-E generated image based on the cocktail.  

`OPENAI_API_KEY` is an environment variable on your system on in your container that has your OpenAI API key

To be called from web front end.

To build and run a container:  

```
podman build -t cocktail-ai .
podman run -e OPENAI_API_KEY=$OPENAI_API_KEY -e DEBUG=[true/false] -p 8000:8080 cocktail-ai
```

This command runs the podman container, mapping port 8000 on your local machine to port 8080 in the podman container (which your FastAPI app should be listening on).  
  
## To test locally

If you're not already doing so, consider using a virtual environment. This isolates your project's dependencies from the global Python environment and can often resolve conflicts and dependency issues.  
  
```
python -m venv venv
source venv/bin/activate  # For Unix or MacOS
venv\Scripts\activate     # For Windows

pip install --upgrade pip
pip install -r requirements.txt

export OPENAI_API_KEY=<your own OpenAI key>

export DEBUG=true #to call mock API that is free and fast for testing purposes

uvicorn main:app --reload
```

Note: If using OpenShift DevSpaces, there is no need to create a virtual environment (venv). Also no need to run pip install locally.

## To clean up python virtual environment
- If you are currently inside a virtual environment, you'll need to deactivate it first. You can do this by running the deactivate command in your terminal or command prompt.  

```
deactivate
```

This will return you to your system's default Python environment.  
  
Once you've deactivated the virtual environment, you can simply delete its directory to remove it completely. The virtual environment is just a directory containing all the necessary files, so removing this directory will delete the environment.

```
rm -rf venv  # Unix/Linux/MacOS
rmdir /s /q venv  # Windows
```
For some swagger action:

```
<url>/docs
<url>/redocs
```
