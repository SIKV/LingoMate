from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from gradio.routes import mount_gradio_app
from ui import gradio_app

app = FastAPI()

@app.get("/", include_in_schema=False)
def redirect_to_gradio():
    return RedirectResponse(url="/app")

app = mount_gradio_app(app, gradio_app, path="/app")
