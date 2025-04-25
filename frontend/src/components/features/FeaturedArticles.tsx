import React from 'react';
import { Article } from '../../types';
import ArticleCard from '../article/ArticleCard';
import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

interface FeaturedArticlesProps {
  articles: Article[];
}

const FeaturedArticles: React.FC<FeaturedArticlesProps> = ({ articles }) => {
  // Select the first article as the featured one
  const featuredArticle = articles[0];
  // Get remaining articles for the grid
  const remainingArticles = articles.slice(1);

  return (
    <section className="py-12 bg-white dark:bg-gray-900">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between mb-8">
          <h2 className="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
            Featured Articles
          </h2>
          <Link 
            to="/articles" 
            className="flex items-center text-indigo-600 dark:text-indigo-400 hover:text-indigo-800 dark:hover:text-indigo-300 font-medium transition-colors"
          >
            View all 
            <ArrowRight className="ml-1 h-4 w-4" />
          </Link>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Featured Article */}
          <div className="lg:col-span-7">
            <ArticleCard article={featuredArticle} variant="featured" />
          </div>
          
          {/* Remaining Articles Grid */}
          <div className="lg:col-span-5 grid grid-cols-1 gap-6">
            {remainingArticles.slice(0, 2).map(article => (
              <ArticleCard key={article.id} article={article} variant="compact" />
            ))}
          </div>
        </div>
      </div>
    </section>
  );
};

export default FeaturedArticles;