import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import ArticleContent from '../components/article/ArticleContent';
import ArticleCard from '../components/article/ArticleCard';
import ChatBot from '../components/features/ChatBot';
import { getArticleById, articles } from '../data/articles';
import { Article } from '../types';

const ArticleDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const [article, setArticle] = useState<Article | null>(null);
  const [loading, setLoading] = useState(true);
  const [relatedArticles, setRelatedArticles] = useState<Article[]>([]);
  const navigate = useNavigate();
  
  useEffect(() => {
    if (!id) {
      navigate('/articles');
      return;
    }
    
    // Simulate loading delay
    setLoading(true);
    
    setTimeout(() => {
      const foundArticle = getArticleById(id);
      
      if (foundArticle) {
        setArticle(foundArticle);
        
        // Find related articles (articles with at least one matching tag)
        const related = articles
          .filter(a => 
            a.id !== id && 
            a.tags.some(tag => foundArticle.tags.includes(tag))
          )
          .slice(0, 2);
          
        setRelatedArticles(related);
      } else {
        navigate('/articles');
      }
      
      setLoading(false);
    }, 500);
  }, [id, navigate]);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-600"></div>
      </div>
    );
  }
  
  if (!article) {
    return null;
  }

  return (
    <div className="py-8">
      <ArticleContent article={article} />
      
      {relatedArticles.length > 0 && (
        <div className="max-w-3xl mx-auto px-4 sm:px-6 mt-16">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
            Related Articles
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {relatedArticles.map(related => (
              <ArticleCard key={related.id} article={related} />
            ))}
          </div>
        </div>
      )}
      
      <ChatBot articleId={article.id} />
    </div>
  );
};

export default ArticleDetailPage;