# README - Algoritmos de Otimização e Processamento de Leads

2ESPR - Challenge 2 SEMESTRE
Francisco Vargas RM560322
Matheus Eiki RM559483
Davis Júnior RM560723
Felipe Gomes RM559885


## 📋 Visão Geral

Este projeto implementa três soluções de otimização baseadas em algoritmos fundamentais da Ciência da Computação, com foco em processamento de dados de leads (contatos) e agendamento inteligente. Cada tarefa explora um conceito chave: **recursão**, **memoização** e **estruturas de dados eficientes**.

---

## 🎯 Estrutura do Projeto

### 1️⃣ **`lead.py`** - Modelo de Dados

Define a classe `Lead`, uma estrutura básica para representar um contato com informações essenciais.

```python
class Lead:
    def __init__(self, nome: str, telefone: str, email: str, cpf: str):
        self.nome      = nome
        self.telefone  = telefone
        self.email     = email
        self.cpf       = cpf
```

**Atributos:**
- `nome`: Nome completo do lead
- `telefone`: Número de contato
- `email`: Endereço de e-mail
- `cpf`: CPF do lead (identificador único)

**Método:**
- `__repr__()`: Representação em string do objeto para debug

---

## 📌 Tarefa 1: Verificação Recursiva de Duplicidade

**Arquivo:** `tarefa1_verificacao_recursiva.py`

### Conceito: Recursão

A recursão é uma técnica onde uma função chama a si mesma com um subproblema menor até atingir um caso base.

### 🔧 Funcionamento

#### **Pesos de Similaridade**

Cada campo possui um peso que define sua importância na detecção de duplicatas:

```python
PESOS = {
    "cpf":      1.0,  # Indica duplicata certa
    "email":    0.8,  # Alto grau de confiança
    "telefone": 0.6,  # Médio grau de confiança
    "nome":     0.4,  # Baixo grau de confiança
}
```

**Limiar de Duplicidade:** `0.8` (score mínimo para considerar duplicata)

#### **Função `calcular_score()`**

Compara dois leads e retorna um score de similaridade:

- ✅ CPF idêntico → +1.0 pontos
- ✅ Email idêntico → +0.8 pontos
- ✅ Telefone idêntico → +0.6 pontos
- ✅ Nome idêntico (case-insensitive) → +0.4 pontos

```python
def calcular_score(novo_lead: Lead, cadastro: Lead) -> float:
    score = 0.0
    if novo_lead.cpf == cadastro.cpf:
        score += PESOS["cpf"]
    # ... outras comparações
    return score
```

#### **Função `verificar_duplicidade()` - Recursiva**

Percorre a lista de cadastros recursivamente:

1. **Caso Base:** Se `indice >= len(cadastros)`, retorna `(False, None)`
2. **Comparação:** Calcula o score do lead atual
3. **Decisão:** Se score ≥ limiar, retorna `(True, cadastro_duplicado)`
4. **Recursão:** Chama a si mesma para o próximo índice

```python
def verificar_duplicidade(novo_lead: Lead, cadastros: list, indice: int = 0) -> tuple:
    if indice >= len(cadastros):  # Caso base
        return False, None
    
    cadastro_atual = cadastros[indice]
    score = calcular_score(novo_lead, cadastro_atual)
    
    if score >= LIMIAR_DUPLICIDADE:  # Duplicata encontrada
        return True, cadastro_atual
    
    return verificar_duplicidade(novo_lead, cadastros, indice + 1)  # Recursão
```

**Complexidade:**
- Tempo: **O(n)** - percorre cada cadastro uma vez
- Espaço: **O(n)** - pilha de recursão

### 📊 Exemplo de Uso

```
Verificando duplicidade para: Lead(nome=Francisco Vargas, cpf=333.333.333-33)

Comparando com Lead(nome=Felipe Molinari, cpf=222.222.222-22) → score: 0.00
Comparando com Lead(nome=Matheus Eiki, cpf=111.111.111-11) → score: 0.00
Comparando com Lead(nome=Francisco Vargas, cpf=323.312.223-13) → score: 0.40
Comparando com Lead(nome=Davis Junior, cpf=333.333.333-33) → score: 1.00

✗ Lead duplicado encontrado: Lead(nome=Davis Junior, cpf=333.333.333-33)
```

---

## 💾 Tarefa 2: Verificação com Memoização

**Arquivo:** `tarefa2_memoizacao.py`

### Conceito: Memoização (Programação Dinâmica)

Memoização é uma técnica que **armazena resultados de subproblemas já resolvidos** para evitar recomputação. É implementada através de uma **hash table (dicionário)**.

### 🔧 Funcionamento

#### **Cache de Comparações**

Uma hash table centraliza as comparações já realizadas:

```python
_cache_comparacoes: dict = {}
# Chave: (cpf_novo, cpf_cadastro)
# Valor: score da comparação
```

#### **Função `verificar_com_memoizacao()`**

Similar à tarefa anterior, mas com otimização:

1. **Gera chave única:** `(novo_lead.cpf, cadastro_atual.cpf)`
2. **Verifica cache:**
   - 🎯 **CACHE HIT:** Encontrou resultado anterior → retorna imediatamente
   - ❌ **CACHE MISS:** Primeira vez → calcula e armazena
3. **Compara com limiar:** Se score ≥ limiar, duplicata encontrada
4. **Recursão:** Próximo cadastro

```python
def verificar_com_memoizacao(novo_lead: Lead, cadastros: list, indice: int = 0) -> tuple:
    if indice >= len(cadastros):
        return False, None
    
    cadastro_atual = cadastros[indice]
    chave_cache = (novo_lead.cpf, cadastro_atual.cpf)
    
    if chave_cache in _cache_comparacoes:  # CACHE HIT
        score = _cache_comparacoes[chave_cache]
        print(f"[CACHE HIT] {chave_cache} → score: {score:.2f}")
    else:  # CACHE MISS
        score = calcular_score(novo_lead, cadastro_atual)
        _cache_comparacoes[chave_cache] = score
        print(f"[CACHE MISS] {chave_cache} → score: {score:.2f}")
    
    if score >= LIMIAR_DUPLICIDADE:
        return True, cadastro_atual
    
    return verificar_com_memoizacao(novo_lead, cadastros, indice + 1)
```

**Benefícios:**
- ⚡ Evita recomputação de comparações
- 📊 Reduz operações redundantes
- 🎯 Ideal para cenários com muitas verificações

**Complexidade:**
- Tempo: **O(1)** para hits, **O(n)** no pior caso (primeira passagem)
- Espaço: **O(n)** para armazenar o cache

### 📊 Exemplo de Uso

```
— Primeira verificação: Lead(nome=Ana Lima, cpf=111.111.111-11)
  [CACHE MISS] ('111.111.111-11', '111.111.111-11') → score: 1.00
  [CACHE MISS] ('111.111.111-11', '222.222.222-22') → score: 0.00
  [CACHE MISS] ('111.111.111-11', '333.333.333-33') → score: 0.00

— Segunda verificação (deve usar cache): Lead(nome=Ana Lima, cpf=111.111.111-11)
  [CACHE HIT] ('111.111.111-11', '111.111.111-11') → score: 1.00
  [CACHE HIT] ('111.111.111-11', '222.222.222-22') → score: 0.00
  [CACHE HIT] ('111.111.111-11', '333.333.333-33') → score: 0.00

Cache de comparações (hash table):
  ('111.111.111-11', '111.111.111-11') → 1.00
  ('111.111.111-11', '222.222.222-22') → 0.00
  ('111.111.111-11', '333.333.333-33') → 0.00
```

---

## 📅 Tarefa 3: Otimização de Agenda

**Arquivo:** `tarefa3_agenda.py`

### Conceito: Estruturas de Dados Eficientes (Heap) + Memoização

Um **heap** é uma estrutura de dados baseada em árvore que permite operações rápidas de inserção, remoção e extração do elemento mínimo/máximo.

### 🔧 Funcionamento

#### **Estruturas de Dados**

- 📚 **Heap (min-heap):** Ordena horários disponíveis por tempo de início
- 📋 **Dict (cache):** Armazena soluções de subproblemas (memoização)

#### **Função `calcular_melhor_agenda()`**

Encaixa consultas recursivamente nos horários disponíveis:

```python
def calcular_melhor_agenda(horarios_disponiveis: tuple, consultas: tuple) -> list:
    # Caso base
    if not consultas or not horarios_disponiveis:
        return []
    
    # Memoização
    chave = (horarios_disponiveis, consultas)
    if chave in _cache_agenda:
        return _cache_agenda[chave]
    
    # Cria heap de horários
    heap_horarios = list(horarios_disponiveis)
    heapq.heapify(heap_horarios)
    
    # Extrai primeira consulta
    consulta_atual = consultas[0]
    consultas_resto = consultas[1:]
    
    # Tenta encaixar a consulta
    encaixou = False
    while heap_horarios:
        horario = heapq.heappop(heap_horarios)  # Extrai mínimo
        h_inicio, h_fim = horario
        
        if h_inicio <= inicio_consulta and h_fim >= fim_consulta:
            resultado.append({...})
            encaixou = True
            break
    
    # Recursão para próximas consultas
    horarios_restantes = tuple(sorted(heap_horarios + horarios_usados))
    resultado += calcular_melhor_agenda(horarios_restantes, consultas_resto)
    
    # Memoiza resultado
    _cache_agenda[chave] = resultado
    return resultado
```

#### **Estrutura de Dados: Consulta**

```python
(inicio_desejado, fim_desejado, prioridade, paciente)

Exemplo:
(8, 10, 1, "Carlos - Urgente")
```

#### **Lógica de Encaixe**

Para cada consulta, o algoritmo:

1. 🔍 **Busca:** Procura um horário onde `h_inicio ≤ inicio_consulta` e `h_fim ≥ fim_consulta`
2. ✅ **Encaixa:** Se encontrar, adiciona à agenda e continua
3. ❌ **Rejeita:** Se não encontrar, registra como não agendado
4. ♻️ **Recursão:** Passa para a próxima consulta

### 📊 Exemplo de Uso

```
=== Otimização de Agenda ===

  ✓ Consulta 'Carlos - Urgente' encaixada no horário 8h–10h
  ✓ Consulta 'Maria - Rotina' encaixada no horário 10h–12h
  ✓ Consulta 'João - Retorno' encaixada no horário 13h–15h
  ✗ Sem horário disponível para 'Paula - Rotina' (13h–15h)
  ✓ Consulta 'Pedro - Urgente' encaixada no horário 15h–17h

=== Agenda Final ===
  [1] Carlos - Urgente           → 8h às 10h
  [2] Maria - Rotina             → 10h às 12h
  [3] João - Retorno             → 13h às 14h
  [1] Pedro - Urgente            → 15h às 17h
```

**Complexidade:**
- Tempo: **O(n²)** no pior caso (n consultas × n horários)
- Espaço: **O(n)** para heap + cache

---

## 🚀 Como Executar

### Requisitos
- Python 3.7+
- Nenhuma dependência externa

### Executar cada tarefa

```bash
# Tarefa 1: Verificação Recursiva
python tarefa1_verificacao_recursiva.py

# Tarefa 2: Verificação com Memoização
python tarefa2_memoizacao.py

# Tarefa 3: Otimização de Agenda
python tarefa3_agenda.py
```

---

## 📚 Conceitos-Chave Resumidos

| Conceito | Tarefa | Descrição |
|----------|--------|-----------|
| **Recursão** | 1 | Função que chama a si mesma com subproblema menor até caso base |
| **Memoização** | 2 | Armazena resultados de subproblemas para evitar recomputação |
| **Heap** | 3 | Estrutura de árvore eficiente para acesso ao mínimo/máximo em O(log n) |
| **Hash Table** | 1, 2, 3 | Dicionário para armazenamento/acesso rápido em O(1) |
| **Programação Dinâmica** | 2, 3 | Combina memoização + recursão para otimizar problemas sobrepostos |

---

## 🎓 Aprendizados

✅ **Recursão:** Simplifique problemas grandes em subproblemas menores  
✅ **Memoização:** Armazene resultados para evitar recomputação  
✅ **Estruturas de Dados:** Escolha a estrutura certa para cada caso (heap, dict, list)  
✅ **Algoritmos Greedy:** Encaixe ótimo vs. ótimo global  
✅ **Análise de Complexidade:** Entenda trade-offs entre tempo e espaço  

---

## 📝 Licença

Este projeto é fornecido como material educacional.

---

**Autor:** Fleps031 | **Data:** 2026-04-06
