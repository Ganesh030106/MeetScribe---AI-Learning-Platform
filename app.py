import os
import re
import json
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

# --- Configuration ---
print("Starting MeetScribe server...")
load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 1. Configure the Gemini API
try:
    api_key = os.environ["GEMINI_API_KEY"]
    if not api_key:
        raise KeyError
    genai.configure(api_key=api_key)
    print("Gemini API configured successfully.")
except KeyError:
    print("\n" + "="*50)
    print("FATAL ERROR: GEMINI_API_KEY not found.")
    print("Please create a file named '.env' in this directory and add:")
    print("GEMINI_API_KEY=your_api_key_here")
    print("="*50 + "\n")
    exit()

# 2. This is the Master Prompt for the Gemini Agent.
# It's the most important part! It tells Gemini exactly what to do
# and forces it to return a clean JSON object.
MEETING_ANALYSIS_PROMPT = """
You are "MeetScribe," an expert meeting analyst. You will be given a video file of a meeting.
Your task is to analyze the entire video and audio and return a clean, valid JSON object.
Do not, under any circumstances, wrap the JSON in markdown (```json ... ```).
The JSON object must have exactly these three top-level keys:

1.  "summary": A concise, one-paragraph summary of the meeting's purpose, key discussions, and final outcomes.
2.  "action_items": A list of objects. Each object must have:
    - "task": (string) The specific action item.
    - "owner": (string) The person or group assigned. Default to "Unassigned" if not mentioned.
    - "deadline": (string) The due date. Default to "Not specified" if not mentioned.
3.  "sentiment": A brief, 2-3 sentence analysis of the team's overall sentiment (e.g., optimistic, concerned, collaborative), based on tone of voice and language.

Analyze the spoken words, the tone of voice, and any text visible on slides.
"""

def clean_gemini_output(text_response):
    """
    Cleans the raw text output from Gemini to extract the JSON.
    It removes the markdown wrapper (```json ... ```) if it exists.
    This makes the demo more reliable.
    """
    match = re.search(r'```json\s*(\{.*?\})\s*```', text_response, re.DOTALL | re.IGNORECASE)
    if match:
        print("Cleaning markdown from Gemini output.")
        return match.group(1)
    # If no markdown, assume it's a clean JSON string
    return text_response.strip()

# --- Routes ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    print("Serving index.html")
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_meeting():
    """Handles the video upload and analysis."""
    print("\nReceived new /analyze request.")
    if 'video' not in request.files:
        print("Error: No video file in request.")
        return jsonify({"error": "No video file provided"}), 400

    file = request.files['video']
    if file.filename == '':
        print("Error: No selected file.")
        return jsonify({"error": "No selected file"}), 400

    # We need to save the file locally *first* to upload it to the API
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    video_file_gemini = None  # To store the Gemini file object

    try:
        # 1. Save the file temporarily
        print(f"Saving temporary file: {filepath}")
        file.save(filepath)

        # 2. Upload the file to the Gemini API
        # This is a key step. It uploads the file and makes it ready for processing.
        print(f"Uploading file to Gemini API: {filepath}...")
        video_file_gemini = genai.upload_file(path=filepath, display_name=file.filename)
        
        # 3. Poll until the file is 'ACTIVE' (ready for use)
        # This is CRITICAL for a good demo, otherwise the API will fail.
        print(f"Waiting for file '{video_file_gemini.name}' to be processed...")
        while video_file_gemini.state.name == "PROCESSING":
            print("...")
            # Time delay to avoid spamming the API
            import time
            time.sleep(5) 
            video_file_gemini = genai.get_file(video_file_gemini.name)

        if video_file_gemini.state.name == "FAILED":
            print(f"Error: File processing failed. {video_file_gemini.state}")
            raise Exception("File processing failed on the server.")
        
        print("File is now ACTIVE and ready for analysis.")

        # 4. Call the Gemini API
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")
        
        # Send the prompt *and* the video file handle
        print("Sending prompt and video to Gemini 1.5 Pro...")
        response = model.generate_content(
            [MEETING_ANALYSIS_PROMPT, video_file_gemini],
            request_options={"timeout": 1000} # Increase timeout for long videos
        )

        print("Received response from Gemini.")
        
        # 5. Extract and send the clean JSON back to the frontend
        cleaned_json_string = clean_gemini_output(response.text)
        analysis_data = json.loads(cleaned_json_string)
        
        print("Analysis complete. Sending JSON to frontend.")
        return jsonify(analysis_data)

    except Exception as e:
        print(f"\n--- An Error Occurred ---")
        print(f"Error: {e}")
        print(f"---------------------------\n")
        return jsonify({"error": str(e)}), 500
    
    finally:
        # 6. Clean up: Delete the local file and the file on Gemini's server
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Deleted local file: {filepath}")
        if video_file_gemini:
            genai.delete_file(video_file_gemini.name)
            print(f"Deleted remote file: {video_file_gemini.name}")

if __name__ == '__main__':
    print("MeetScribe server starting on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)