import React from 'react';
import ReactMarkdown from 'react-markdown';
import { Article } from '../../types';
import { Clock, Calendar, Tag, Share2, Bookmark } from 'lucide-react';

interface ArticleContentProps {
  article: Article;
}

const ArticleContent: React.FC<ArticleContentProps> = ({ article }) => {
  const { title, content, author, coverImage, publishedDate, readingTime, tags } = article;
  
  const date = new Date(publishedDate).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 py-8">
      <div className="mb-8">
        <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white mb-4">
          {title}
        </h1>
        
        <div className="flex items-center space-x-4 mb-6">
          <div className="flex items-center">
            <img
              src={author.avatar}
              alt={author.name}
              className="w-10 h-10 rounded-full mr-3"
            />
            <div>
              <p className="font-medium text-gray-900 dark:text-white">{author.name}</p>
              <p className="text-sm text-gray-500 dark:text-gray-400">{author.bio}</p>
            </div>
          </div>
        </div>
        
        <div className="flex flex-wrap items-center text-sm text-gray-500 dark:text-gray-400 mb-6 gap-4">
          <div className="flex items-center">
            <Calendar className="h-4 w-4 mr-1" />
            <span>{date}</span>
          </div>
          <div className="flex items-center">
            <Clock className="h-4 w-4 mr-1" />
            <span>{readingTime} min read</span>
          </div>
          <div className="flex items-center flex-wrap gap-2">
            {tags.map(tag => (
              <span 
                key={tag} 
                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800 dark:bg-indigo-900 dark:text-indigo-200"
              >
                <Tag className="h-3 w-3 mr-1" />
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>
      
      <div className="relative rounded-xl overflow-hidden mb-8 h-72 sm:h-96 lg:h-[500px]">
        <img
          src={coverImage}
          alt={title}
          className="w-full h-full object-cover"
        />
      </div>
      
      <div className="flex justify-between items-center mb-8 sticky top-20 z-10 bg-white dark:bg-gray-900 p-3 rounded-lg shadow-sm">
        <div className="flex space-x-2">
          <button className="inline-flex items-center p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
            <Share2 className="h-5 w-5 text-gray-600 dark:text-gray-300" />
          </button>
          <button className="inline-flex items-center p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
            <Bookmark className="h-5 w-5 text-gray-600 dark:text-gray-300" />
          </button>
        </div>
        <button className="text-sm text-white bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2">
          Ask AI Assistant
        </button>
      </div>
      
      <div className="prose dark:prose-invert prose-indigo max-w-none">
        <ReactMarkdown>
          {content}
        </ReactMarkdown>
      </div>
      
      <div className="mt-12 pt-8 border-t border-gray-200 dark:border-gray-800">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-4">About the author</h2>
        <div className="flex items-start space-x-4">
          <img
            src={author.avatar}
            alt={author.name}
            className="w-16 h-16 rounded-full"
          />
          <div>
            <p className="font-medium text-gray-900 dark:text-white mb-1">{author.name}</p>
            <p className="text-gray-600 dark:text-gray-400 mb-4">{author.bio}</p>
            <button className="text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 font-medium transition-colors">
              View all articles
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArticleContent;