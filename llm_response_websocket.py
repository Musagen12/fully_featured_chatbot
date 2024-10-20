from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.query_llm import process_input  # Your function to process LLM input
from src.text_to_speech import talk
import logging
import asyncio
import json

app = FastAPI()
logging.basicConfig(level=logging.INFO)

@app.websocket("/ws/llm_response")
async def llm_response(websocket: WebSocket):
    await websocket.accept()
    logging.info("WebSocket connection established.")

    try:
        while True:
            query = await websocket.receive_text()  # Receive query from Speech Recognition Project
            logging.info(f"Received query: {query}")

            try:
                # Process the input using the LLM (asynchronously)
                llm_response = await asyncio.to_thread(process_input, query)

                # Log the received LLM response and its type
                logging.info(f"LLM Response: {llm_response} | Type: {type(llm_response)}")

                # Prepare response to send
                response_to_send = prepare_response(llm_response)

                # Log the response that will be sent back to the client
                logging.info(f"Sending response: {response_to_send}")

                # Stream the LLM response back to the Speech Recognition Project
                await websocket.send_text(response_to_send)

                # Call talk() after sending the response
                talk(response_to_send)  # Speak the response

            except Exception as e:
                logging.error(f"Error processing input: {e}")
                await websocket.send_text("An error occurred while processing your request.")

    except WebSocketDisconnect:
        logging.info("LLM response WebSocket disconnected.")

def prepare_response(llm_response):
    """Prepare the response based on the LLM output."""
    if llm_response is None:
        logging.warning("LLM response is None, sending default message.")
        return "No response generated."

    # Check if llm_response is a dictionary and convert it to a string
    if isinstance(llm_response, dict):
        logging.info("LLM response is a dictionary, converting to string.")
        llm_response = json.dumps(llm_response)

    # Prepare and return the response
    if isinstance(llm_response, str):
        return llm_response
    else:
        return str(llm_response)  # Fallback to string conversion

if __name__ == "__main__":
    import uvicorn
    # Start the FastAPI server on localhost at port 8001
    uvicorn.run(app, host="127.0.0.1", port=8001)
