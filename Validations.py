import brazilcep
from Database import DataBase
import string
import pdb

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

        obj = DataBase()
        obj.create_connection()

        cpf_user = cpf_user.translate(str.maketrans('', '', string.punctuation))

        query = 'SELECT cpf FROM Inscricoes WHERE cpf = ?'''
        #pdb.set_trace()
        obj.cursor.execute(query, cpf_user)
        resultado = obj.cursor.fetchall()
        if len(resultado) != 0:
            return False
        else:
            return True


    @staticmethod
    def valida_cep(cep):

        cep = cep.translate(str.maketrans('', '', string.punctuation))
        try:
            address = brazilcep.get_address_from_cep(cep, webservice=brazilcep.WebService.APICEP)

            cidade = address['city']
            if cidade.upper() == 'VALINHOS':
                return True
            else:
                return False
        except:
            return False

    @staticmethod
    def get_user(user_mail):
        obj = DataBase()
        obj.create_connection()

        user_mail = user_mail.lower()
        query = 'SELECT email FROM usuarios WHERE email = ?'
        obj.cursor.execute(query, user_mail)
        resultado = obj.cursor.fetchall()

        if len(resultado) != 0:
            return False
        else:
            return True

