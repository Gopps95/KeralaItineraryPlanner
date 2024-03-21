from flask import Flask, request, jsonify
from hugchat import hugchat
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

chatbot = hugchat.ChatBot(cookie_path="cookies.json")
conversation_id = chatbot.new_conversation()
chatbot.change_conversation(conversation_id)

@app.route('/api/chatbot', methods=['POST', 'GET'])
def chat():
    if request.method == 'GET':
        return 'Chatbot API is up and running.'

    if request.method == 'POST':
        data = request.get_json()
        user_input = data.get('message')

        if user_input.lower() == 'q' or user_input.lower() == 'quit':
            return jsonify({'response': 'Goodbye!'})

        elif user_input.lower() == 'c' or user_input.lower() == 'change':
            conversation_list = chatbot.get_conversation_list()
            return jsonify({'response': 'Choose a conversation to switch to:', 'conversations': conversation_list})

        elif user_input.lower() == 'n' or user_input.lower() == 'new':
            global conversation_id
            conversation_id = chatbot.new_conversation()
            chatbot.change_conversation(conversation_id)
            return jsonify({'response': 'Clean slate!'})

        else:
            chatbot_response = chatbot.chat(user_input)
            return jsonify({'response': str(chatbot_response)})


    return jsonify({'error': 'Invalid request method'}), 405

if __name__ == '__main__':
    app.run(debug=True)