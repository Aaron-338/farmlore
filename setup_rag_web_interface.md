# Setting Up the RAG-Enhanced Web Interface

This guide explains how to connect the FarmLore web interface to use the RAG (Retrieval-Augmented Generation) system we've implemented.

## Overview

We've created three key components:
1. `standalone_rag.py` - Our core RAG implementation that enhances responses with agricultural pest information
2. `rag_web_connector.py` - A Flask server that acts as a bridge between the web UI and our RAG system
3. `rag_chat.html` - A modified version of the chat.html template that connects to the RAG connector

## Setup Instructions

### Step 1: Set up the Flask RAG Connector

1. Make sure you have the necessary dependencies:
   ```bash
   pip install flask requests
   ```

2. Start the RAG connector server (use a separate terminal window):
   ```bash
   python rag_web_connector.py
   ```
   This will start the connector server on port 5000 by default.

### Step 2: Copy the RAG Chat Template

Copy the RAG-enhanced chat template to the Django templates directory:

```bash
cp rag_chat.html pest-management-chatbot/farmlore-project/chatbot/templates/chatbot/rag_chat.html
```

### Step 3: Create a Django View for the RAG Chat

Create a new view in your Django project that uses the rag_chat.html template:

1. Open `pest-management-chatbot/farmlore-project/chatbot/views.py`
2. Add the following code:

```python
def rag_chat_view(request):
    """
    View for the RAG-enhanced chat interface
    """
    return render(request, 'chatbot/rag_chat.html')
```

### Step 4: Add URL Route for the RAG Chat

Add a URL route for the RAG chat interface:

1. Open `pest-management-chatbot/farmlore-project/chatbot/urls.py`
2. Add the following import (if not already present):
   ```python
   from chatbot import views
   ```
3. Add the following URL pattern:
   ```python
   path('rag-chat/', views.rag_chat_view, name='rag_chat'),
   ```

### Step 5: Test the RAG-Enhanced Chat Interface

1. Make sure the Django server is running:
   ```bash
   cd pest-management-chatbot/farmlore-project
   python manage.py runserver
   ```

2. Make sure the RAG connector is running:
   ```bash
   python rag_web_connector.py
   ```

3. Navigate to http://localhost:8000/chatbot/rag-chat/ in your browser

4. Test the interface with pest-related questions, such as:
   - What pests affect cucumber plants?
   - How do I control aphids on my tomato plants?
   - What's the best way to deal with spider mites in my garden?

## Troubleshooting

If you encounter issues with the RAG-enhanced chat:

1. Check that the RAG connector server is running and accessible
   ```bash
   curl http://localhost:5000/rag-enhance -d '{"query":"test","response":"test"}' -H "Content-Type: application/json"
   ```

2. Verify the main API is working
   ```bash
   curl http://localhost:80/api/chat/ -d '{"message":"hello"}' -H "Content-Type: application/json"
   ```

3. Check the browser console for JavaScript errors

4. Ensure the RAG_PROXY_URL in rag_chat.html points to your RAG connector server

## Adding More Pest Information

To improve the RAG system's knowledge base, add more pest information to the PEST_DATA array in standalone_rag.py. For example:

```python
PEST_DATA = [
    # ... existing entries ...
    {
        "title": "Cucumber Beetle Management",
        "content": """
Cucumber beetles (both spotted and striped varieties) are common pests of cucumber plants. They feed on leaves, stems, and fruits, and can transmit bacterial wilt disease.

Effective control methods include:

1. Row covers: Use floating row covers until flowering to prevent beetles from reaching plants.
2. Yellow sticky traps: Deploy around plants to catch adult beetles.
3. Diatomaceous earth: Apply around the base of plants to control beetle populations.
4. Beneficial nematodes: Apply to soil to control larval stages.
5. Crop rotation: Avoid planting cucurbits in the same location in consecutive years.
"""
    }
] 