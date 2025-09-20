import os, openai
def init_openai_from_env_or_error():
    key = os.environ.get('OPENAI_API_KEY')
    if not key:
        raise RuntimeError('OPENAI_API_KEY not set in environment. Provide via GUI or env var.')
    openai.api_key = key

def generate_script(topic: str, language: str = 'Hindi', tone: str = 'informative'):
    init_openai_from_env_or_error()
    prompt = f"""You are a helpful assistant that writes short YouTube scripts in {language}. Create hook, 3 points and CTA for: {topic}"""
    resp = openai.ChatCompletion.create(
        model='gpt-4o-mini',
        messages=[{'role':'system','content':'You are a scriptwriter.'},{'role':'user','content':prompt}],
        temperature=0.7,
        max_tokens=700
    )
    return resp['choices'][0]['message']['content'].strip()
