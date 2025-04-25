import React, { useState } from 'react';
import { Article } from '../../types';
import ArticleCard from './ArticleCard';
import { Search, Filter, ArrowUpDown } from 'lucide-react';

interface ArticleListProps {
  articles: Article[];
  title?: string;
  showFilters?: boolean;
}

const ArticleList: React.FC<ArticleListProps> = ({ 
  articles, 
  title = 'Latest Articles',
  showFilters = true 
}) => {
  const [searchQuery, setSearchQuery] = useState('');
  const [sortBy, setSortBy] = useState<'newest' | 'oldest' | 'readingTime'>('newest');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  
  // Extract all unique tags from articles
  const allTags = Array.from(new Set(articles.flatMap(article => article.tags)));
  
  // Filter articles based on search query and selected tags
  let filteredArticles = articles.filter(article => {
    const matchesSearch = searchQuery === '' || 
      article.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      article.excerpt.toLowerCase().includes(searchQuery.toLowerCase());
      
    const matchesTags = selectedTags.length === 0 || 
      selectedTags.some(tag => article.tags.includes(tag));
      
    return matchesSearch && matchesTags;
  });
  
  // Sort filtered articles
  filteredArticles = [...filteredArticles].sort((a, b) => {
    if (sortBy === 'newest') {
      return new Date(b.publishedDate).getTime() - new Date(a.publishedDate).getTime();
    } else if (sortBy === 'oldest') {
      return new Date(a.publishedDate).getTime() - new Date(b.publishedDate).getTime();
    } else if (sortBy === 'readingTime') {
      return a.readingTime - b.readingTime;
    }
    return 0;
  });
  
  const toggleTag = (tag: string) => {
    setSelectedTags(prev => 
      prev.includes(tag) 
        ? prev.filter(t => t !== tag) 
        : [...prev, tag]
    );
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between mb-8">
        <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white mb-4 sm:mb-0">
          {title}
        </h2>
        
        {showFilters && (
          <div className="flex space-x-2">
            <div className="relative">
              <input
                type="text"
                placeholder="Search articles..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 pr-4 py-2 rounded-md border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
            </div>
            
            <div className="relative inline-block">
              <button 
                className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <Filter className="h-4 w-4 mr-2" />
                Filter
              </button>
            </div>
            
            <div className="relative inline-block">
              <button 
                className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md bg-white dark:bg-gray-800 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                onClick={() => setSortBy(sortBy === 'newest' ? 'oldest' : 'newest')}
              >
                <ArrowUpDown className="h-4 w-4 mr-2" />
                {sortBy === 'newest' ? 'Newest' : sortBy === 'oldest' ? 'Oldest' : 'Reading Time'}
              </button>
            </div>
          </div>
        )}
      </div>
      
      {showFilters && (
        <div className="mb-8 flex flex-wrap gap-2">
          {allTags.map(tag => (
            <button
              key={tag}
              onClick={() => toggleTag(tag)}
              className={`px-3 py-1 rounded-full text-sm font-medium transition-colors ${
                selectedTags.includes(tag)
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-700'
              }`}
            >
              {tag}
            </button>
          ))}
        </div>
      )}
      
      {filteredArticles.length === 0 ? (
        <div className="text-center py-12">
          <p className="text-gray-500 dark:text-gray-400 text-lg">
            No articles found. Try adjusting your search or filters.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredArticles.map(article => (
            <ArticleCard key={article.id} article={article} />
          ))}
        </div>
      )}
    </div>
  );
};

export default ArticleList;