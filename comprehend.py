import boto3
import json

REGION='ap-northeast-1'

def detect_dominant_language(text,language_code):
    comprehend=boto3.client('comprehend',region_name=REGION)
    response= comprehend.detect_entities(Text=text,LanguageCode=language_code)
    return response

def main(_text):
    text=_text
    language_code='ja'
    result=detect_dominant_language(text,language_code)
    return result

if __name__=='__main__':
    main()