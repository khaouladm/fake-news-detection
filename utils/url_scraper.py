import requests
from bs4 import BeautifulSoup
import streamlit as st
import re
import nltk

class URLScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Ensure NLTK data is available for newspaper3k
        self._ensure_nltk_data()
    
    def _ensure_nltk_data(self):
        """Silently check and download required NLTK data"""
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt', quiet=True)

    def scrape_with_newspaper3k(self, url):
        """Scrape article content using newspaper3k library"""
        try:
            # Try to import newspaper3k
            try:
                from newspaper import Article
                from newspaper import Config
            except ImportError:
                st.warning("newspaper3k not available, using fallback method")
                return {'success': False, 'error': 'newspaper3k not installed'}
            
            # Configure to mimic a browser
            config = Config()
            config.browser_user_agent = self.headers['User-Agent']
            config.request_timeout = 10
            
            # newspaper3k auto-detects language, which is usually sufficient
            article = Article(url, config=config)
            article.download()
            article.parse()
            
            # Only perform NLP if we have content
            if article.text and len(article.text) > 100:
                try:
                    article.nlp()
                    summary = article.summary
                except Exception:
                    # NLP might fail on non-supported languages, but text extraction often succeeds
                    summary = ""
            else:
                summary = ""
            
            # Clean the text (remove multilingual boilerplate)
            cleaned_content = self.clean_text(article.text)
            
            return {
                'title': article.title or "No title found",
                'content': cleaned_content,
                'summary': summary,
                'authors': article.authors,
                'publish_date': str(article.publish_date) if article.publish_date else "",
                'top_image': article.top_image,
                'success': True if cleaned_content and len(cleaned_content) > 100 else False
            }
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def scrape_with_bs4(self, url):
        """Fallback scraping with BeautifulSoup"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside", "form", "iframe", "noscript"]):
                script.decompose()
            
            # Try to get title
            title = ""
            title_selectors = [
                'h1', 'title', '.headline', '.title', 
                '[class*="headline"]', 'h1[class*="title"]',
                '.article-title', '.story-title'
            ]
            
            for selector in title_selectors:
                element = soup.select_one(selector)
                if element:
                    title_text = element.get_text().strip()
                    if title_text and len(title_text) > 10:
                        title = title_text
                        break
            
            # Try to get content from article-specific elements
            content = ""
            content_selectors = [
                'article', '.article-content', '.story-content', '.post-content',
                '[class*="content"]', 'main', '.main-content', '.entry-content', '.post-body'
            ]
            
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content_parts = []
                    for elem in elements:
                        text = elem.get_text(separator=' ').strip()
                        if text and len(text) > 50:
                            content_parts.append(text)
                    
                    if content_parts:
                        content = ' '.join(content_parts)
                        break
            
            # If no specific content found, get all paragraphs from main content areas
            if not content or len(content) < 200:
                main_content = soup.find('main') or soup.find('article') or soup.find('body')
                if main_content:
                    paragraphs = main_content.find_all('p')
                    content = ' '.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
            
            # Clean up content
            content = self.clean_text(content)
            
            return {
                'title': title or "No title found",
                'content': content,
                'success': True if content and len(content) > 200 else False
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def clean_text(self, text):
        """Clean extracted text with multilingual support (EN, FR, AR)"""
        if not text:
            return ""
        
        # Remove extra whitespace (preserving internal spaces for Arabic/Latin)
        text = re.sub(r'\s+', ' ', text)
        
        # Multilingual Boilerplate Phrases to remove
        boilerplate_phrases = [
            # English
            'subscribe to our newsletter', 'follow us on', 'share this article',
            'read more', 'related articles', 'comments', 'advertisement',
            'privacy policy', 'terms of use', 'cookie policy', 'all rights reserved',
            'click here', 'sign up', 'log in', 'copyright',
            
            # French
            'abonnez-vous', 'suivez-nous', 'partager cet article',
            'lire la suite', 'articles connexes', 'commentaires', 'publicité',
            'politique de confidentialité', 'conditions d\'utilisation', 'tous droits réservés',
            'cliquez ici', 's\'inscrire', 'se connecter', 'en savoir plus', 'droits d\'auteur',
            
            # Arabic
            'اشترك في نشرتنا', 'تابعنا على', 'شارك هذا المقال',
            'اقرأ المزيد', 'مقالات ذات صلة', 'تعليقات', 'إعلان',
            'سياسة الخصوصية', 'شروط الاستخدام', 'جميع الحقوق محفوظة',
            'اضغط هنا', 'تسجيل الدخول', 'أنشئ حساباً', 'المزيد من الأخبار',
            'حقوق النشر', 'اتصل بنا', 'من نحن'
        ]
        
        # Create a regex pattern that matches any of these phrases (case insensitive)
        # We escape special regex characters in the phrases just in case
        pattern = '|'.join(map(re.escape, boilerplate_phrases))
        
        # Remove matches
        text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        return text.strip()
    
    def scrape_article(self, url):
        """Main function to scrape article from URL"""
        # Validate URL
        if not url:
            return {'success': False, 'error': 'No URL provided'}
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        alert_box("Message à afficher", alert_type="success")

        
        # Try newspaper3k first (Better at detecting main content)
        result = self.scrape_with_newspaper3k(url)
        
        if result['success']:
            return result
        
        # If newspaper3k fails, try BeautifulSoup
        alert_box("Trying alternative scraping method...", alert_type="info")
        result = self.scrape_with_bs4(url)
        
        if result['success']:
            return result
        
        # If both methods fail
        return {
            'success': False,
            'error': 'Could not extract meaningful content from this URL',
            'title': 'Extraction failed',
            'content': 'Unable to extract article content. The website might be blocking scrapers or require JavaScript.'
        }