class Lead:
    def __init__(self, nome: str, telefone: str, email: str, cpf: str):
        self.nome      = nome
        self.telefone  = telefone
        self.email     = email
        self.cpf       = cpf

    def __repr__(self):
        return f"Lead(nome={self.nome}, cpf={self.cpf})"