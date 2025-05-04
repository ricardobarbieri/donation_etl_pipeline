import pandas as pd
import requests
import sqlite3
import psycopg2
import json
import logging
import schedule
import time
from datetime import datetime
from pathlib import Path

# Configuração de logging
logging.basicConfig(
    filename='pipeline.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DonationPipeline:
    def __init__(self, db_type='sqlite', db_name='donations.db', pg_conn_params=None):
        self.db_type = db_type
        self.db_name = db_name
        self.pg_conn_params = pg_conn_params or {}
        self.data_dir = Path('data')
        self.data_dir.mkdir(exist_ok=True)

    def extract_data(self, use_api=False):
        """Extrai dados de uma API ou arquivo JSON local."""
        try:
            if use_api:
                # Exemplo com Open Collective API (substitua por uma API real se disponível)
                url = "https://api.opencollective.com/v1/collectives"
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                data = response.json()['data']
            else:
                # Dados fictícios locais para testes
                local_file = self.data_dir / 'donations.json'
                if not local_file.exists():
                    sample_data = [
                        {"donor_id": 1, "amount": 50.0, "campaign_id": 101, "timestamp": "2025-05-03T10:00:00"},
                        {"donor_id": 2, "amount": 100.0, "campaign_id": 102, "timestamp": "2025-05-03T10:01:00"},
                        {"donor_id": 1, "amount": 75.0, "campaign_id": 101, "timestamp": "2025-05-03T10:02:00"}
                    ]
                    with open(local_file, 'w') as f:
                        json.dump(sample_data, f)
                with open(local_file, 'r') as f:
                    data = json.load(f)
            df = pd.DataFrame(data)
            logging.info("Extração concluída: %d registros obtidos", len(df))
            return df
        except Exception as e:
            logging.error("Falha na extração: %s", e)
            raise

    def transform_data(self, df):
        """Transforma os dados: limpeza e agregação."""
        try:
            if df.empty:
                raise ValueError("DataFrame vazio")
            
            # Limpeza
            df = df.dropna(subset=['donor_id', 'amount', 'campaign_id'])
            df['amount'] = pd.to_numeric(df['amount'], errors='coerce')
            df = df.dropna(subset=['amount'])
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.drop_duplicates(subset=['donor_id', 'timestamp'])
            df['processed_at'] = datetime.now()

            # Agregação: total e contagem de doações por campanha
            stats = df.groupby('campaign_id').agg(
                total_amount=pd.NamedAgg(column='amount', aggfunc='sum'),
                donation_count=pd.NamedAgg(column='amount', aggfunc='count')
            ).reset_index()

            logging.info("Transformação concluída: %d registros após limpeza", len(df))
            return df, stats
        except Exception as e:
            logging.error("Falha na transformação: %s", e)
            raise

    def load_data(self, df, stats):
        """Carrega os dados no banco de dados."""
        try:
            if self.db_type == 'sqlite':
                conn = sqlite3.connect(self.db_name)
                df.to_sql('donations', conn, if_exists='append', index=False)
                stats.to_sql('stats', conn, if_exists='replace', index=False)
                conn.close()
            elif self.db_type == 'postgres':
                conn = psycopg2.connect(**self.pg_conn_params)
                df.to_sql('donations', conn, if_exists='append', index=False, schema='public')
                stats.to_sql('stats', conn, if_exists='replace', index=False, schema='public')
                conn.close()
            logging.info("Carregamento concluído: %d registros salvos", len(df))
            return True
        except Exception as e:
            logging.error("Falha no carregamento: %s", e)
            raise

    def run(self, use_api=False):
        """Executa o pipeline ETL completo."""
        try:
            df = self.extract_data(use_api)
            df_transformed, stats = self.transform_data(df)
            self.load_data(df_transformed, stats)
            return df_transformed, stats
        except Exception as e:
            logging.error("Pipeline falhou: %s", e)
            raise

    def schedule_pipeline(self, interval_minutes=60):
        """Agenda a execução do pipeline."""
        def job():
            logging.info("Iniciando pipeline agendado")
            self.run()
            logging.info("Pipeline agendado concluído")
        
        schedule.every(interval_minutes).minutes.do(job)
        while True:
            schedule.run_pending()
            time.sleep(60)

    def export_data(self, df, format='csv'):
        """Exporta dados para CSV ou JSON."""
        try:
            output_file = self.data_dir / f'export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.{format}'
            if format == 'csv':
                df.to_csv(output_file, index=False)
            elif format == 'json':
                df.to_json(output_file, orient='records', lines=True)
            logging.info("Dados exportados para %s", output_file)
            return output_file
        except Exception as e:
            logging.error("Falha na exportação: %s", e)
            raise