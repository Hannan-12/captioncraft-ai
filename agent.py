import os
from groq import Groq
from dotenv import load_dotenv
import logging
from PIL import Image

logger = logging.getLogger(__name__)

class CaptionGenerator:
    def __init__(self):
        load_dotenv()
        self.groq_token = os.getenv("GROQ_API_KEY")
        
        if not self.groq_token:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.groq_client = Groq(api_key=self.groq_token)
        logger.info("CaptionGenerator initialized successfully")

    def _analyze_image_properties(self, image):
        """Extract basic image properties"""
        try:
            # Get image dimensions
            width, height = image.size
            aspect_ratio = width / height
            
            # Determine orientation
            if aspect_ratio > 1.1:
                orientation = "landscape"
            elif aspect_ratio < 0.9:
                orientation = "portrait"
            else:
                orientation = "square"
            
            # Get dominant colors
            colors = image.convert('RGB').getcolors(maxcolors=1000)
            if colors:
                dominant_colors = sorted(colors, key=lambda x: x[0], reverse=True)[:3]
                color_names = [self._get_color_name(color[1]) for color in dominant_colors]
            else:
                color_names = ["varied"]
            
            return {
                "orientation": orientation,
                "size": f"{width}x{height}",
                "colors": color_names
            }
            
        except Exception as e:
            logger.error(f"Error analyzing image properties: {str(e)}")
            raise

    def _get_color_name(self, rgb):
        """Convert RGB to basic color name"""
        r, g, b = rgb
        if r > 200 and g > 200 and b > 200:
            return "white"
        elif r < 50 and g < 50 and b < 50:
            return "black"
        elif r > g and r > b:
            return "red"
        elif g > r and g > b:
            return "green"
        elif b > r and b > g:
            return "blue"
        else:
            return "mixed"

    def generate(self, image, emotion):
        try:
            logger.info("Starting caption generation process")
            
            # Get image properties
            image_properties = self._analyze_image_properties(image)
            logger.info(f"Image properties analyzed: {image_properties}")
            
            # Generate caption using Groq
            caption = self._generate_caption_with_groq(image_properties, emotion)
            logger.info("Caption generation completed")
            
            return caption
            
        except Exception as e:
            logger.error(f"Error in generate method: {str(e)}")
            raise

    def _generate_caption_with_groq(self, image_properties, emotion):
        """Generate caption using Groq"""
        try:
            prompt = self._construct_prompt(image_properties, emotion)
            
            response = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": """You are a creative social media caption writer who specializes in creating engaging, 
                        emotion-based captions. You excel at incorporating visual elements and maintaining consistent emotional tone.remember you have to be concise."""
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=300,
            )
            
            caption = response.choices[0].message.content
            return self._format_caption(caption, emotion, image_properties)
            
        except Exception as e:
            logger.error(f"Error in Groq caption generation: {str(e)}")
            raise

    def _construct_prompt(self, image_properties, emotion):
        """Construct detailed prompt for caption generation"""
        emotion_guides = {
            "Happy": ("joyful and upbeat", "happiness, celebration, positivity"),
            "Excited": ("energetic and enthusiastic", "excitement, adventure, thrill"),
            "Peaceful": ("serene and calming", "tranquility, relaxation, harmony"),
            "Professional": ("polished and business-appropriate", "success, competence, expertise"),
            "Funny": ("witty and humorous", "humor, fun, entertainment"),
            "Nostalgic": ("heartwarming and reminiscent", "memories, past times, reflection"),
            "Inspirational": ("uplifting and motivational", "inspiration, growth, achievement"),
            "Romantic": ("loving and tender", "love, romance, affection")
        }

        emotion_tone, themes = emotion_guides.get(emotion, ("engaging", "general positivity"))
        colors_desc = ", ".join(image_properties["colors"])

        return f"""Create a {emotion_tone} social media caption for a {image_properties['orientation']} image with {colors_desc} tones.

Content Guidelines:
1. Theme: Focus on {themes}
2. Tone: Maintain a {emotion.lower()} emotional feel throughout
3. Visual Elements: Incorporate {colors_desc} colors and {image_properties['orientation']} composition
4. Structure: Write 2-3 engaging sentences
5. Hashtags: Include 4-5 relevant hashtags that match both the emotion and visual elements

Style Requirements:
- Be creative and authentic
- Avoid clichés
- Keep it social media-friendly
- Make it relatable and engaging

Consider these elements while creating a caption that would make someone want to engage with a {image_properties['orientation']} photo featuring {colors_desc} tones.

Example format:
[Creative opening connecting visual elements with emotion]
[Supporting sentence enhancing the emotional impact]

#relevanthashtag1 #relevanthashtag2 #relevanthashtag3 #emotionhashtag"""

    def _format_caption(self, caption, emotion, image_properties):
        """Format and enhance the generated caption"""
        caption = caption.strip()
        
        if '#' not in caption:
            # Create hashtags based on emotion and image properties
            emotion_hashtags = {
                "Happy": ["happy", "joy", "smile"],
                "Excited": ["excited", "adventure", "thrill"],
                "Peaceful": ["peaceful", "calm", "serenity"],
                "Professional": ["professional", "success", "business"],
                "Funny": ["funny", "humor", "fun"],
                "Nostalgic": ["throwback", "memories", "nostalgia"],
                "Inspirational": ["inspiration", "motivation", "growth"],
                "Romantic": ["love", "romance", "heart"]
            }
            
            # Combine emotion hashtags with image properties
            visual_hashtags = [
                image_properties['orientation'],
                *image_properties['colors'][:2]
            ]
            
            all_hashtags = emotion_hashtags.get(emotion, ["lifestyle"]) + visual_hashtags
            hashtag_string = " ".join([f"#{tag.lower()}" for tag in all_hashtags if tag != "mixed"])
            
            caption += f"\n\n{hashtag_string}"
        
        return caption