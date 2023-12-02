from setuptools import setup, find_packages

setup(
    name='chatagb',
    version='1.0',
    description='Chatbot that can answer questions from alumni CSV',
    author='lcmalagon',
    author_email='lcm12@stmarys-ca.edu',
    packages=find_packages(),
    install_requires=[
        'langchain',
        'openai',
        'chromadb',
        'kaleido',
        'python-multipart',
        'tiktoken',
        'sqlalchemy',
        'streamlit',
        'pandas',
        'gpt4all',
    
    ],
)
