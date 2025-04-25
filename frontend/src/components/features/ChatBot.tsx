import React, { useState } from 'react';
import { Bot, X, Maximize, Minimize, ArrowRight } from 'lucide-react';
import { ChatMessage } from '../../types';

interface ChatBotProps {
  articleId?: string;
}

const ChatBot: React.FC<ChatBotProps> = ({ articleId }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [message, setMessage] = useState('');
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      content: articleId 
        ? "Hi there! I can answer questions about this article. What would you like to know?"
        : "Hello! I'm your ContentLens AI assistant. How can I help you today?",
      sender: 'bot',
      timestamp: new Date().toISOString()
    }
  ]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;
    
    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      content: message,
      sender: 'user',
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setMessage('');
    
    // Simulate bot response
    setTimeout(() => {
      const botResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        content: generateBotResponse(message, articleId),
        sender: 'bot',
        timestamp: new Date().toISOString()
      };
      
      setMessages(prev => [...prev, botResponse]);
    }, 1000);
  };
  
  const generateBotResponse = (userMessage: string, articleId?: string): string => {
    const userMessageLower = userMessage.toLowerCase();
    
    // For demo purposes only - in a real app this would connect to an actual AI service
    if (articleId) {
      if (userMessageLower.includes('summary') || userMessageLower.includes('summarize')) {
        return "This article discusses the key aspects of the topic, including important concepts, practical applications, and future implications. It provides a comprehensive overview with supporting examples and expert opinions.";
      } else if (userMessageLower.includes('key point') || userMessageLower.includes('main idea')) {
        return "The main points of this article are:\n1. Introduction to the core concept\n2. Historical context and development\n3. Current applications and significance\n4. Future trends and potential impact\n5. Expert opinions and analysis";
      } else if (userMessageLower.includes('author')) {
        return "The author is an expert in this field with extensive experience and credentials. They've published multiple works on related topics and are recognized for their contributions to this area of study.";
      }
    }
    
    if (userMessageLower.includes('hello') || userMessageLower.includes('hi')) {
      return "Hello there! How can I assist you today?";
    } else if (userMessageLower.includes('help')) {
      return "I can help you with:\n- Summarizing articles\n- Answering questions about content\n- Finding related topics\n- Explaining complex concepts\n\nJust let me know what you need!";
    } else if (userMessageLower.includes('thank')) {
      return "You're welcome! Is there anything else I can help you with?";
    }
    
    return "I'm happy to help! Could you provide more details about what you're looking for?";
  };
  
  const toggleChat = () => {
    if (isMinimized) {
      setIsMinimized(false);
    } else {
      setIsOpen(!isOpen);
    }
  };
  
  const minimizeChat = (e: React.MouseEvent) => {
    e.stopPropagation();
    setIsMinimized(true);
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Chat Button */}
      <button
        onClick={toggleChat}
        className={`${
          isOpen && !isMinimized ? 'hidden' : 'flex'
        } items-center justify-center w-14 h-14 rounded-full bg-indigo-600 text-white shadow-lg hover:bg-indigo-700 transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500`}
        aria-label="Open chat"
      >
        <Bot className="h-6 w-6" />
      </button>
      
      {/* Chat Window */}
      <div
        className={`${
          isOpen ? 'flex' : 'hidden'
        } ${
          isMinimized ? 'h-14 w-64' : 'h-96 w-80 sm:w-96'
        } flex-col bg-white dark:bg-gray-800 rounded-lg shadow-xl transition-all duration-300 overflow-hidden`}
      >
        {/* Chat Header */}
        <div className="bg-indigo-600 text-white p-4 flex items-center justify-between">
          <div className="flex items-center">
            <Bot className="h-5 w-5 mr-2" />
            <h3 className="font-medium">
              {articleId ? 'Article Assistant' : 'Content Lens AI'}
            </h3>
          </div>
          <div className="flex items-center space-x-2">
            {isMinimized ? (
              <button
                onClick={() => setIsMinimized(false)}
                className="text-white hover:text-indigo-100"
                aria-label="Maximize"
              >
                <Maximize className="h-4 w-4" />
              </button>
            ) : (
              <button
                onClick={minimizeChat}
                className="text-white hover:text-indigo-100"
                aria-label="Minimize"
              >
                <Minimize className="h-4 w-4" />
              </button>
            )}
            <button
              onClick={() => setIsOpen(false)}
              className="text-white hover:text-indigo-100"
              aria-label="Close"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
        </div>
        
        {!isMinimized && (
          <>
            {/* Chat Messages */}
            <div className="flex-1 p-4 overflow-y-auto">
              <div className="space-y-4">
                {messages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg p-3 ${
                        msg.sender === 'user'
                          ? 'bg-indigo-600 text-white'
                          : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{msg.content}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Chat Input */}
            <form onSubmit={handleSubmit} className="border-t border-gray-200 dark:border-gray-700 p-4">
              <div className="flex items-center">
                <input
                  type="text"
                  value={message}
                  onChange={(e) => setMessage(e.target.value)}
                  placeholder="Type your message..."
                  className="flex-1 border border-gray-300 dark:border-gray-600 rounded-l-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
                />
                <button
                  type="submit"
                  className="bg-indigo-600 text-white px-3 py-2 rounded-r-lg hover:bg-indigo-700 transition-colors"
                >
                  <ArrowRight className="h-5 w-5" />
                </button>
              </div>
            </form>
          </>
        )}
      </div>
    </div>
  );
};

export default ChatBot;