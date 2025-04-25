import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL;

if (!API_URL) {
  throw new Error('Missing API URL environment variable');
}

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getArticles = async () => {
  const response = await api.get('/articles');
  return response.data;
};

export const getArticleById = async (id: string) => {
  const response = await api.get(`/articles/${id}`);
  return response.data;
};

export const searchArticles = async (query: string) => {
  const response = await api.get(`/articles/search?q=${encodeURIComponent(query)}`);
  return response.data;
};

export const getArticlesByTag = async (tag: string) => {
  const response = await api.get(`/articles/tag/${encodeURIComponent(tag)}`);
  return response.data;
};

export const askQuestion = async (articleId: string, question: string) => {
  const response = await api.post(`/articles/${articleId}/ask`, { question });
  return response.data;
};

export const searchAI = async (query: string) => {
  const response = await api.post('/search/ai', { query });
  return response.data;
};