import heapq

# Cache para memoização dos subproblemas de agenda
_cache_agenda: dict = {}


def calcular_melhor_agenda(horarios_disponiveis: tuple, consultas: tuple) -> list:
    """
    Calcula recursivamente o melhor encaixe de consultas nos horários disponíveis
    usando memoização. Cada consulta tem (inicio, fim, prioridade).

    Estrutura de dados:
    - Heap (heapq) para ordenar horários disponíveis por prioridade
    - Dict como cache dos subproblemas já resolvidos
    """
    # Caso base
    if not consultas or not horarios_disponiveis:
        return []

    # Chave de memoização: combinação de horários + consultas restantes
    chave = (horarios_disponiveis, consultas)
    if chave in _cache_agenda:
        print(f"  [CACHE HIT] subproblema já resolvido para {len(consultas)} consultas.")
        return _cache_agenda[chave]

    # Heap de horários disponíveis ordenados pelo início
    heap_horarios = list(horarios_disponiveis)
    heapq.heapify(heap_horarios)

    consulta_atual   = consultas[0]   # (inicio, fim, prioridade, paciente)
    consultas_resto  = consultas[1:]

    inicio_consulta = consulta_atual[0]
    fim_consulta    = consulta_atual[1]
    prioridade      = consulta_atual[2]
    paciente        = consulta_atual[3]

    encaixou        = False
    horarios_usados = []
    resultado       = []

    # Tenta encaixar a consulta em algum horário disponível
    while heap_horarios:
        horario = heapq.heappop(heap_horarios)  # pega o menor horário disponível
        h_inicio, h_fim = horario

        if h_inicio <= inicio_consulta and h_fim >= fim_consulta:
            print(f"  ✓ Consulta '{paciente}' encaixada no horário {h_inicio}h–{h_fim}h")
            resultado.append({
                "paciente":  paciente,
                "inicio":    inicio_consulta,
                "fim":       fim_consulta,
                "prioridade": prioridade,
                "horario":   horario,
            })
            encaixou = True
            break
        else:
            horarios_usados.append(horario)  # devolve horários não usados

    if not encaixou:
        print(f"  ✗ Sem horário disponível para '{paciente}' ({inicio_consulta}h–{fim_consulta}h)")

    # Reconstrói heap com horários restantes e os que não foram usados
    horarios_restantes = tuple(sorted(heap_horarios + horarios_usados))

    # Chamada recursiva para as próximas consultas (subproblema menor)
    resultado += calcular_melhor_agenda(horarios_restantes, consultas_resto)

    # Armazena resultado no cache
    _cache_agenda[chave] = resultado
    return resultado


# ------- Exemplo de uso -------

# Horários disponíveis do médico: (inicio, fim)
horarios_disponiveis = tuple(sorted([
    (8,  10),
    (10, 12),
    (13, 15),
    (15, 17),
]))

# Consultas: (inicio_desejado, fim_desejado, prioridade, paciente)
# Prioridade: quanto menor o número, maior a prioridade
consultas = (
    (8,  10, 1, "Carlos - Urgente"),
    (10, 12, 2, "Maria - Rotina"),
    (13, 14, 3, "João - Retorno"),
    (13, 15, 2, "Paula - Rotina"),   # conflito com João
    (15, 17, 1, "Pedro - Urgente"),
)

print("=== Otimização de Agenda ===\n")
agenda_final = calcular_melhor_agenda(horarios_disponiveis, consultas)

print("\n=== Agenda Final ===")
for consulta in agenda_final:
    print(f"  [{consulta['prioridade']}] {consulta['paciente']:25} "
          f"→ {consulta['inicio']}h às {consulta['fim']}h")