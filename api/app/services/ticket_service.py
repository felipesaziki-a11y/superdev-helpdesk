

from uuid import uuid4

from app.models.ticket import Ticket
from app.repositories.ticket_repository import TicketRepository
from app.schemas.ticket_schema import TicketCancelar, TicketCriar, TicketResolver
from app.services.usuario_service import UsuarioService
from sqlalchemy.orm import Session

from app.core.enums import Papel, StatusChamado
from app.core.tempo import agora


class TicketService:
    def __init__(self, db: Session)
        self.db = db
        self.ticket_repository = TicketRepository(db)
        self.usuario_service = UsuarioService(db)

    def __gerar_numero_protocolo(self, ticket: Ticket) -> str:
        data_criacao = ticket.data_criacao.strftime("%Y%m%d") #ANOMESDIA
        numero = str(ticket.id).zfill(6) # ticket 1 => 000001
        return f"{data_criacao}-{numero}"


    def criar(self, dado: TicketCriar) -> Ticket:
        # Validar que o usuário existe efetivamente
        usuario = self.usuario_service.obter_por_id(dado.id_usuario)
        if usuario.papel != Papel.SOLICITANTE:
            raise PermissaoNegadaError("Tickets podem ser abertos somente por SOLICITANTE")


        ticket = Ticket(
            titulo=dado.titulo,
            descricao=dado.descricao,
            setor=dado.setor,
            solicitante_id=dado.id_usuario,
            status=StatusChamado.ABERTO,
            numero_protocolo=str(uuid4())
        )
        self.ticket_repository.adicionar(ticket)
        self.db.flush()
        self.db.commit()
        return ticket

    def resolver(self, id: int, dado: TicketResolver) -> Ticket:
        ticket = self.obter_por_id(id)
        usuario = self.usuario_service(dado.id_usuario)
        if usuario.papel != Papel.ATENDENTE:
            raise PermissaoNegadaError("Somente com papel ATENDENTE pode resolver o ticket")

        if ticket.atendente_id != dado.id_usuario:
            raise PermissaoNegadaError("Somente o atendente associado pode resolver esse ticket")

        if ticket.status != StatusChamado.EM_ANALISE:
            raise RegraNegocioError("Somente tickets em análise podem ser resolvidos")

        ticket.descricao_solucao = dado.descricao
        ticket.status = StatusChamado.RESOLVIDO
        ticket.data_atualizacao = agora()

        return ticket

    def cancelar(self, id: int, dado: TicketCancelar) -> Ticket:
        ticket = self.obter_por_id(id)
        usuario = self.usuario_service.obter_por_id(dado.id_usuario)

        if ticket.status == StatusChamado.RESOLVIDO:
            raise RegraNegocioError("Tickets resolvidos não podem ser cancelados")

        if ticket.status == StatusChamado.CANCELADO:
            raise RegraNegocioError("Ticket já está cancelado")

        ticket.motivo_cancelamento = dado.motivo
        ticket.status = StatusChamado.CANCELADO
        ticket.data_atualizacao = agora()
        self.db.commit()
        return ticket