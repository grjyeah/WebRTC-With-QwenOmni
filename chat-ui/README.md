# Real-time Chat UI

A responsive, real-time chat interface that displays conversation history between a user and chatbot.

## Features

- Real-time message display
- Distinct styling for user and bot messages
- Automatic scrolling to the latest message
- Responsive design for all screen sizes
- Send messages by button click or Enter key

## Files

- `index.html` - Main HTML structure
- `styles.css` - Styling for the chat interface
- `script.js` - JavaScript functionality for real-time updates
- `server.js` - Simple Node.js server to serve the files

## How to Run

1. Make sure you have Node.js installed on your system
2. Navigate to the chat-ui directory in your terminal
3. Run the server with:
   ```
   npm start
   ```
4. Open your browser and go to `http://localhost:3000`

## How It Works

1. Messages are displayed in a scrollable container with distinct styling for user (blue) and bot (green) messages
2. Each message shows the sender's identity on the left and content on the right
3. The interface automatically scrolls to the newest message
4. Users can send messages by typing and clicking Send or pressing Enter
5. The bot responds with simulated responses after a short delay

## Customization

You can customize the styling by modifying `styles.css`:
- Colors: Adjust the background colors and text colors
- Spacing: Modify padding and margins
- Borders: Change border-radius for different message shapes
- Responsiveness: Adjust media queries for different screen sizes

To modify the bot's responses, edit the `getBotResponse()` function in `script.js`.