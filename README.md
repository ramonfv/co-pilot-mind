# CoPilotMind 🧠✈️

**CoPilotMind** é um sistema modular para aquisição, transcrição e armazenamento estruturado de comunicações simuladas entre um operador GCS (Ground Control Station) em um ambiente de suporte a voos, utilizando o Microsoft Flight Simulator 2020.

O objetivo do projeto é criar uma base robusta de **corpus de voz** por usuário, possibilitando a aplicação com técnicas de **NLP** para aumentar a **consciência situacional** em missões simuladas, através de um assistente de voo digital.

---

## 🚀 Visão Geral

- 🔊 Aquisição de áudio (real-time)
- 🧼 Pré-processamento (redução de ruído, VAD)
- 🧠 Transcrição automática (Whisper e NVIDIA NeMo)
- 🗂️ Armazenamento estruturado por usuários
- 📤 Preparado para exportação em JSONL/CSV
- 🔌 Futura integração com MSFS SDK via SimConnect

---

## 📁 Estrutura do Projeto

co_pilot_mind/

    ├── interface/          
    ├── audio_data/          
    ├── scripts/             
    ├── data/                
    ├── services/            
    ├── config/              
    └── README.md            


---

## 🛠️ Tecnologias

- Python 3.10+
- Whisper ASR / NVIDIA NeMo
- RNNoise / DeepFilterNet (pré-processamento)
- PostgreSQL ou SQLite
- SimConnect SDK 
- JSONL / CSV

---

## 📌 Objetivos Futuros

- [ ] NLP em tempo real com transformers
- [ ] Verificação cruzada com dados de voo via SimConnect
- [ ] Análise de intenção e alerta de inconsistências
- [ ] Interface web para anotação e revisão de transcrições
- [ ] Publicação de corpus anonimizado para pesquisa

---

## 🤝 Contribuindo

Este projeto está em fase experimental, mas pretende-se evoluir para uma ferramenta de código aberto, por fazer parte de uma pesquisa fomentada pela FAPESP. Além disso, os resultados do uso serão publicados através de dissertações e artigos.

---

## 📄 Licença

MIT 

---

## ✉️ Contato

Caso tenha interesse acadêmico ou técnico, entre em contato via email: [ramonviana@ita.br ou carolinacrl@ita.br].



