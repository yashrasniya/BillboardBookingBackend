from openai import OpenAI

client = OpenAI(api_key='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')

re=client.images.generate(
  model="dall-e-2",
  prompt="A cute baby sea otter",
  n=1,
  size="256x256"
)
print(re.data)