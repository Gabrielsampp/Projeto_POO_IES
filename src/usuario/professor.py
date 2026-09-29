from usuario.usuario import Usuario
from papeis.criador import Criador 
from papeis.participante import Participante
 
class Professor(Usuario,Criador,Participante):
    "Define o professor"
    pass