function sendMessage() {
    var userInput = document.getElementById('search-box').value;

    // Display user message in the chat
    displayMessage('user', userInput);

    // Send user message to the backend
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 'message': userInput }),
    })
    .then(response => response.json())
    .then(data => {
        // Display chatbot response in the chat
        displayMessage('bot', data.botResponse);
    })
    .catch(error => console.error('Error:', error));

    // Clear the input field
    document.getElementById('search-box').value = '';
}