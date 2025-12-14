"""Screener.in scraping module for stock data extraction."""
import requests
from bs4 import BeautifulSoup
from typing import Dict, Optional, List
import re
import pandas as pd
import os


class ScreenerScraper:
    """Scraper for extracting stock data from Screener.in."""
    
    BASE_URL = "https://www.screener.in"
    
    def __init__(self):
        """Initialize the scraper with proper headers and load stock mapping."""
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        
        # Load stock mapping from Excel file
        self.stock_mapping = self._load_stock_mapping()
    
    def _load_stock_mapping(self) -> Dict[str, Dict[str, str]]:
        """
        Load stock mapping from Excel file.
        
        Returns:
            Dictionary mapping query terms to stock info (slug, name, symbol)
        """
        mapping = {}
        try:
            excel_path = "screener links.xlsx"
            if not os.path.exists(excel_path):
                print(f"Warning: {excel_path} not found. Using empty mapping.")
                return mapping
            
            df = pd.read_excel(excel_path)
            
            # Filter out rows with NaN NSE Symbol (category headers)
            df = df[df['NSE Symbol'].notna()]
            df = df[df['Company Name'].notna()]
            
            for _, row in df.iterrows():
                company_name = str(row['Company Name']).strip()
                nse_symbol = str(row['NSE Symbol']).strip()
                screener_link = str(row.get('Screener.in Link (Template)', '')).strip()
                
                # Extract slug from link (format: https://www.screener.in/company/SLUG/)
                slug = None
                if screener_link and 'company/' in screener_link:
                    slug = screener_link.split('company/')[-1].rstrip('/')
                elif nse_symbol:
                    slug = nse_symbol
                
                if not slug:
                    continue
                
                # Create searchable terms
                search_terms = [
                    company_name.lower(),
                    nse_symbol.lower(),
                    # Add partial matches for common names
                    company_name.split()[0].lower() if company_name else None,
                ]
                
                # Store mapping
                stock_info = {
                    'slug': slug,
                    'name': company_name,
                    'symbol': nse_symbol
                }
                
                for term in search_terms:
                    if term:
                        # Store with original query format
                        mapping[term] = stock_info
                        # Also store without common suffixes
                        if term.endswith(' ltd.') or term.endswith(' ltd'):
                            mapping[term.replace(' ltd.', '').replace(' ltd', '')] = stock_info
                        if term.endswith(' limited'):
                            mapping[term.replace(' limited', '')] = stock_info
            
            print(f"Loaded {len(set(info['slug'] for info in mapping.values()))} stocks from Excel file")
            return mapping
            
        except Exception as e:
            print(f"Error loading stock mapping: {e}")
            return {}
    
    def search_stock(self, query: str) -> Optional[Dict[str, str]]:
        """
        Search for a stock in the Nifty 50 mapping.
        
        Args:
            query: Stock name or symbol (e.g., "reliance", "tcs", "hdfcbank")
            
        Returns:
            Stock info dict with slug, name, symbol if found, None otherwise
        """
        query_lower = query.lower().strip()
        
        # Direct match
        if query_lower in self.stock_mapping:
            return self.stock_mapping[query_lower]
        
        # Partial match in company name or symbol
        for term, stock_info in self.stock_mapping.items():
            if (query_lower in term or term in query_lower or
                query_lower in stock_info['name'].lower() or
                query_lower in stock_info['symbol'].lower() or
                stock_info['symbol'].lower() in query_lower):
                return stock_info
        
        return None
    
    def extract_value(self, soup: BeautifulSoup, label: str) -> Optional[str]:
        """
        Extract a value from the company page by label.
        
        Args:
            soup: BeautifulSoup object of the page
            label: Label text to search for
            
        Returns:
            Value as string or None
        """
        try:
            # Find the label element
            label_elem = soup.find("span", string=re.compile(label, re.I))
            if label_elem:
                # Find the next sibling or parent's next sibling that contains the value
                parent = label_elem.find_parent()
                if parent:
                    value_elem = parent.find("span", class_="number")
                    if value_elem:
                        return value_elem.get_text(strip=True)
                    # Alternative: look for next sibling
                    next_sibling = parent.find_next_sibling()
                    if next_sibling:
                        value_elem = next_sibling.find("span", class_="number")
                        if value_elem:
                            return value_elem.get_text(strip=True)
        except Exception as e:
            print(f"Error extracting {label}: {e}")
        return None
    
    def extract_from_table(self, soup: BeautifulSoup, row_label: str) -> Optional[str]:
        """
        Extract value from a table row by label.
        
        Args:
            soup: BeautifulSoup object
            row_label: Label in the table row
            
        Returns:
            Value as string or None
        """
        try:
            # Find table rows
            rows = soup.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 2:
                    if row_label.lower() in cells[0].get_text(strip=True).lower():
                        value = cells[1].get_text(strip=True)
                        return value if value else None
        except Exception as e:
            print(f"Error extracting from table {row_label}: {e}")
        return None
    
    def extract_from_key_metrics(self, soup: BeautifulSoup, label: str) -> Optional[str]:
        """
        Extract value from key metrics section using various selectors.
        
        Args:
            soup: BeautifulSoup object
            label: Label to search for
            
        Returns:
            Value as string or None
        """
        # Try multiple strategies to find the metric
        strategies = [
            # Strategy 1: Look for data attributes
            lambda: soup.find(attrs={"data-name": re.compile(label, re.I)}),
            # Strategy 2: Look for spans with specific classes
            lambda: soup.find("span", string=re.compile(f"^{label}", re.I)),
            # Strategy 3: Look in key metrics divs
            lambda: soup.find("div", class_=re.compile("key-metric", re.I)),
        ]
        
        for strategy in strategies:
            try:
                elem = strategy()
                if elem:
                    # Try to find value near the element
                    parent = elem.find_parent()
                    if parent:
                        # Look for number class
                        value_elem = parent.find(class_=re.compile("number|value", re.I))
                        if value_elem:
                            return value_elem.get_text(strip=True)
                        # Look for next sibling
                        next_elem = parent.find_next_sibling()
                        if next_elem:
                            value_elem = next_elem.find(class_=re.compile("number|value", re.I))
                            if value_elem:
                                return value_elem.get_text(strip=True)
            except:
                continue
        
        return None
    
    def scrape_company_data(self, slug: str) -> Dict[str, Optional[str]]:
        """
        Scrape company data from Screener.in.
        
        Args:
            slug: Company slug from search
            
        Returns:
            Dictionary containing scraped metrics
        """
        url = f"{self.BASE_URL}/company/{slug}/"
        
        try:
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "lxml")
            
            data = {}
            
            # Try to get company name first
            name_elem = soup.find("h1")
            if name_elem:
                data["Company Name"] = name_elem.get_text(strip=True)
            
            # Extract Current Price (multiple methods)
            price_elem = soup.find("span", id="top-price")
            if not price_elem:
                price_elem = soup.find("span", class_=re.compile("price", re.I))
            if not price_elem:
                # Look for price in key metrics
                price_elem = soup.find(string=re.compile("Current Price", re.I))
                if price_elem:
                    parent = price_elem.find_parent()
                    if parent:
                        price_elem = parent.find_next_sibling()
            if price_elem:
                price_text = price_elem.get_text(strip=True) if hasattr(price_elem, 'get_text') else str(price_elem)
                # Clean price text
                price_text = re.sub(r'[^\d.,]', '', price_text)
                if price_text:
                    data["Current Price"] = f"₹{price_text}" if not price_text.startswith('₹') else price_text
            
            # Extract metrics using multiple strategies
            metrics_to_extract = {
                "Market Cap": ["Market Cap", "Market capitalization"],
                "P/E": ["P/E", "PE", "Price to Earnings"],
                "ROCE": ["ROCE", "Return on Capital Employed"],
                "ROE": ["ROE", "Return on Equity"],
                "Debt": ["Debt", "Total Debt"],
                "High / Low": ["High / Low", "52W High / Low"],
                "Profit Growth": ["Profit Growth", "Net Profit Growth"],
                "Sales Growth": ["Sales Growth", "Revenue Growth"],
                "Cash Flows": ["Cash", "Cash Flow", "Operating Cash Flow"]
            }
            
            for metric_key, search_terms in metrics_to_extract.items():
                value = None
                for term in search_terms:
                    # Try different extraction methods
                    value = (self.extract_from_key_metrics(soup, term) or 
                            self.extract_value(soup, term) or 
                            self.extract_from_table(soup, term))
                    if value:
                        break
                
                if value:
                    data[metric_key] = value
            
            # Special handling for High/Low if not found together
            if "High / Low" not in data or not data["High / Low"]:
                high = None
                low = None
                for term in ["High", "52W High"]:
                    high = self.extract_from_table(soup, term) or self.extract_value(soup, term)
                    if high:
                        break
                for term in ["Low", "52W Low"]:
                    low = self.extract_from_table(soup, term) or self.extract_value(soup, term)
                    if low:
                        break
                if high and low:
                    data["High / Low"] = f"{high} / {low}"
            
            return data
            
        except Exception as e:
            print(f"Error scraping company data: {e}")
            return {}
    
    def get_stock_data(self, query: str) -> Dict[str, Optional[str]]:
        """
        Complete workflow: search and scrape stock data.
        
        Args:
            query: Stock name or symbol
            
        Returns:
            Dictionary containing scraped metrics
        """
        stock_info = self.search_stock(query)
        if not stock_info:
            return {"error": f"Stock '{query}' not found in Nifty 50. Please use company name or NSE symbol (e.g., 'tcs', 'reliance', 'hdfcbank')."}
        
        slug = stock_info['slug']
        data = self.scrape_company_data(slug)
        if not data or len(data) == 0:
            return {"error": f"Could not scrape data for '{query}'"}
        
        # Add stock info
        data["slug"] = slug
        if "Company Name" not in data or not data["Company Name"]:
            data["Company Name"] = stock_info['name']
        data["NSE Symbol"] = stock_info['symbol']
        
        return data

