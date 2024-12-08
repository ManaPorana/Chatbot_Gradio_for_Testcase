import gradio as gr
import google.generativeai as genai

# ตั้งค่า API Key สำหรับ Google Generative AI
API_KEY = "AIzaSyBw2mqZ45BxGvcwS9YLDa8ru3Fb3mHnP-0"  # ใส่ API Key ของคุณ
genai.configure(api_key=API_KEY)

def format_history(msg: str, history: list[list[str, str]], system_prompt: str):
    chat_history = [{"role": "system", "content": system_prompt}]
    for query, response in history:
        chat_history.append({"role": "user", "content": query})
        chat_history.append({"role": "assistant", "content": response})
    chat_history.append({"role": "user", "content": msg})
    return chat_history

def generate_response(msg: str, history: list[list[str, str]], system_prompt: str, *args):
    # สร้างข้อความ prompt จากประวัติการสนทนา
    chat_history = format_history(msg, history, system_prompt)
    prompt = "\n".join([entry["content"] for entry in chat_history])  # รวมข้อความเป็น prompt เดียว

    # เรียกใช้งาน Google Generative AI โมเดล Gemini 1.5 Flash
    model = genai.GenerativeModel("gemini-1.5-flash")  # ใช้โมเดล Gemini 1.5 Flash
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=700
        )
    )
    
    message = response.text  # ดึงข้อความคำตอบ
    yield message

def handle_file_upload(file):
    if file is not None:
        return f"Uploaded file: {file.name}"
    return "No file uploaded."

chatbot = gr.ChatInterface(
    generate_response,
    chatbot=gr.Chatbot(
        avatar_images=["user.jpg", "chatbot.png"],
        height="64vh"
    ),
    additional_inputs=[
        gr.Textbox(
            "You are helpful AI And have expertise in software Tester",
            label="System Prompt"
        ),
        gr.File(label="Upload File", file_types=[".png", ".jpg", ".jpeg", ".pdf"], type="filepath", interactive=True)
    ],
    title="Chatbot with Gradio-GUI",
    description="Feel free to ask any question.",
    theme="soft",
    submit_btn="Summit",
    retry_btn="🔄 Regenerate Response",
    undo_btn="↩ Delete Previous",
    clear_btn="🗑️ Clear Chat"
)

# Launch the chatbot interface
chatbot.launch()