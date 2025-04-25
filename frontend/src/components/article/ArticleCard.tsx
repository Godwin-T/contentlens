import React from 'react';
import { Link } from 'react-router-dom';
import { Article } from '../../types';
import { Clock, Tag } from 'lucide-react';

interface ArticleCardProps {
  article: Article;
  variant?: 'default' | 'featured' | 'compact';
}

const ArticleCard: React.FC<ArticleCardProps> = ({ article, variant = 'default' }) => {
  const { id, title, excerpt, author, coverImage, publishedDate, readingTime, tags } = article;
  
  const date = new Date(publishedDate).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });
  
  if (variant === 'featured') {
    return (
      <Link 
        to={`/article/${id}`}
        className="group block overflow-hidden rounded-2xl shadow-lg transition transform hover:-translate-y-1 hover:shadow-xl bg-white dark:bg-gray-800"
      >
        <div className="relative h-80 overflow-hidden">
          <img
            src={coverImage}
            alt={title}
            className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          />
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent" />
          <div className="absolute bottom-0 left-0 right-0 p-6 text-white">
            <div className="flex items-center space-x-2 mb-3">
              <img
                src={author.avatar}
                alt={author.name}
                className="w-8 h-8 rounded-full border-2 border-white"
              />
              <span className="text-sm font-medium">{author.name}</span>
            </div>
            <h2 className="text-2xl sm:text-3xl font-bold mb-2 line-clamp-2">{title}</h2>
            <p className="line-clamp-2 text-gray-200 mb-3">{excerpt}</p>
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2 text-sm">
                <span>{date}</span>
                <span>•</span>
                <div className="flex items-center">
                  <Clock className="h-4 w-4 mr-1" />
                  <span>{readingTime} min read</span>
                </div>
              </div>
              {tags.length > 0 && (
                <span className="bg-indigo-600 text-white text-xs px-2 py-1 rounded-full">
                  {tags[0]}
                </span>
              )}
            </div>
          </div>
        </div>
      </Link>
    );
  }
  
  if (variant === 'compact') {
    return (
      <Link 
        to={`/article/${id}`}
        className="flex items-center gap-4 p-4 rounded-lg transition hover:bg-gray-100 dark:hover:bg-gray-800"
      >
        <img
          src={coverImage}
          alt={title}
          className="w-16 h-16 rounded-md object-cover flex-shrink-0"
        />
        <div className="flex-1 min-w-0">
          <h3 className="font-medium text-gray-900 dark:text-gray-100 line-clamp-1">{title}</h3>
          <div className="flex items-center text-xs text-gray-500 dark:text-gray-400 mt-1">
            <span>{date}</span>
            <span className="mx-2">•</span>
            <Clock className="h-3 w-3 mr-1" />
            <span>{readingTime} min</span>
          </div>
        </div>
      </Link>
    );
  }
  
  // Default variant
  return (
    <Link 
      to={`/article/${id}`}
      className="group block overflow-hidden rounded-xl shadow transition transform hover:-translate-y-1 hover:shadow-md bg-white dark:bg-gray-800"
    >
      <div className="relative h-48 overflow-hidden">
        <img
          src={coverImage}
          alt={title}
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
        />
      </div>
      <div className="p-5">
        <div className="flex items-center space-x-2 mb-3">
          <img
            src={author.avatar}
            alt={author.name}
            className="w-6 h-6 rounded-full"
          />
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">{author.name}</span>
        </div>
        <h3 className="text-xl font-bold mb-2 text-gray-900 dark:text-white line-clamp-2">{title}</h3>
        <p className="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">{excerpt}</p>
        <div className="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
          <div className="flex items-center">
            <Clock className="h-4 w-4 mr-1" />
            <span>{readingTime} min read</span>
          </div>
          <div className="flex items-center space-x-2">
            {tags.slice(0, 1).map(tag => (
              <span 
                key={tag} 
                className="flex items-center text-indigo-600 dark:text-indigo-400"
              >
                <Tag className="h-3 w-3 mr-1" />
                {tag}
              </span>
            ))}
          </div>
        </div>
      </div>
    </Link>
  );
};

export default ArticleCard;