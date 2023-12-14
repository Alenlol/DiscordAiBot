import google.generativeai as palm
from google.generativeai.types import safety_types


palm.configure(api_key='AIzaSyC1BDog70NAY6Eeu0yT-8Ko357zq7uCf7E')

default = [
            {
                "category": safety_types.HarmCategory.HARM_CATEGORY_UNSPECIFIED,
                "threshold": safety_types.HarmBlockThreshold.BLOCK_NONE
            },
            {
                "category": safety_types.HarmCategory.HARM_CATEGORY_DEROGATORY,
                "threshold": safety_types.HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": safety_types.HarmCategory.HARM_CATEGORY_TOXICITY,
                "threshold": safety_types.HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": safety_types.HarmCategory.HARM_CATEGORY_VIOLENCE,
                "threshold": safety_types.HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": safety_types.HarmCategory.HARM_CATEGORY_SEXUAL,
                "threshold": safety_types.HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": safety_types.HarmCategory.HARM_CATEGORY_MEDICAL,
                "threshold": safety_types.HarmBlockThreshold.BLOCK_NONE,
            },
            {
                "category": safety_types.HarmCategory.HARM_CATEGORY_DANGEROUS,
                "threshold": safety_types.HarmBlockThreshold.BLOCK_NONE,
            }
        ]


def aiGenerateText(text, cntWords = "", candidatesCount = 3):
    if cntWords:
        cntWords = f". No more than {cntWords} words and without author's name"


    #response = palm.chat(context="Speak like Thomas Shelby" + cntWords, temperature= 1, messages=text)
    response = palm.generate_text(
        prompt=text+cntWords,
        candidate_count=1,
        temperature=1,
        safety_settings=default
    )
    #print(response.candidates[0], response.candidates[1], response.candidates[2])
    textResponse = sorted([output['output'] for output in response.candidates], key=len)
    print(textResponse)

    return textResponse[-1]

def aiMessageChat(text):
    chatResponse = palm.chat(context="Speak like Thomas Shelby", messages=text, temperature=1)

    return chatResponse.last


if __name__ == '__main__':
    print(aiGenerateText("Hello"))
