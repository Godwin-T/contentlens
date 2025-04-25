export interface Article {
  id: string;
  title: string;
  excerpt: string;
  content: string;
  author: Author;
  coverImage: string;
  publishedDate: string;
  readingTime: number;
  tags: string[];
}

export interface Author {
  id: string;
  name: string;
  avatar: string;
  bio: string;
}

export interface ChatMessage {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: string;
}