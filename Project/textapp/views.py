
from django.shortcuts import render
from django.conf import settings
from .forms import TextForm
import os
from langchain.document_loaders import TextLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_cohere import CohereEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.llms import Cohere
from langchain_core.documents import Document
from django.http import HttpResponse



def make_vecorstore(request):
        pdf_path = os.path.join(settings.BASE_DIR, 'textapp', 'datasets', 'Riaz.pdf') 
        pdf_files = [pdf_path]
        all_docs = []
        for pdf in pdf_files:
            loader = PyPDFLoader(pdf)
            docs = loader.load()
            all_docs.extend(docs) 

        print("Document loaded . . .")

        # Step 2: Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        split_docs = text_splitter.split_documents(all_docs)


        print("Document splitted into chunks. . . ")


        # Step 3: define embedding model
        load_dotenv()
        cohere_api_key = os.getenv("secret_key")

        embedding_model = CohereEmbeddings(
            model="embed-multilingual-v3.0",
            cohere_api_key=cohere_api_key  
        )

        print("Embedding Model Loaded . . . .")


        # Step 4: Create vector store
        vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding= embedding_model,
            persist_directory="chroma_db"
            )

        print("Vectore Store Created")
        print(type(vectorstore))

        # step 5:  Save the vector store for reuse
        vectorstore.persist()

        print("Vector Store Saved Locally")
        return render(request, 'textapp/query.html', { 'message': "Vector Store Created Successfully"})




def make_query(request):
        # Load environment and API key
        load_dotenv()
        cohere_api_key = os.getenv("cohere_api_key")

        # Re-initialize the same embedding model used when vector store was created
        embedding_model = CohereEmbeddings(
            model="embed-multilingual-v3.0",
            cohere_api_key=cohere_api_key
        )

        # Load the persisted Chroma vector store
        vectorstore = Chroma(
            persist_directory="chroma_db",
            embedding_function=embedding_model
        )


        print("Vectored Store Loaded Successfully!")

        #load LLM

        llm = Cohere(
            model="command-r-plus",  # Best for multilingual and complex queries
            cohere_api_key=cohere_api_key,
            temperature=0.3,
            max_tokens=300,
        )

        print("LLM Loaded successfully!")

        #Make retriever
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type="stuff"  # You can also try "map_reduce" or "refine"
        )


        print("Retriever has be made successfully!")


        # Perform similarity search
        query = "Who is Poltu?"

        response = qa_chain(query)

        print("Making Query. . . . . . ")

        print("Answer:", response['result'])
        return render(request, 'textapp/query.html', { 'message': response['result']})





def add_new(request):
    message = ''
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data['filename']
            content = form.cleaned_data['content']
            # Ensure it ends with .txt
            if not filename.endswith('.txt'):
                filename += '.txt'
            file_path = os.path.join(settings.TEXT_FILE_SAVE_PATH, filename)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            message = f"File '{filename}' saved successfully!"
    else:
        form = TextForm()
    return render(request, 'textapp/form.html', {'form': form, 'message': message})


def add_new_doc(request):
    message=''
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            filename = form.cleaned_data['filename']
            content = form.cleaned_data['content']
            
            
            doc = Document(page_content=content)
            print("document loaded")
            # Load .env and API key
            load_dotenv()
            cohere_api_key = os.getenv("cohere_api_key")

            # Reinitialize the embedding model
            embedding_model = CohereEmbeddings(
                model="embed-multilingual-v3.0",
                cohere_api_key=cohere_api_key
            )
            print("Embedding Model Loaded")

            # Load existing vector store
            vectorstore = Chroma(
                persist_directory="chroma_db",
                embedding_function=embedding_model
            )
            print("vector store loaded ..")

            # Split the document into chunks
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
            split_new_docs = text_splitter.split_documents([doc])

            # Add new documents to the store
            vectorstore.add_documents(split_new_docs)

            # Save changes to disk
            vectorstore.persist()
            message = f"File '{filename}' saved successfully!"

            print("New Document added successfully!")


    else:
        form = TextForm()
    return render(request, 'textapp/form.html', {'form': form, 'message': message})


def ask(query):
        # Load environment and API key
        load_dotenv()
        cohere_api_key = os.getenv("cohere_api_key")

        # Re-initialize the same embedding model used when vector store was created
        embedding_model = CohereEmbeddings(
            model="embed-multilingual-v3.0",
            cohere_api_key=cohere_api_key
        )

        # Load the persisted Chroma vector store
        vectorstore = Chroma(
            persist_directory="chroma_db",
            embedding_function=embedding_model
        )


        print("Vectored Store Loaded Successfully!")

        #load LLM

        llm = Cohere(
            model="command-r-plus",  # Best for multilingual and complex queries
            cohere_api_key=cohere_api_key,
            temperature=0.3,
            max_tokens=300,
        )

        print("LLM Loaded successfully!")

        #Make retriever
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
            return_source_documents=True,
            chain_type="stuff"  # You can also try "map_reduce" or "refine"
        )


        print("Retriever has be made successfully!")

        response = qa_chain(query)

        return response


def getQuery(request):
    name = ''
    llm_response=''
    submitted = False

    if request.method == 'POST':
        name = request.POST.get('name', '')
        submitted = True
        llm_response=ask(name)
        llm_response=llm_response['result']

    return render(request, 'textapp/getQuery.html', {
        'name': name,
        'submitted': submitted,
        'response':llm_response
    })

