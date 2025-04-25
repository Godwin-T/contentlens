import { Article } from '../types';

export const articles: Article[] = [
  {
    id: '1',
    title: 'Understanding the Future of Artificial Intelligence',
    excerpt: 'A deep dive into how AI is shaping our world and what to expect in the coming years.',
    content: `
      # Understanding the Future of Artificial Intelligence

      Artificial Intelligence has become an integral part of our daily lives, from the smartphones we use to the recommendations we receive on streaming platforms. But what does the future hold for this rapidly evolving technology?

      ## Current State of AI

      Today's AI systems are primarily focused on narrow tasks - recognizing images, translating languages, or playing games. These systems, while impressive, are examples of what experts call "narrow AI" - designed to perform specific tasks without the broader understanding that humans possess.

      ## The Path to General AI

      Researchers are now working towards developing Artificial General Intelligence (AGI) - systems that can understand, learn, and apply knowledge across a wide range of tasks, similar to human intelligence. This represents a significant leap from current capabilities.

      ## Ethical Considerations

      As AI becomes more sophisticated, important ethical questions arise:
      
      - How do we ensure AI systems make fair and unbiased decisions?
      - What happens to jobs that become automated?
      - How do we maintain privacy in a world of intelligent systems?
      - Who is responsible when AI systems make mistakes?

      ## The Future Landscape

      The integration of AI into more aspects of our lives seems inevitable. From healthcare diagnostics to climate change solutions, AI promises to help address some of humanity's most pressing challenges. However, thoughtful regulation and ethical frameworks will be essential to guide this powerful technology.

      The journey of AI is just beginning, and how we choose to develop and deploy these systems will shape our collective future for generations to come.
    `,
    author: {
      id: '1',
      name: 'Dr. Maya Patel',
      avatar: 'https://images.pexels.com/photos/3799785/pexels-photo-3799785.jpeg?auto=compress&cs=tinysrgb&w=150',
      bio: 'AI researcher and professor at Technology Institute'
    },
    coverImage: 'https://images.pexels.com/photos/8386440/pexels-photo-8386440.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    publishedDate: '2023-11-15',
    readingTime: 8,
    tags: ['Artificial Intelligence', 'Technology', 'Ethics', 'Future']
  },
  {
    id: '2',
    title: 'The Rise of Sustainable Architecture',
    excerpt: 'How architects are incorporating eco-friendly practices into modern building design.',
    content: `
      # The Rise of Sustainable Architecture

      As climate change concerns mount, the architecture world is responding with innovative approaches to building design that prioritize sustainability and environmental responsibility.

      ## Green Building Principles

      Sustainable architecture focuses on reducing environmental impact through energy efficiency, resource conservation, and harmony with the surrounding environment. Modern green buildings often incorporate:

      - Solar panels and other renewable energy sources
      - Rainwater harvesting systems
      - Natural lighting and ventilation
      - Locally-sourced, sustainable building materials
      - Green roofs and walls

      ## Notable Examples

      Around the world, groundbreaking projects are demonstrating the potential of sustainable design:

      **The Edge (Amsterdam)** - Often called the world's most sustainable office building, featuring smart technology that optimizes energy use.

      **Bosco Verticale (Milan)** - Residential towers covered with trees and plants, creating a vertical forest that absorbs CO2 and produces oxygen.

      **Gardens by the Bay (Singapore)** - Iconic supertrees that harvest solar energy and collect rainwater, while serving as vertical gardens.

      ## Economic Benefits

      While sustainable buildings may have higher upfront costs, they typically offer significant long-term savings through reduced energy consumption, lower maintenance costs, and increased property values. Studies show that green buildings can reduce energy use by 25-30% compared to conventional structures.

      ## The Future Direction

      The future of architecture lies in regenerative design - buildings that not only minimize negative environmental impacts but actively contribute to the health of ecosystems. This includes buildings that generate more energy than they consume, purify water and air, and even provide habitats for local wildlife.

      As climate challenges intensify, sustainable architecture isn't just an aesthetic choice—it's becoming an essential approach to building our future communities.
    `,
    author: {
      id: '2',
      name: 'Carlos Rodriguez',
      avatar: 'https://images.pexels.com/photos/220453/pexels-photo-220453.jpeg?auto=compress&cs=tinysrgb&w=150',
      bio: 'Award-winning architect specializing in sustainable design'
    },
    coverImage: 'https://images.pexels.com/photos/2119713/pexels-photo-2119713.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    publishedDate: '2023-12-03',
    readingTime: 6,
    tags: ['Architecture', 'Sustainability', 'Environment', 'Design']
  },
  {
    id: '3',
    title: 'The Psychology of Decision Making',
    excerpt: 'Exploring how our minds work when making choices and ways to improve decision-making processes.',
    content: `
      # The Psychology of Decision Making

      Every day, we make countless decisions - from what to eat for breakfast to major life choices about careers and relationships. But what's happening in our brains during this process?

      ## The Dual-System Theory

      Psychologist Daniel Kahneman popularized the concept that we have two systems for decision making:

      **System 1**: Fast, automatic, emotional, and intuitive
      **System 2**: Slow, deliberate, logical, and calculating

      Many of our daily decisions are handled by System 1, which relies on mental shortcuts (heuristics) to make quick judgments. While efficient, this system is prone to biases.

      ## Common Decision-Making Biases

      Understanding these biases can help us make better choices:

      - **Confirmation Bias**: Favoring information that confirms existing beliefs
      - **Availability Heuristic**: Overestimating the likelihood of events based on how easily examples come to mind
      - **Loss Aversion**: Feeling losses more strongly than equivalent gains
      - **Anchoring Effect**: Relying too heavily on the first piece of information encountered

      ## Improving Decision Making

      Research suggests several strategies to enhance decision quality:

      1. **Slow down**: For important decisions, engage System 2 by deliberately taking time to consider options.
      
      2. **Consider the opposite**: Intentionally explore contrary perspectives to counter confirmation bias.
      
      3. **Use decision frameworks**: Structured approaches like pros/cons lists or decision matrices can help organize thinking.
      
      4. **Recognize emotional states**: Strong emotions can cloud judgment; sometimes it's best to delay decisions until emotions settle.

      ## The Role of Intuition

      While biases can lead us astray, intuition isn't always wrong. Experts in a field often develop reliable intuitive judgments based on extensive experience. The key is knowing when to trust your gut and when to engage in more deliberate analysis.

      Understanding the psychology behind our choices won't guarantee perfect decisions, but it can help us navigate life's complexities with greater awareness and intention.
    `,
    author: {
      id: '3',
      name: 'Dr. Sarah Kim',
      avatar: 'https://images.pexels.com/photos/774909/pexels-photo-774909.jpeg?auto=compress&cs=tinysrgb&w=150',
      bio: 'Cognitive psychologist and behavioral researcher'
    },
    coverImage: 'https://images.pexels.com/photos/3758105/pexels-photo-3758105.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2',
    publishedDate: '2024-01-20',
    readingTime: 7,
    tags: ['Psychology', 'Decision Making', 'Cognitive Bias', 'Mental Health']
  }
];

export const getArticleById = (id: string): Article | undefined => {
  return articles.find(article => article.id === id);
};

export const getArticlesByTag = (tag: string): Article[] => {
  return articles.filter(article => article.tags.includes(tag));
};

export const searchArticles = (query: string): Article[] => {
  const lowercaseQuery = query.toLowerCase();
  return articles.filter(article => 
    article.title.toLowerCase().includes(lowercaseQuery) || 
    article.excerpt.toLowerCase().includes(lowercaseQuery) || 
    article.content.toLowerCase().includes(lowercaseQuery) ||
    article.tags.some(tag => tag.toLowerCase().includes(lowercaseQuery))
  );
};