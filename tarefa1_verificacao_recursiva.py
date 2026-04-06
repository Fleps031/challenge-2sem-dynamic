from lead import Lead

# Pesos de similaridade por campo
PESOS = {
    "cpf":      1.0,  # CPF igual → duplicata certa
    "email":    0.8,
    "telefone": 0.6,
    "nome":     0.4,
}

LIMIAR_DUPLICIDADE = 0.8  # score mínimo para considerar duplicata


def calcular_score(novo_lead: Lead, cadastro: Lead) -> float:
    """Calcula score de similaridade entre dois leads."""
    score = 0.0

    if novo_lead.cpf       == cadastro.cpf:       score += PESOS["cpf"]
    if novo_lead.email     == cadastro.email:     score += PESOS["email"]
    if novo_lead.telefone  == cadastro.telefone:  score += PESOS["telefone"]
    if novo_lead.nome.lower() == cadastro.nome.lower(): score += PESOS["nome"]

    return score


def verificar_duplicidade(novo_lead: Lead, cadastros: list, indice: int = 0) -> tuple:
    """
    Percorre recursivamente a lista de cadastros verificando duplicidade.
    Retorna (True, cadastro_duplicado) ou (False, None).
    """
    # Caso base: percorreu todos os cadastros
    if indice >= len(cadastros):
        return False, None

    cadastro_atual = cadastros[indice]
    score = calcular_score(novo_lead, cadastro_atual)

    print(f"  Comparando com {cadastro_atual} → score: {score:.2f}")

    if score >= LIMIAR_DUPLICIDADE:
        return True, cadastro_atual

    # Chamada recursiva para o próximo cadastro
    return verificar_duplicidade(novo_lead, cadastros, indice + 1)


# ------- Exemplo de uso -------
cadastros = [
    Lead("Felipe Molinari", "11999990002", "bruno@email.com",  "222.222.222-22"),
    Lead("Matheus Eiki",    "11999990001", "ana@email.com",    "111.111.111-11"),
    Lead("Francisco Vargas",  "11999990003", "carla@email.com",  "323.312.223-13"),
    Lead("Davis Junior", "11999990003", "carla@email.com", "333.333.333-33"),

]

novo_lead = Lead("Francisco Vargas", "11999990003", "ana_novo@email.com", "333.333.333-33")

print(f"\nVerificando duplicidade para: {novo_lead}")
duplicado, encontrado = verificar_duplicidade(novo_lead, cadastros)

if duplicado:
    print(f"\n✗ Lead duplicado encontrado: {encontrado}")
else:
    print(f"\n✓ Nenhuma duplicidade encontrada.")