import sqlite3
import sqlalchemy
from pycep_correios import get_address_from_cep, WebService, exceptions
import pycep_correios
from Databases import DataBase

class Validations:

    @staticmethod
    def cpf_validate(cpfNotValidate):
        try:
            cpf = [int(char) for char in cpfNotValidate if char.isdigit()]
        except:
            return False

        if len(cpf) != 11:
            return False
        if cpf == cpf[::-1]:
            return False
        for i in range(9, 11):
            value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
            digit = ((value * 10) % 11) % 10
            if digit != cpf[i]:
                return False
        return True


    @staticmethod
    def check_cpf_db(cpf_user):
        import string
        obj = DataBase()
        obj.create_connection()

        cpf_user = cpf_user.translate(str.maketrans('', '', string.punctuation))

        query = f'SELECT CPF FROM INSCRICOES WHERE CPF = "{cpf_user}"'
        obj.cur.execute(query)
        resultado = obj.cur.fetchall()
        if len(resultado) != 0:
            return False
        else:
            return True


    @staticmethod
    def valida_cep(cep):
        import string
        cep = cep.translate(str.maketrans('', '', string.punctuation))
        try:
            address = pycep_correios.get_address_from_cep(cep, webservice=pycep_correios.WebService.APICEP)
            cidade = address['cidade']
            if cidade.upper() == 'VALINHOS':
                return True
            else:
                return False

        except pycep_correios.exceptions.InvalidCEP as eic:
            return eic

        except pycep_correios.exceptions.CEPNotFound as ecnf:
            return ecnf

        except pycep_correios.exceptions.ConnectionError as errc:
            return errc

        except pycep_correios.exceptions.Timeout as errt:
            return errt

        except pycep_correios.exceptions.HTTPError as errh:
            return errh

        except pycep_correios.exceptions.BaseException as e:
            return e

