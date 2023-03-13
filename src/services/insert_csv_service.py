import csv
from dataclasses import dataclass
from src.infra.dynamodb_config import dynamodb_client
import datetime

table_name = "user"

@dataclass
class InsertUserService:
    @staticmethod
    def execute(data:list):
        records = csv.DictReader(data)
        
        cont = 0
        for eachRecord in records:
            cont+=1
            nome = eachRecord["NOME"]
            nascimento = eachRecord["NASCIMENTO"]
            cpf = eachRecord["CPF"]
            cnpj = eachRecord["CNPJ"]

            cpf, cnpj = InsertUserService.remove_mask(cpf, cnpj)
            nascimento = InsertUserService.format_date(nascimento)

            response = dynamodb_client.put_item(
                TableName=table_name,
                Item={
                    "id": {"S": f"{cont}"},
                    "NOME": {"S": nome},
                    "NASCIMENTO": {"S": nascimento},
                    "CPF": {"N": cpf},
                    "CNPJ": {"N": cnpj},
                },
            )
        return response

    @staticmethod
    def format_date(nascimento):
        nascimento = datetime.datetime.strptime(nascimento, "%d/%m/%Y").strftime("%Y-%m-%d")
        return nascimento

    @staticmethod
    def remove_mask(cpf, cnpj):
        if '.' or '-' in cpf:
            cpf = cpf.replace('.', '')
            cpf = cpf.replace('-', '')

        if '.' or '-' or '/' in cnpj:
            cnpj = cnpj.replace('.', '')
            cnpj = cnpj.replace('-', '')
            cnpj = cnpj.replace('/', '')
        return cpf, cnpj
            
