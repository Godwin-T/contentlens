import React from 'react';
import ArticleList from '../components/article/ArticleList';
import ChatBot from '../components/features/ChatBot';
import { articles } from '../data/articles';

const ArticlesPage: React.FC = () => {
  return (
    <div className="py-12">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="max-w-4xl mx-auto text-center mb-12">
          <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            Explore Our Articles
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-400">
            Discover insightful content on a variety of topics
          </p>
        </div>
      </div>
      
      <ArticleList 
        articles={articles} 
        title="All Articles"
        showFilters={true}
      />
      
      <ChatBot />
    </div>
  );
};

export default ArticlesPage;