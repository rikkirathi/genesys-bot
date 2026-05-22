from fastapi import FastAPI, Request, HTTPException
import uvicorn

app = FastAPI()

@app.post("/botconnector/postutterance")
async def handle_genesys_utterance(request: Request):
    try:
        # 1. Genesys से आने वाले डेटा को रिसीव करें
        genesys_data = await request.json()
        
        # 2. यूजर का मैसेज (Text) निकालें
        user_message = genesys_data.get("utterance", "")
        conversation_id = genesys_data.get("conversationId", "")
        
        print(f"Message received from Genesys: '{user_message}' for Conv ID: {conversation_id}")

        # 3. बॉट का लॉजिक (यहाँ आप OpenAI, Rasa या अपना कस्टम कोड लगा सकते हैं)
        bot_reply = "नमस्ते! मैं आपका कस्टम टेस्टिंग बॉट हूँ। मुझे आपका यह मैसेज मिला: " + user_message
        
        if "help" in user_message.lower():
            bot_reply = "मैं आपकी क्या मदद कर सकता हूँ? आप बैलेंस, सपोर्ट या एजेंट टाइप कर सकते हैं।"
        elif "agent" in user_message.lower():
            # बॉट को बंद करके लाइव एजेंट को ट्रांसफर करने का सिग्नल
            return {
                "replyUtterance": "ठीक है, मैं आपको लाइव एजेंट से कनेक्ट कर रहा हूँ।",
                "intent": "TransferToAgent",
                "parameters": {},
                "botState": "Disconnect"
            }

        # 4. Genesys Bot Connector के स्टैंडर्ड फॉर्मेट में जवाब भेजें
        return {
            "replyUtterance": bot_reply,
            "intent": "None",
            "parameters": {},
            "botState": "MoreUtterances"  # बॉट को चालू रखने के लिए
        }

    except Exception as e:
        print(f"Error processing request: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    # लोकल टेस्टिंग के लिए पोर्ट 8000 पर चलाएं
    uvicorn.run(app, host="0.0.0.0", port=8000)
