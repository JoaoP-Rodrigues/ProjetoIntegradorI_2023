import sqlite3
import sqlalchemy
#from pycep_correios import get_address_from_cep, WebService, exceptions
import pycep_correios

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
    def check_cpf_db(cpf_user, cursor):
        query = f'SELECT CPF FROM INSCRICOES WHERE CPF = "{cpf_user}"'
        cursor.execute(query)
        resultado = cursor.fetchall()
        if len(resultado) != 0:
            return True
        else:
            return False


    @staticmethod
    def valida_cep(cep):
        try:
            address = pycep_correios.get_address_from_cep('37503-130', webservice=pycep_correios.WebService.APICEP)
            cidade = address['cidade']
            if cidade.upper() == 'VALINHOS':
                return True
            else:
                return False

        except pycep_correios.exceptions.InvalidCEP as eic:
            print(eic)

        except pycep_correios.exceptions.CEPNotFound as ecnf:
            print(ecnf)

        except pycep_correios.exceptions.ConnectionError as errc:
            print(errc)

        except pycep_correios.exceptions.Timeout as errt:
            print(errt)

        except pycep_correios.exceptions.HTTPError as errh:
            print(errh)

        except pycep_correios.exceptions.BaseException as e:
            print(e)

