# CaptionCraft AI

CaptionCraft AI is a lightweight Python app that turns an uploaded image and a selected mood into a social-media caption with relevant hashtags. It uses Gradio for the interface, Pillow for basic image analysis, and Groq for caption generation.

## Live demo

No public live demo is configured in this repository at the moment.

## Features

- Upload an image in the browser
- Choose a mood or emotion for the caption
- Get basic image metadata such as dimensions, orientation, and dominant colors
- Generate a concise, social-ready caption plus hashtags
- Run locally or in Docker

## How it works

Image upload
→ Basic image property analysis
→ User-selected mood/emotion
→ Prompt construction
→ Groq LLM
→ Social-media caption + hashtags
→ Gradio output

## Accurate image-analysis explanation

This project does not perform full computer-vision reasoning or semantic scene understanding. The image analysis is intentionally basic and limited to:

- image size in pixels
- aspect ratio and orientation (landscape, portrait, or square)
- dominant or common color groupings derived from the image
- brightness range estimate for tone guidance

It does not claim to perform:

- object detection
- face recognition
- semantic scene understanding
- full visual-language reasoning

## Tech stack

- Python 3
- Gradio
- Pillow
- Groq API
- Docker

## Architecture and data flow

1. A user uploads an image through the Gradio UI.
2. The app validates the input and converts the image to a standard RGB representation for analysis.
3. A basic analysis extracts width, height, orientation, and dominant color information.
4. The selected emotion is combined with those visual properties into a prompt.
5. The prompt is sent to the configured Groq model.
6. The LLM returns a caption and the app appends relevant hashtags.
7. The result is displayed in the browser.

## Setup

1. Clone the repository.
2. Create a virtual environment.
3. Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4. Create a local `.env` file from the example:

```bash
cp .env.example .env
```

5. Add your Groq API key and preferred configuration values.

## Environment variables

Use a local `.env` file for secrets. The project expects:

```bash
GROQ_API_KEY=your_key_here
GROQ_MODEL=llama-3.3-70b-versatile
HOST=0.0.0.0
PORT=7862
```

## Docker usage

Build the image:

```bash
docker build -t captioncraft-ai .
```

Run the container:

```bash
docker run --rm -p 7862:7862 --env-file .env captioncraft-ai
```

The app listens on port `7862` by default and binds to `0.0.0.0`.

## Example workflow

1. Open the Gradio app in a browser.
2. Upload a photo.
3. Select a mood such as Happy, Peaceful, or Professional.
4. Click the generate button.
5. Review the caption and hashtags produced.

## Screenshots

### Upload screen

Placeholder: add a screenshot of the image upload and mood selection UI here.

### Generated caption result

Placeholder: add a screenshot of the generated caption output here.

### Different mood examples

Placeholder: add screenshots for Happy, Peaceful, and Professional caption outputs here.

## Known limitations

- Caption quality depends on the chosen Groq model and prompt design.
- The image analysis is intentionally basic and not a full vision system.
- Output stays concise and social-media oriented, which is useful but not perfect for every context.
- Groq API usage requires a valid API key and quota.

## Future improvements

- Add a richer mood/style library
- Add optional caption length controls
- Support a local fallback when the API is unavailable
- Improve prompt templates for different content styles
- Add basic logging and usage analytics

## Security note

This project stores secrets in a local `.env` file, not in source control. The repository includes a `.gitignore` to prevent accidental commits of `.env` files and Python bytecode artifacts.

## License

This project does not include a license file yet. Add one before publishing publicly if you intend to distribute it widely.
