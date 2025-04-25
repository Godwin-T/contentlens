import React, { useState } from 'react';
import { Search } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';
import Button from '../ui/Button';

const Hero: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/articles?search=${encodeURIComponent(searchQuery)}`);
    }
  };

  return (
    <div className="relative bg-gray-50 dark:bg-gray-900 overflow-hidden">
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-50 to-purple-50 dark:from-indigo-950/30 dark:to-purple-950/30 opacity-80" />
        <div className="absolute inset-0 bg-[url('https://images.pexels.com/photos/4050356/pexels-photo-4050356.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2')] bg-cover bg-center opacity-10 dark:opacity-5" />
      </div>
      
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="py-20 md:py-28 lg:py-32 max-w-4xl mx-auto text-center">
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-gray-900 dark:text-white mb-6 leading-tight">
            Discover <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-purple-600">Insights</span> with AI-Enhanced Reading
          </h1>
          
          <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 leading-relaxed">
            Content Lens transforms how you consume articles with AI search and chat features that make information discovery effortless.
          </p>
          
          <div className="flex justify-center mb-12">
            <Link to="/articles">
              <Button size="lg" variant="primary">
                Browse Articles
              </Button>
            </Link>
          </div>
          
          <div className="max-w-2xl mx-auto relative">
            <form onSubmit={handleSearch} className="relative">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search for articles, topics, or authors..."
                className="w-full pl-12 pr-4 py-4 rounded-full border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500 shadow-lg"
              />
              <Search className="absolute left-4 top-1/2 transform -translate-y-1/2 h-6 w-6 text-gray-400" />
            </form>
            <div className="absolute -bottom-3 left-0 right-0 text-center">
              <div className="inline-flex gap-2 text-sm text-gray-500 dark:text-gray-400 bg-white dark:bg-gray-800 px-4 py-1 rounded-full shadow">
                <span>Popular:</span>
                <Link to="/articles?tag=AI" className="text-indigo-600 dark:text-indigo-400 hover:underline">AI</Link>
                <Link to="/articles?tag=Technology" className="text-indigo-600 dark:text-indigo-400 hover:underline">Technology</Link>
                <Link to="/articles?tag=Psychology" className="text-indigo-600 dark:text-indigo-400 hover:underline">Psychology</Link>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="absolute bottom-0 left-0 right-0 h-16 bg-gradient-to-t from-gray-100 dark:from-gray-900 to-transparent" />
    </div>
  );
};

export default Hero;