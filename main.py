from fastapi import FastAPI, Request, HTTPException
import uvicorn

app = FastAPI()

# Genesys जब भी वैलिडेशन चेक करेगा, वह इस / रूट पर या खाली बॉडी भेजता है
@app.get("/")
@app.post("/")
async def root_ping():
    return {"status": "alive", "message": "Bot is working"}

@app.post("/botconnector/postutterance")
async def handle_genesys_utterance(request: Request):
    try:
        # अगर Genesys कोई खाली या बिना बॉडी की वैलिडेशन रिक्वेस्ट भेजता है
        body_bytes = await request.body()
        if not body_bytes:
            return {"status": "validated"}
            
        genesys_data = await request.json()
        user_message = genesys_data.get("utterance", "")
        
        # अगर यह सिर्फ टेस्ट/पिंग यूआरएल चेक है
        if not user_message:
            return {"status": "validated"}
            
        bot_reply = "नमस्ते! मैं आपका कस्टम टेस्टिंग बॉट हूँ। मुझे आपका मैसेज मिला: " + user_message
        
        return {
            "replyUtterance": bot_reply,
            "intent": "None",
            "parameters": {},
            "botState": "MoreUtterances"
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        # वैलिडेशन फेल होने से बचाने के लिए खाली या एरर रिक्वेस्ट पर भी सक्सेस रिस्पॉन्स देना बेहतर है
        return {"status": "validated"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
