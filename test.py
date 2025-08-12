import google.generativeai as genai

genai.configure(api_key="AIzaSyDP4EoV09j16IlXro8EGNuF1Tpc1W-WWg0")

models = genai.list_models()
for model in models:
    print(model.name, model.supported_generation_methods)
