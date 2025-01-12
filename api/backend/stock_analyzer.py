import numpy as np
from typing import List, Dict, Tuple
import json
from datetime import datetime, timedelta

class StockAnalyzer:
    def __init__(self, db_connection):
        self.db = db_connection
        
    def get_historical_data(self, ticker: str) -> List[Dict]:
        """Retrieve historical data for a given stock ticker"""
        cursor = self.db.cursor()
        cursor.execute('''
            SELECT date, close_price, volume 
            FROM stock_historical_data 
            WHERE ticker = %s 
            ORDER BY date DESC 
            LIMIT 30
        ''', (ticker,))
        return cursor.fetchall()
    
    def calculate_moving_averages(self, prices: List[float]) -> Tuple[float, float]:
        """Calculate short (5-day) and long (20-day) moving averages"""
        if len(prices) < 20:
            return None, None
        
        short_ma = np.mean(prices[:5])
        long_ma = np.mean(prices[:20])
        return short_ma, long_ma
    
    def calculate_rsi(self, prices: List[float], period: int = 14) -> float:
        """Calculate Relative Strength Index"""
        if len(prices) < period + 1:
            return None
            
        deltas = np.diff(prices)
        gains = np.clip(deltas, 0, None)
        losses = -np.clip(deltas, None, 0)
        
        avg_gain = np.mean(gains[:period])
        avg_loss = np.mean(losses[:period])
        
        if avg_loss == 0:
            return 100
            
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def analyze_stock(self, ticker: str) -> Dict:
        """Perform comprehensive stock analysis and return buy/sell recommendation"""
        historical_data = self.get_historical_data(ticker)
        if not historical_data:
            return {"error": "No historical data available"}
            
        prices = [row['close_price'] for row in historical_data]
        volumes = [row['volume'] for row in historical_data]
        
        short_ma, long_ma = self.calculate_moving_averages(prices)
        rsi = self.calculate_rsi(prices)
        avg_volume = np.mean(volumes)
        recent_volume = volumes[0]
        volume_trend = (recent_volume - avg_volume) / avg_volume * 100
        
        # Price trend
        price_change = ((prices[0] - prices[-1]) / prices[-1]) * 100
        
        # Generate trading signal
        signal = 0  # Initialize neutral signal
        
        if short_ma and long_ma:
            if short_ma > long_ma:
                signal += 1  # Bullish signal
            else:
                signal -= 1  # Bearish signal
                
        if rsi:
            if rsi < 30:
                signal += 1  # Oversold - buying opportunity
            elif rsi > 70:
                signal -= 1  # Overbought - selling opportunity
                
        if volume_trend > 20:  # Significant volume increase
            signal += 0.5 if price_change > 0 else -0.5
            
        # Convert signal to recommendation
        recommendation = {
            "ticker": ticker,
            "signal": signal,
            "recommendation": "BUY" if signal > 0 else "SELL" if signal < 0 else "HOLD",
            "confidence": abs(signal) / 3.5 * 100,  # Normalize to percentage
            "indicators": {
                "rsi": rsi,
                "short_term_ma": short_ma,
                "long_term_ma": long_ma,
                "volume_trend": volume_trend,
                "price_change": price_change
            }
        }
        
        return recommendation
        
    def update_stock_indicators(self, ticker: str) -> None:
        """Update stock trend indicators in the database"""
        analysis = self.analyze_stock(ticker)
        if "error" not in analysis:
            cursor = self.db.cursor()
            cursor.execute('''
                UPDATE stock 
                SET trend_indicator = %s 
                WHERE ticker = %s
            ''', (analysis["signal"], ticker))
            self.db.commit()