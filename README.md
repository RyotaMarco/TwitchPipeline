# 🛡️ Pipeline de Análise de Copyright e Uso Indevido em Streams (Twitch)

Este projeto implementa um pipeline completo e escalável na AWS para identificar possíveis violações de direitos autorais e uso indevido de categorias em streams de vídeo — com foco especial em **categorias menos populares da Twitch**.

---

## ⚙️ Arquitetura

![Diagrama da Arquitetura](https://github.com/user-attachments/assets/7526aaf8-4570-4574-ac68-62085ba6f394)

### Componentes principais:

| Serviço        | Função                                                                 |
|----------------|------------------------------------------------------------------------|
| **EC2 + PySpark** | Coleta dados da API (streaming) e realiza ETL transformando para Parquet |
| **S3**         | Armazena os dados transformados                                         |
| **Lambda (Score)** | Calcula um score com base em critérios definidos                    |
| **MongoDB**    | Armazena streams suspeitas com `score >= 5`                             |
| **Step Function** | Orquestra o fluxo completo para análise profunda com IA              |
| **Gemini 1.5 Flash** | Analisa contexto textual dos streams suspeitos (uso de IA generativa) |
| **RDS (PostgreSQL)** | Armazena resultado final da análise (todos os streams)             |
| **API Gateway + SQS** | Permite integração com novos consumidores de dados                 |
| **EventBridge** | Publica eventos de análise completa para desacoplar consumidores       |
| **Looker**     | Visualiza dados para tomada de decisão                                  |

---

## 📌 Objetivos do Projeto

- **Detectar uso indevido de categorias na Twitch** com base em padrões de conteúdo.
- **Avaliar risco de violação de copyright** através de análise contextual e IA.
- **Oferecer um sistema desacoplado e extensível**, capaz de evoluir com novos componentes (ex: novos dashboards, alertas, etc.).
- **Explorar tecnologias da AWS dentro do free tier**, com foco em escalabilidade, custo zero e boas práticas de engenharia de dados.

---

## 🧪 Funcionalidades

- ✅ Coleta e transformação de dados em lote com PySpark
- ✅ Armazenamento otimizado em S3 no formato Parquet
- ✅ Score automático com lógica configurável
- ✅ Análise aprofundada via IA generativa (Gemini)
- ✅ Orquestração com Step Function e Lambda Functions
- ✅ Dados enriquecidos e categorizados no RDS
- ✅ Notificações via EventBridge para múltiplos destinos
- ✅ Visualização dos dados com Looker

---
