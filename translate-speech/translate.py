import boto3


# translation
translate = boto3.client(service_name='translate')

with open('test.txt', encoding='utf-8') as f:
    text = f.read()

result = translate.translate_text(Text=text, 
            SourceLanguageCode="ja", TargetLanguageCode="en")
translated = result.get('TranslatedText')
print('TranslatedText: ' + translated)
print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))


# text to speech
polly = boto3.client(service_name='polly')

response = polly.synthesize_speech(
    VoiceId='Ivy',
    OutputFormat='mp3',
    Text=translated
)

with open('speech.mp3', 'wb') as f2:
    f2.write(response['AudioStream'].read())
