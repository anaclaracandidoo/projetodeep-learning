# 📚 EduAcessível

Sistema de apoio pedagógico desenvolvido no âmbito da disciplina de **Projeto Integrador: Deep Learning** (`projetodeep-learning`), voltado para a adaptação de materiais didáticos para **alunos surdos** e para o apoio à organização docente.

## 🎯 Objetivo do Projeto
Facilitar o trabalho de professores na adaptação de conteúdos escolares (como PDF, DOCX e TXT) para formatos mais acessíveis visual e linguisticamente a estudantes surdos, mantendo também funcionalidades de registo de planos de aula e histórico de materiais processados.

## 🤟 Principais Funcionalidades
* **Extração de Conteúdo:** lê documentos enviados pelo utilizador (`PDF`, `DOCX` ou `TXT`) através do backend.
* **Adaptação para Português L2 (Leitura Visual Direta):** reestrutura textos extensos em frases curtas, diretas e com destaque visual de conceitos-chave.
* **Resumo em Glosa de Libras:** organiza os conceitos centrais na estrutura tópico-comentário.
* **Glossário Visual Real:** explica termos e conceitos por meio de exemplos concretos do dia a dia.
* **Atividades Adaptadas:** ajusta questões para apoiar a compreensão do estudante, incluindo dicas guiadas quando aplicável.
* **Exportação e Acessibilidade:** permite transferir o material adaptado em `.txt` e integra o widget do **VLibras**.
* **Gestão Docente e Histórico:** reúne painel principal, gestão de planos de aula e histórico de materiais com data e hora configuradas para `America/Sao_Paulo`.

## 🧩 Estrutura do Repositório
* `main.py`: lógica de backend e extração de texto dos ficheiros.
* `requirements.txt`: dependências necessárias para executar o projeto.
* `10_projeto_unificado.ipynb`: caderno principal unificado que clona o repositório, instala as dependências, integra o backend e inicia a interface interativa.
* `01_...` a `09_...` e `API_EduAcessivel.ipynb`: etapas modulares e experimentais construídas durante o desenvolvimento do projeto integrador.

## ▶️ Como Executar no Google Colab
1. Abra o caderno `10_projeto_unificado.ipynb` no Google Colab.
2. Configure a variável de ambiente / chave da API (`GEMINI_API_KEY`) na célula correspondente antes de executar.
3. Execute as células em sequência para iniciar o serviço e abrir a interface.
