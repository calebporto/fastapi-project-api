from models.basemodels import Expense_List, Finance_Values, Offer_List, Standard_Output, Tithe_List
from models.tables.client import Expenses, Tithe, User, User_Data, Waiting_Approval, Offers, Finance
from datetime import date, timedelta, datetime
from models.connection import async_session
from sqlalchemy import delete, and_, or_
from providers.hash_provider import *
from sqlalchemy.future import select
from typing import List

class UserService:
    async def user_email_exists(email: str): # Consultar se email fornecido já existe nos Users
        async with async_session() as session:
            result = await session.execute(select(User).where(User.email==email))
            return result.scalars().all()

    async def user_register(input_object): # Registrar na tabela User
        async with async_session() as session:
            session.add(User(input_object.name, input_object.email, input_object.hash, is_admin=input_object.is_admin, is_designer=input_object.is_designer))
            await session.commit()

    async def user_data_register(user_id, input_object): # Registrar na tabela User_Data
        async with async_session() as session:
            session.add(User_Data(user_id, input_object.cep, input_object.address, input_object.gender, input_object.tel, input_object.birth, input_object.added))
            await session.commit()

    async def get_user(input_object): # Consultar dados de login, e retornar dados do usuário caso inputs sejam válidos
        async with async_session() as session:
            result = await session.execute(select(User).filter(or_(User.email==input_object.email, User.id==input_object.id)))
            return result.scalars().first()

    async def get_user_id(email: str): # Pegar o id do usuário recém cadastrado
        async with async_session() as session:
            result = await session.execute(select(User.id).where(User.email==email))
            return result.scalars().first()

    async def get_user_with_data(id): # Pegar o usuário com os dados completos
        async with async_session() as session:
            user_result = await session.execute(select(User).where(User.id==id))
            user_data_result = await session.execute(select(User_Data).where(User_Data.user_id==id))
            user = user_result.scalars().first()
            user_data = user_data_result.scalars().first()
            return user, user_data

    async def user_list(): # Lista de usuários cadastrados
        async with async_session() as session:
            result = await session.execute(select(User))
            return result.scalars().all()

    async def user_update(new_user): # Altera dados do usuário
        async with async_session() as session:
            query = await session.execute(
                select(User, User_Data)
                .join(User_Data, User.id == User_Data.user_id)
                .where(User.id==new_user.id))
            
            query_result = query.all()
            if len(query_result) > 0:
                userlist = query_result[0]
            
                user = userlist[0]
                user_data = userlist[1]

                user.name = new_user.name if new_user.name else user.name
                user.email = new_user.email if new_user.email else user.email
                user.hash = new_user.hash if new_user.hash else user.hash
                user.is_admin = new_user.is_admin if new_user.is_admin else user.is_admin
                user.is_designer = new_user.is_designer if new_user.is_designer else user.is_designer
                user_data.cep = new_user.cep if new_user.cep else user_data.cep
                user_data.address = new_user.address if new_user.address else user_data.address
                user_data.gender = new_user.gender if new_user.gender else user_data.gender
                user_data.tel = new_user.tel if new_user.tel else user_data.tel
                user_data.birth = new_user.birth if new_user.birth else user_data.birth
                user_data.added = new_user.added if new_user.added else user_data.added

                session.add(user)
                session.add(user_data)
                await session.commit()

                return True
            return False

    async def delete_user(user_id: int): # Deletar usuário (Falta incluir a exclusão da tabela de dízimos, etc)
        async with async_session() as session:
            await session.execute(delete(User_Data).where(User_Data.user_id==user_id))
            await session.execute(delete(User).where(User.id==user_id))
            await session.commit()

class WaitingService:
    async def send_user(input_object): # Enviar usuário para a fila de análise
        async with async_session() as session:
            session.add(Waiting_Approval(input_object.name, input_object.email, input_object.hash, input_object.cep, input_object.address, input_object.gender, input_object.tel, input_object.birth))
            await session.commit()

    async def waiting_email_exists(email: str): # Consultar se email fornecido já existe na fila de espera
        async with async_session() as session:
            result = await session.execute(select(Waiting_Approval).where(Waiting_Approval.email==email))
            return result.scalars().all()

    async def waiting_list(): # Lista de espera completa
        async with async_session() as session:
            result = await session.execute(select(Waiting_Approval))
            return result.scalars().all()

    async def delete_of_waiting_list(id: int): # Rejeitar usuário da fila de espera
        async with async_session() as session:
            await session.execute(delete(Waiting_Approval).where(Waiting_Approval.id==id))
            await session.commit()

class TitheService:
    async def tithe_register(object_input): # registrar dízimo
            async with async_session() as session:
                for objeto in object_input:
                    session.add(Tithe(objeto.user_id, objeto.value, objeto.tithe_date, objeto.treasurer_id))
                await session.commit()

    async def tithe_list_client(user_id): # Histórico de dízimos para o cliente
        async with async_session() as session:
            result = await session.execute(select(Tithe, User)
                .join(Tithe, User.id == Tithe.user_id)
                .filter(and_((Tithe.date >= date.today() - timedelta(365)), (Tithe.user_id == user_id))))
            datalist_tuples = result.all()
            datalist = []
            
            for item in datalist_tuples:
                data = Tithe_List(
                    id=item[0].id, 
                    user_id=item[0].user_id, 
                    value=item[0].value, 
                    tithe_date=item[0].date, 
                    treasurer=item[1].name)
                datalist.append(data)
            return datalist
            

    async def tithe_list(time, user_id): # Histórico de dízimos por usuário e tempo para o admin
        async with async_session() as session:
            if time > 365 or time < 0:
                time = 365
            if user_id == -1:
                result = await session.execute(select(Tithe, User)
                .join(Tithe, User.id == Tithe.user_id)
                .filter(Tithe.date >= date.today() - timedelta(time)))
            else:
                result = await session.execute(select(Tithe, User)
                .join(Tithe, User.id == Tithe.user_id)
                .filter(and_((Tithe.date >= date.today() - timedelta(time)), (Tithe.user_id == user_id))))
            datalist_tuples = result.all()
            datalist = []
            for item in datalist_tuples:
                data = Tithe_List(
                    id=item[0].id, 
                    user_id=item[0].user_id, 
                    value=item[0].value, 
                    tithe_date=item[0].date, 
                    username=item[1].name)
                datalist.append(data)
            return datalist

class ExpensesService:
    async def expense_register(object_input): # registrar dízimo
        async with async_session() as session:
            session.add(Expenses(object_input.value, object_input.description, object_input.expense_date, object_input.treasurer_id))
            await session.commit()
            return Standard_Output(confirm=True)

    async def expense_list(start, end): # Lista de despesas em determinado período
        async with async_session() as session:
            if start > end:
                temp = start
                start = end
                end = temp
            if end - start > timedelta(365):
                start = end - timedelta(365)
            result = await session.execute(select(Expenses).filter(and_((Expenses.date >= start), (Expenses.date <= end))))
            expense_list_objects = result.scalars().all()
            expense_list = []
            for i, item in enumerate(expense_list_objects):
                data = Expense_List(
                    id = item.id, 
                    value = item.value, 
                    description = item.description, 
                    expense_date = item.date, 
                    treasurer_id = item.treasurer_id
                )
                expense_list.append(data)
            return expense_list

class OfferService:
    async def offer_include(object_input): # inclui registro na tabela de ofertas
        async with async_session() as session:
            for objeto in object_input:
                session.add(Offers(objeto.value, objeto.offer_date, objeto.treasurer_id))
            await session.commit()
            return Standard_Output(confirm=True)

    async def offer_list(start, end): # Lista de ofertas em determinado período
        async with async_session() as session:
            if start > end:
                temp = start
                start = end
                end = temp
            if end - start > timedelta(365):
                start = end - timedelta(365)
            result = await session.execute(select(Offers).filter(and_((Offers.date >= start), (Offers.date <= end))))
            offer_list_objects = result.scalars().all()
            offer_list = []
            for item in offer_list_objects:
                data = Offer_List(
                    id = item.id, 
                    value = item.value, 
                    offer_date = item.date,
                    treasurer_id = item.treasurer_id
                )
                offer_list.append(data)
            return offer_list

class FinanceService:
    async def finance_values(start, end): # Obtém dados de entradas e saídas para cálculo
        async with async_session() as session:
            offer_query = await session.execute(select(Offers.value).filter(and_(Offers.date >= start, Offers.date <= end)))
            tithe_query = await session.execute(select(Tithe.value).filter(and_(Tithe.date >= start, Tithe.date <= end)))
            expense_query = await session.execute(select(Expenses.value).filter(and_(Expenses.date >=start, Expenses.date <= end)))
            
            previous_end = start - timedelta(1)
            previous_balance = await session.execute(select(Finance.total_balance).filter(Finance.end == previous_end))

            return Finance_Values(
                offers=offer_query.scalars().all(),
                tithes=tithe_query.scalars().all(),
                expenses=expense_query.scalars().all(),
                previous_balance=previous_balance.scalars().all()
            )

    async def finance_include(object_input): # inclui registro na tabela de relatório mensal
        async with async_session() as session:
            session.add(Finance(object_input.entry, object_input.issues, object_input.start, object_input.end, object_input.period_balance, object_input.total_balance))
            await session.commit()
            return Standard_Output(confirm=True)

    async def finance_list(start, end): # Lista de ofertas em determinado período
        async with async_session() as session:
            if start > end:
                temp = start
                start = end
                end = temp
            if end - start > timedelta(365):
                start = end - timedelta(365)
            result = await session.execute(select(Finance).filter(and_((Finance.start >= start), (Finance.start <= end))))
            return result.scalars().all()