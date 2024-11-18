# main.py
import gradio as gr
from agent import CaptionGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_caption(image, emotion):
    try:
        if image is None:
            return "Please upload an image first."
        
        logger.info(f"Generating caption for emotion: {emotion}")
        generator = CaptionGenerator()
        caption = generator.generate(image, emotion)
        return caption
    except Exception as e:
        logger.error(f"Error generating caption: {str(e)}")
        return f"Error generating caption: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # AI Caption Generator with Image Analysis 📸✨
    Upload an image and select an emotion to generate a contextual caption!
    """)
    
    with gr.Row():
        with gr.Column():
            image_input = gr.Image(type="pil", label="Upload your image")
            emotion_input = gr.Dropdown(
                choices=[
                    "Happy", "Excited", "Peaceful", "Professional", 
                    "Funny", "Nostalgic", "Inspirational", "Romantic"
                ],
                value="Happy",
                label="Select the emotion for your caption"
            )
            generate_btn = gr.Button("✨ Analyze & Generate Caption", variant="primary")
        
        with gr.Column():
            caption_output = gr.Textbox(
                label="Generated Caption", 
                lines=5,
                placeholder="Your AI-generated caption will appear here..."
            )
    
    gr.Markdown("""
    ### Features:
    - Advanced image analysis
    - Emotion-aware caption generation
    - Contextual hashtag suggestions
    - Perfect for social media posts
    """)
    
    generate_btn.click(
        fn=generate_caption,
        inputs=[image_input, emotion_input],
        outputs=caption_output
    )

if __name__ == "__main__":
    # Launch the application with specific host and port
    demo.launch(server_name="0.0.0.0", server_port=7862)