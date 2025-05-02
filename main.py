from src.api.twitch_api import *
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
from data.save_data import save_all_stream_data
from utils.log import *

log_config()
data_api = get_streams()

logging.info(f"Total de {len(data_api)} Streams ID's encontrados")


if not data_api:
    logging.warning('Nenhum stream ID encontrado')



max_workers = 18 # max number of threads to use
stream_details = [] # list to store the details of the streams

logging.info(f"Buscando filtros com {max_workers} threads em paralelo")
start_time = time.time()

batches = [data_api[i:i+100]for i in range(0, len(data_api), 100)]

results = []
with ThreadPoolExecutor(max_workers=max_workers) as executor:
    # Criar uma barra de progresso
    batch_results = list(tqdm(
        executor.map(get_filtered_params, data_api),
        total=len(data_api),
        desc="Processando streams"
    ))
    for batch in batch_results:
        results.append(batch)

successful = [r for r in results if 'error' not in r]
failed = [r for r in results if 'error' in r]


logging.info(f"Concluido em {time.time() - start_time:.2f} segudos")
logging.info(f"Sucesso: {len(successful)}, Falhas: {len(failed)}")

save_all_stream_data(successful)

if successful:
    print("\nExemplo de dados obtidos:")
    print()