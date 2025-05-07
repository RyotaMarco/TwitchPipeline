from src.api.twitch_api import TwitchAPI
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from data.save_data import save_all_stream_data
from src.service.etl import PySparkETL
from src.utils.log import get_logger
import os


def main():
    logger = get_logger("main")
    twitch_api = TwitchAPI()
    
    try:
        logger.info("Iniciando coleta de dados da Twitch...")

        streams = twitch_api.get_streams()
        logger.info(f"Encontrados {len(streams)} streams ao vivo")
        
        if not streams:
            logger.warning("Nenhum stream encontrado")
            return
        
        if streams:
            logger.info(f"Exemplo de stream: {streams[0]}")
        
        logger.info("Processando dados dos streams em paralelo...")
        categories_streams = []
        
        with ThreadPoolExecutor(max_workers=18) as executor:
            futures = [executor.submit(twitch_api.filter_stream_data, stream) for stream in streams]
            
        
            for future in tqdm(futures, total=len(streams), desc="Processando streams"):
                stream_data = future.result()
                if stream_data and 'error' not in stream_data:
                    categories_streams.append(stream_data)
                else:
                    logger.warning(f"Stream descartado ou erro: {stream_data}")
        
        logger.info(f"Processados {len(categories_streams)} streams com sucesso")
        
        
        if categories_streams:
            save_all_stream_data(categories_streams)
            logger.info("Dados salvos com sucesso")
        else:
            logger.warning("Nenhum stream processado com sucesso para salvar")

        logger.info("Iniciando transformação de JSON para Parquet.")

        etl = PySparkETL()

        spark = etl.spark_session()

        schema = etl.get_schema()

        json_path = f'{os.getenv("RAW_DATA")}/*.json'
        output_path = os.getenv("PROCESSED_DATA")

        df = etl.read_json(spark=spark, json_path=json_path, schema=schema)
        df_clean = etl.clean_data(df)
        etl.parquet_transform(df_clean, output_path=output_path, partition_col="user_id")

        
    except Exception as e:
        logger.error(f"Erro ao buscar ou processar streams: {e}")
        raise
    
    return categories_streams


if __name__ == "__main__":
    main()