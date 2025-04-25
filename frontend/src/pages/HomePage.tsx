import React from 'react';
import Hero from '../components/features/Hero';
import FeaturedArticles from '../components/features/FeaturedArticles';
import AIFeatures from '../components/features/AIFeatures';
import ChatBot from '../components/features/ChatBot';
import { articles } from '../data/articles';

const HomePage: React.FC = () => {
  return (
    <div>
      <Hero />
      <FeaturedArticles articles={articles} />
      <AIFeatures />
      <ChatBot />
    </div>
  );
};

export default HomePage;