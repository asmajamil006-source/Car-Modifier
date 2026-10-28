# HondaForge - AI Honda customizer (Python / Streamlit)

Setup
    pip install -r requirements.txt
    streamlit run app.py

Optional keys (the app still runs without them)
    ANTHROPIC_API_KEY   full AI assistant (otherwise offline rule-based answers)
    HF_TOKEN            free Hugging Face token for the AI Real Photo tab
    CLAUDE_MODEL / PHOTO_MODEL   override the default models

Real 3D models (optional)
    Put a car model at assets/models/<key>.glb (keys: civic, city, accord, hrv, jazz, crv, brv, amaze, brio).
    The 3D tab loads it, recolours paint/rims/glass by material name, and falls back to the built-in model if none exists.
    Check each model's licence before using or sharing it. Ride height does not move imported models.

Files
    app.py              Streamlit UI, cost/stats/advice logic, AI calls
    assets/data.js      model shapes and colour/option data
    assets/render2d.js  studio-style 2D renderer
    assets/viewer2d.html, viewer3d.html   templates the app fills with your build
