from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from grok_client import GrokClient

app = FastAPI()

# Your cookie values (Paste all cookies you can find in F12)
cookies = {
    "x-anonuserid": "ffdd32e1",
    "x-challenge": "TkC4D..",
    "x-signature": "fJ0...",
    "sso": "ey..."
}

# Initialize the client
client = GrokClient(cookies)

@app.get("/v1/models")
async def get_models():
    try:
        models = ["grok-3"]
        return jsonable_encoder(models)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/completions")
async def create_completion(request: dict):
    try:
        data = request
        
        # model = data.get('model', 'grok-3')
        messages = data.get('messages', [])
        # temperature = data.get('temperature', 1.0)
        
        if not messages:
            raise HTTPException(status_code=400, detail="Messages are required")
        
        response = client.send_message(messages)
        
        return {
            "choices": [{
                "message": {
                    "content": response
                }
            }]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8046)