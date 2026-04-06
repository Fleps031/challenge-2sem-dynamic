from lead import Lead
from tarefa1_verificacao_recursiva import calcular_score, LIMIAR_DUPLICIDADE

# Hash table de comparações já realizadas: chave = (cpf_novo, cpf_cadastro)
_cache_comparacoes: dict = {}


def verificar_com_memoizacao(novo_lead: Lead, cadastros: list, indice: int = 0) -> tuple:
    """
    Verifica duplicidade com memoização.
    Evita recomparar pares de leads já analisados usando um dicionário como hash table.
    """
    if indice >= len(cadastros):
        return False, None

    cadastro_atual = cadastros[indice]
    chave_cache    = (novo_lead.cpf, cadastro_atual.cpf)  # chave única do par

    # Verifica se a comparação já foi feita (hit no cache)
    if chave_cache in _cache_comparacoes:
        score = _cache_comparacoes[chave_cache]
        print(f"  [CACHE HIT] {chave_cache} → score: {score:.2f}")
    else:
        score = calcular_score(novo_lead, cadastro_atual)
        _cache_comparacoes[chave_cache] = score  # armazena no hash
        print(f"  [CACHE MISS] {chave_cache} → score: {score:.2f}")

    if score >= LIMIAR_DUPLICIDADE:
        return True, cadastro_atual

    return verificar_com_memoizacao(novo_lead, cadastros, indice + 1)


def exibir_cache():
    print("\nCache de comparações (hash table):")
    for chave, score in _cache_comparacoes.items():
        print(f"  {chave} → {score:.2f}")


# ------- Exemplo de uso -------
cadastros = [
    Lead("Ana Lima",    "11999990001", "ana@email.com",   "111.111.111-11"),
    Lead("Bruno Costa", "11999990002", "bruno@email.com", "222.222.222-22"),
    Lead("Carla Dias",  "11999990003", "carla@email.com", "333.333.333-33"),
]

lead_a = Lead("Ana Lima", "11999990001", "ana_novo@email.com", "111.111.111-11")
lead_b = Lead("Ana Lima", "11999990001", "ana_novo@email.com", "111.111.111-11")  # mesmo lead

print(f"\n— Primeira verificação: {lead_a}")
verificar_com_memoizacao(lead_a, cadastros)

print(f"\n— Segunda verificação (deve usar cache): {lead_b}")
verificar_com_memoizacao(lead_b, cadastros)

exibir_cache()