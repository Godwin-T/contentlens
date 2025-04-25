import React from 'react';
import { Bot, Search, BookOpen, Brain } from 'lucide-react';

const AIFeatures: React.FC = () => {
  return (
    <section className="py-20 bg-gray-50 dark:bg-gray-950">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <span className="text-indigo-600 dark:text-indigo-400 font-semibold text-sm uppercase tracking-wider">AI-Powered Experience</span>
          <h2 className="mt-2 text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white">
            Enhance Your Reading with Artificial Intelligence
          </h2>
          <p className="mt-4 text-xl text-gray-600 dark:text-gray-400">
            Our AI technologies transform how you discover and interact with content
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {/* Feature 1 */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-8 transition-transform hover:-translate-y-1 hover:shadow-lg">
            <div className="w-12 h-12 rounded-full bg-indigo-100 dark:bg-indigo-900/50 flex items-center justify-center mb-6">
              <Search className="h-6 w-6 text-indigo-600 dark:text-indigo-400" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
              AI-Powered Search
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Find exactly what you're looking for with our semantic search that understands context and meaning, not just keywords.
            </p>
          </div>
          
          {/* Feature 2 */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-8 transition-transform hover:-translate-y-1 hover:shadow-lg">
            <div className="w-12 h-12 rounded-full bg-purple-100 dark:bg-purple-900/50 flex items-center justify-center mb-6">
              <Bot className="h-6 w-6 text-purple-600 dark:text-purple-400" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
              Article Chat Assistant
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Too busy to read the whole article? Chat with our AI to quickly extract key information and insights from any content.
            </p>
          </div>
          
          {/* Feature 3 */}
          <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-8 transition-transform hover:-translate-y-1 hover:shadow-lg">
            <div className="w-12 h-12 rounded-full bg-blue-100 dark:bg-blue-900/50 flex items-center justify-center mb-6">
              <Brain className="h-6 w-6 text-blue-600 dark:text-blue-400" />
            </div>
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
              Personalized Recommendations
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              Discover content tailored to your interests and reading behavior with our adaptive recommendation engine.
            </p>
          </div>
        </div>
        
        <div className="mt-20 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl overflow-hidden shadow-xl">
          <div className="grid grid-cols-1 lg:grid-cols-5">
            <div className="p-8 lg:p-12 lg:col-span-3">
              <h3 className="text-2xl sm:text-3xl font-bold text-white mb-4">
                Experience Content Like Never Before
              </h3>
              <p className="text-indigo-100 text-lg mb-8">
                Our AI assistant can answer questions, summarize content, and help you extract exactly what you need from any article.
              </p>
              <button className="bg-white text-indigo-600 hover:bg-indigo-50 px-6 py-3 rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-indigo-600">
                Try the AI Assistant
              </button>
            </div>
            <div className="lg:col-span-2 bg-indigo-800 p-4 flex items-center justify-center">
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-4 w-full max-w-sm">
                <div className="flex items-center border-b border-gray-200 dark:border-gray-700 pb-4 mb-4">
                  <BookOpen className="h-5 w-5 text-indigo-600 mr-2" />
                  <span className="font-medium">ChatLens AI</span>
                </div>
                <div className="space-y-4">
                  <div className="flex items-start">
                    <div className="bg-indigo-100 dark:bg-indigo-900/50 rounded-full p-2 mr-3">
                      <Bot className="h-4 w-4 text-indigo-600 dark:text-indigo-400" />
                    </div>
                    <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-3 text-sm text-gray-800 dark:text-gray-200 max-w-[80%]">
                      How can I help you with this article?
                    </div>
                  </div>
                  <div className="flex items-start justify-end">
                    <div className="bg-indigo-600 rounded-lg p-3 text-sm text-white max-w-[80%]">
                      What are the key points about sustainable architecture?
                    </div>
                  </div>
                  <div className="flex items-start">
                    <div className="bg-indigo-100 dark:bg-indigo-900/50 rounded-full p-2 mr-3">
                      <Bot className="h-4 w-4 text-indigo-600 dark:text-indigo-400" />
                    </div>
                    <div className="bg-gray-100 dark:bg-gray-700 rounded-lg p-3 text-sm text-gray-800 dark:text-gray-200 max-w-[80%]">
                      The key points about sustainable architecture include:
                      <br />1. Energy efficiency
                      <br />2. Resource conservation
                      <br />3. Use of renewable energy
                      <br />4. Integration with the environment
                    </div>
                  </div>
                </div>
                <div className="mt-4 flex">
                  <input
                    type="text"
                    placeholder="Ask about this article..."
                    className="flex-1 border border-gray-300 dark:border-gray-600 rounded-l-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 dark:bg-gray-700 dark:text-white"
                  />
                  <button className="bg-indigo-600 text-white px-3 py-2 rounded-r-lg">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14M12 5l7 7-7 7" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default AIFeatures;