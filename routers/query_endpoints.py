from services import UserService, WaitingService, TitheService, OfferService, FinanceService, ExpensesService
from fastapi import HTTPException
from models.basemodels import *
from fastapi import APIRouter
from typing import List


router = APIRouter()

@router.get('/')
async def main():
    return {'api_name': 'ibvg_api'}

@router.post('/send-user', response_model=Standard_Output)
async def send_user(new_user: New_User):
    """Recebe os dados do novo usuário. Caso não haja usuário com o mesmo e-mail ou na fila de espera, 
    registra os dados na fila de espera e retorna True.
    Caso já exista usuário com esse e-mail, retorna False"""
    
    try:
        # Consultar se já tem e-mail registrado em User ou na fila de espera
        query_user = await UserService.user_email_exists(new_user.email)
        query_waiting = await WaitingService.waiting_email_exists(new_user.email)
        if len(query_user) > 0 or len(query_waiting) > 0:
            return Standard_Output(confirm=False)

        # Registrar na tabela Waiting_Approval
        await WaitingService.send_user(new_user)

        return Standard_Output(confirm=True)
    
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.delete('/reject-waiting-user/{waiting_id}', response_model=Standard_Output)
async def delete_waiting(waiting_id: int):
    """Deleta registro da lista de espera"""
    try:
        await WaitingService.delete_of_waiting_list(waiting_id)
        return Standard_Output(confirm=True)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.get('/waiting-list', response_model=List[Waiting_User])
async def waiting_list():
    """Retorna a lista de espera"""
    try:
        return await WaitingService.waiting_list()
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.get('/user-list', response_model=List[User_List])
async def user_list():
    """Retorna a lista de todos os usuários cadastrados"""
    try:
        return await UserService.user_list()
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.post('/get-user', response_model=User_Data)
async def get_user(request_data: Get_User):
    return await UserService.get_user(request_data)

@router.get('/get-user-with-data/{id}', response_model=Waiting_User)
async def get_user_with_data(id: int):
    user, user_data = await UserService.get_user_with_data(id)
    return Waiting_User(
        id=user.id,
        name=user.name,
        email=user.email,
        hash=user.hash,
        cep=user_data.cep,
        address=user_data.address,
        gender=user_data.gender,
        tel=user_data.tel,
        birth=user_data.birth,
        added=user_data.added
    )

@router.post('/add-user', response_model=Standard_Output)
async def add_user(user: Add_User, user_data: Add_User_Data):
    """ Recebe os dados do usuário da lista de espera a ser registrado na lista definitiva
        Obs: user_to_del deve ser o id do usuário aprovado da lista de espera. """
    try:
        # Registrando User
        await UserService.user_register(user)

        # Pegando o id do User recem registrado
        user_id = await UserService.get_user_id(user.email)

        # Registrando User_Data
        await UserService.user_data_register(user_id, user_data)

        # Deletando id da fila de espera
        if user.user_to_del:
            await WaitingService.delete_of_waiting_list(user.user_to_del)

        return Standard_Output(confirm=True, message='ok')

    except Exception as error:
        return HTTPException(400, detail=str(error))

@router.post('/user-update')
async def user_update(new_user: User_Upgrade):
    """Altera dados do usuário"""
    return Standard_Output(confirm=await UserService.user_update(new_user))

@router.delete('/delete-user/{user_id}', response_model=Standard_Output)
async def delete_user(user_id: int):
    """Deleta usuário cadastrado"""
    # Falta configurar a exclusão dos dados das outras tabelas e testar
    try:
        await UserService.delete_user(user_id)
        return Standard_Output(confirm=True)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.post('/tithe-include', response_model=Standard_Output)
async def tithe_include(tithe_data: List[Tithe_Register]):
    """Insere os dízimos dos membros"""
    try:
        await TitheService.tithe_register(tithe_data)
        return Standard_Output(confirm=True)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.get('/tithe-list/{time}/{user_id}/{type_user}', response_model=Tithe_List_Response)
async def tithe_list(time: int, user_id: int, type_user: int):
    """Retorna a lista de dízimos, de acordo com o intervalo de tempo fornecido e o id de usuário. 
    Caso queira obter a lista de todos os usuários, fornecer o id de usuário no valor -1. 
    O tempo padrão da busca é de 365 dias. Caso não queira esperificar tempo, deve enviar o valor -1.
    type_user especifica o tipo de resposta. Se for 1, a resposta será de acordo com o tempo e o id 
    do usuário. Se for 2, a resposta será de acordo com o id do usuário e o tempo padrão de 365 dias."""
    try:
        if type_user == 1:
            tithe_list_data = await TitheService.tithe_list(time, user_id)
            return Tithe_List_Response(tithe_list=tithe_list_data)
        elif type_user == 2:
            tithe_list_data = await TitheService.tithe_list_client(user_id)
            return Tithe_List_Response(tithe_list=tithe_list_data)
        else:
            raise HTTPException(400, detail=str('Dados Inválidos'))
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.post('/expense-include', response_model=Standard_Output)
async def expense_include(expense_data: Expense_Register):
    """Insere as saídas do caixa"""
    try:
        return await ExpensesService.expense_register(expense_data)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.get('/expense-list/{start}/{end}', response_model=List[Expense_List])
async def expense_list(start: date, end: date):
    """Retorna lista de despesas por período escolhido, não superior a umano"""
    try:
        return await ExpensesService.expense_list(start, end)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.post('/offer-include', response_model=Standard_Output)
async def offer_include(offer_data: List[Offer_Include]):
    """Adiciona à tabela de ofertas"""
    try:
        return await OfferService.offer_include(offer_data)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.get('/offer-list/{start}/{end}', response_model=List[Offer_List])
async def offer_list(start: date, end: date):
    """Retorna lista de ofertas por período escolhido, não superior a um ano"""
    try:
        return await OfferService.offer_list(start, end)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.get('/finance-values/{start}/{end}', response_model=Finance_Values)
async def finance_data(start: date, end: date):
    try:
        return await FinanceService.finance_values(start, end)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.post('/finance-include', response_model=Standard_Output)
async def finance_include(finance_data: Finance_Include):
    """Adiciona à tabela de relatórios mensais"""
    try:
        return await FinanceService.finance_include(finance_data)
    except Exception as error:
        raise HTTPException(400, detail=str(error))

@router.get('/finance-list/{start}/{end}', response_model=List[Finance_List])
async def finance_list(start: date, end: date):
    """Retorna lista de relatórios por período escolhido, não superior a um ano.
    As datas fornecidas devem sempre ser o dia primeiro do mês de referencia, pois
    a query é baseada sempre na data de início do relatório."""
    try:
        return await FinanceService.finance_list(start, end)
    except Exception as error:
        raise HTTPException(400, detail=str(error))