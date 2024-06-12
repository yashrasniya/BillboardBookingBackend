from gradio_client import Client

client = Client("yashrasniya/stabilityai-stable-diffusion-xl-base-1.0")
result = client.predict(
		param_0="a cock cola billboard ",
		api_name="/predict"
)
print(result)