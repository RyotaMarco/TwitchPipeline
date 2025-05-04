from src.api.twitch_api import TwitchAPI
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from data.save_data import save_all_stream_data
from src.utils.log import get_logger


def main():
    logger = get_logger("main")
    twitch_api = TwitchAPI()
    
    try:
        logger.info("Buscando streams da Twitch...")
        streams = twitch_api.get_streams()
        logger.info(f"Encontrados {len(streams)} streams ao vivo")
        
        if not streams:
            logger.warning("Nenhum stream encontrado")
            return
        
        stream_ids = [stream['id'] for stream in streams]


        logger.info("Processando informações detalhadas de cada stream...")
        categories_streams = []
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(twitch_api.get_filtered_params, stream_id) for stream_id in stream_ids]
            
            for future in tqdm(futures, total=len(stream_ids), desc="Processando streams"):
                stream_data = future.result()
                if 'error' not in stream_data:
                    categories_streams.append(stream_data)
        
        logger.info(f"Processados {len(categories_streams)} streams com sucesso")
        
        if categories_streams:
            save_all_stream_data(categories_streams)
            logger.info("Dados salvos com sucesso")
        
    except Exception as e:
        logger.error(f"Erro ao buscar ou processar streams: {e}")
        raise
    
    return categories_streams


if __name__ == "__main__":
    main()