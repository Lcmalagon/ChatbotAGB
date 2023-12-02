import streamlit as st
import openai, boto3
from PIL import Image
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from pathlib import Path

# Initializing textract API

textract = boto3.client('textract', region_name='us-east-1', aws_access_key_id='AKIASF2P7IDFKIGWFHIU',aws_secret_access_key='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')

# Creating
def document_to_retriever(document, chunk_size, chunk_overlap):
    with open(document, 'rb') as file:
        img = file.read()
        bytes = bytearray(img)

    extracted_text = textract.analyze_document(Document = {'Bytes': bytes}, FeatureTypes = ['TABLES'])


    text = []
    blocks = extracted_text['Blocks']

    for block in blocks:
        if block['BlockType'] == 'WORD':
             text.append(block['Text'])
    # text formation based upon Line block type
        elif block['BlockType'] == 'LINE':
             text.append(block['Text'])

    words = " ".join(text)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    splits = text_splitter.create_documents([words])
    print(splits)
    vectorstore = Chroma.from_documents(documents=splits,embedding=OpenAIEmbeddings(openai_api_key='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'))
    retriever = vectorstore.as_retriever()


    return retriever

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def generate_response(retriever, input_text):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(ChatOpenAI(model_name="gpt-4", temperature=0,
                                                          openai_api_key='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'),
                                               retriever=retriever, verbose=True, memory=st.session_state.memory)
    result = qa({"chat_history": chat_history, "question":input_text})
    return result['answer']

# Stream lit page configuration
st.set_page_config(page_title="PostGame Extract", page_icon=":tada:", layout="wide")
st.title("Our Project's aim is to make alleviate the hassle of manual transcription and hard to read, handwritten documents in the sports world")

left_column, right_column = st.columns(2)

#Creating file uploader using file.uploader function from streamlit. st.sidebar dictates location of uploader

file_upload = st.sidebar.file_uploader("Please Upload a File", type=['png','jpeg', 'jpg', 'pdf'])

# Initializing messages in the session state for call back to chat history during chat session
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# File upload conditional to limits code execution until after file has been uploaded. Code executed is display of
# image, but you may adjust as needed.
if file_upload is not None:
    with open(file_upload.name, mode='wb') as w:
        w.write(file_upload.getvalue())
    if '.pdf' not in file_upload.name:
        image = Image.open(file_upload.name)
        right_column.image(image, caption='menu',use_column_width=True)

# extracting text from uploaded file and formatting into a retriever for our LLM. file_upload.name used to reference
# file name in session's temp directory (confirming where the file is actually saved to as it does not come across to the local storage.

    retriever = document_to_retriever(file_upload.name, 100,2)


    chat_history = []

# Chat configuration and setup
    
    if prompt := st.chat_input("Ask me about the repository!"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            with st.spinner("Generating an answer..."):
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""
                    response = generate_response(retriever, prompt)
                    for response in response:
                        full_response += response
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": full_response}
                )

#if prompt := st.chat_input(placeholder="What would you like to know?"):
#   st.session_state.messages.append({"role": "user", "content": prompt})
#    st.chat_message("user").write(prompt)
#    response = generate_response(retriever, prompt)
#    msg = response
#    st.session_state.messages.append(msg)
#    st.chat_message("assistant").write(msg)



#with st.chat_message("assistant"):
#    response = generate_response(retriever,st.session_state.messages)
#    st.session_state.messages.append({"role": "assistant", "content": response})
#    st.write(response)

#with st.chat_message('my_form'):
#    text = st.text_area('Enter text:', 'What are the three key pieces of advice for learning how to code?')

#    if submitted:
#        generate_response(retriever,text)


