import React from 'react';
import { Link } from 'react-router-dom';
import { articles } from '../data/articles';
import ChatBot from '../components/features/ChatBot';

const TopicsPage: React.FC = () => {
  // Extract all unique tags from articles
  const allTags = Array.from(new Set(articles.flatMap(article => article.tags)));
  
  // Count articles for each tag
  const tagCounts = allTags.reduce<Record<string, number>>((acc, tag) => {
    acc[tag] = articles.filter(article => article.tags.includes(tag)).length;
    return acc;
  }, {});

  return (
    <div className="py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center mb-12">
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Explore Topics
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400">
            Browse articles by your favorite topics and interests
          </p>
        </div>
        
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {allTags.map(tag => (
            <Link 
              key={tag}
              to={`/articles?tag=${tag}`}
              className="block group"
            >
              <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div className="h-40 bg-gradient-to-r from-indigo-500 to-purple-600 flex items-center justify-center p-6">
                  <span className="text-2xl font-bold text-white">{tag}</span>
                </div>
                <div className="p-6">
                  <div className="flex items-center justify-between">
                    <span className="text-gray-600 dark:text-gray-400">
                      {tagCounts[tag]} {tagCounts[tag] === 1 ? 'Article' : 'Articles'}
                    </span>
                    <span className="text-indigo-600 dark:text-indigo-400 group-hover:underline font-medium">
                      View articles
                    </span>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
      
      <ChatBot />
    </div>
  );
};

export default TopicsPage;