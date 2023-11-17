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
        # Add streamlit and pandas to the list of required packages
        'streamlit',
        'pandas',
        # If you are using any other specific libraries, add them here as well
    ],
)
