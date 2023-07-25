

import openai

openai.api_key = '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'

model_engine = "text-davinci-003"


async def ask(prompt):

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=500,
        temperature=0.4,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    answer = str(response['choices'][0]['text'])

    return answer