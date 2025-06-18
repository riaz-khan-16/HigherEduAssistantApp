
# HigherEduAssistantApp

**HigherEduAssistantApp** is an LLM-powered web application built to help individuals seeking higher education information — especially those applying to universities in the United States. 

It uses real-world experiences shared in the Facebook group [Nextop USA](https://www.facebook.com/groups/nextopusa), where users discuss their application journeys for MS and PhD programs. These posts are converted into a searchable vector database and combined with a large language model to allow users to ask questions and receive relevant, experience-based answers.

---

## Features

- Ask questions in natural language about higher education in the US.
- Retrieves real-life experiences from a vector database built on Facebook group posts.
- Generates intelligent responses using a powerful LLM.
- Simple and clean web interface powered by Django.

---

![image](https://github.com/user-attachments/assets/175e8f42-98c5-4f59-b0fd-45e142026b94)

![image](https://github.com/user-attachments/assets/db0e201a-2cb6-493b-af36-dac084e013c0)

## Technologies Used

- **Vector DB**: [ChromaDB](https://www.trychroma.com/)
- **Large Language Model**: [Cohere](https://cohere.com/)
- **Backend Framework**: [Django](https://www.djangoproject.com/)
- **Framework for LLM Integration**: [LangChain](https://www.langchain.com/)

---

## ⚙️ How It Works

1. **Data Collection**: Posts are collected from the Nextop USA Facebook group.
2. **Preprocessing**: Text is cleaned and embedded using Cohere's embedding model.
3. **Vector Store**: Embeddings are stored in ChromaDB.
4. **User Interaction**: User submits a query through the frontend.
5. **Retrieval-Augmented Generation**: LangChain retrieves similar posts and feeds them to the Cohere LLM.
6. **Response Generation**: The model returns a relevant, informative answer.

---

## Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/HigherEduAssistantApp.git
cd HigherEduAssistantApp

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the dependencies
pip install -r requirements.txt

# Create a .env file and add your Cohere API key
COHERE_API_KEY=your-api-key-here

# Run the Django development server
python manage.py runserver


![image](https://github.com/user-attachments/assets/175e8f42-98c5-4f59-b0fd-45e142026b94)

![image](https://github.com/user-attachments/assets/db0e201a-2cb6-493b-af36-dac084e013c0)

