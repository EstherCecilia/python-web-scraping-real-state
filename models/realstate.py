import time
from dataclasses import dataclass
from typing import List, Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@dataclass
class Imovel:
    endereco: str
    rua: str
    area: str
    quartos: str
    banheiros: str
    vagas: str
    preco: str

class WebScraper:
    def __init__(self, driver_path: str = "./chromedriver/chromedriver"):
        self.driver_path = driver_path
        self.driver = self._setup_driver()

    def _setup_driver(self) -> webdriver.Chrome:
        chrome_options = Options()
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--start-maximized")
        service = Service(self.driver_path)
        return webdriver.Chrome(service=service, options=chrome_options)

    def close(self):
        if self.driver:
            self.driver.quit()

class RealStateScraper(WebScraper):
    LOAD_TIMEOUT = 10


    def scrape_imoveis(self, url: str, page: int = 1) -> List[Imovel]:
        imoveis = []
        
        try:
            print(f"Processando página {page}")
            page_url = f"{url}&pagina={page}" if "?" in url else f"{url}?pagina={page}"
            self._load_page(page_url)
            imoveis.extend(self._extract_page_data())
        except Exception as e:
            print(f"Erro durante scraping: {e}")
        
        return imoveis

    def _load_page(self, url: str):
        self.driver.get(url)
        time.sleep(self.LOAD_TIMEOUT)
        # scrooll
        self.driver.execute_script("window.scrollBy(0, 800);")
        time.sleep(8)

    def _extract_page_data(self) -> List[Imovel]:
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        cards = soup.find_all("article", class_=lambda c: c and c.startswith("card-imovel"))
        print(f"Encontrados {len(cards)} imóveis na página")
        return [self._parse_imovel(card) for card in cards]

    def _parse_imovel(self, card) -> Optional[Imovel]:
        try:
            # Extrair endereço completo e separar bairro e rua
            endereco_completo = self._extract_text(card, '.endereco')
            bairro, rua = self._split_endereco(endereco_completo)
            
            return Imovel(
                endereco=bairro,  # Agora só o bairro (antes da vírgula)
                rua=rua,
                area=self._extract_area(card),
                quartos=self._extract_feature_number(card, 'quartos'),
                banheiros=self._extract_feature_number(card, 'banheiros'),
                vagas=self._extract_feature_number(card, 'vagas'),
                preco=self._extract_price(card)
            )
        except Exception as e:
            print(f"Erro ao processar imóvel: {e}")
            return None

    def _split_endereco(self, endereco: str) -> tuple:
        """Divide o endereço em bairro e rua"""
        if endereco == "N/A":
            return ("N/A", "N/A")
        parts = endereco.split(',')
        if len(parts) > 1:
            return (parts[0].strip(), parts[1].strip())
        return (endereco, "N/A")

    def _extract_feature_number(self, card, feature_type: str) -> str:
        """Extrai número de quartos/banheiros/vagas"""
        element = card.select_one(f'.caracteristica.{feature_type}')
        if not element:
            return "0"
        
        # Encontra o primeiro elemento de texto que é um número
        for content in element.contents:
            if content.name is None and content.strip():  # É um texto direto
                # Pega o primeiro token numérico
                for token in content.strip().split():
                    if token.isdigit():
                        return token
        return "0"

    def _extract_area(self, card) -> str:
        """Extrai área mantendo o m²"""
        area_element = card.select_one('.caracteristica.area')
        if not area_element:
            return "N/A"
        
        # Pega todo o texto e limpa
        area_text = area_element.get_text(strip=True)
        # Remove espaços entre número e m² (ex: "53.61 m²" -> "53.61m²")
        return area_text.replace(' ', '').replace(',', '.').replace('m²', '')

    def _extract_price(self, card) -> str:
        """Extrai o preço formatado"""
        price_tag = card.select_one('.valor')
        if not price_tag:
            return "N/A"
        
        price_text = price_tag.get_text(strip=True)
        # Remove formatação mantendo apenas números
        return price_text.replace('R$', '').replace('.', '').replace(',', '.').strip()

    def _extract_text(self, card, selector: str) -> str:
        element = card.select_one(selector)
        return element.get_text(strip=True) if element else "N/A"
    
class DataExporter:
    @staticmethod
    def to_csv(imoveis: List[Imovel], filename: str):
        if not imoveis:
            print("Nenhum dado para exportar")
            return

        df = pd.DataFrame([vars(imovel) for imovel in imoveis if imovel])
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"Dados salvos em {filename}. Total: {len(df)} imóveis")

def get_real_state(number_pages, init=1):
    url = "https://www.netimoveis.com/venda/minas-gerais/belo-horizonte/apartamento?tipo=apartamento&transacao=venda&localizacao=BR-MG-belo-horizonte---&valorMax=250000&valorMin=12000"
    
    pages = number_pages
    for page in range(init ,pages):
        scraper = RealStateScraper()
        try:
            imoveis = scraper.scrape_imoveis(url, page=page)
            DataExporter.to_csv(imoveis, f"files/real_state_{page}.csv")
        finally:
            scraper.close()
        time.sleep(10)

