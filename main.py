import psycopg2


class Db:
    def __init__(self, database_name, user, password):
        self.conn = psycopg2.connect(database=database_name, user=user, password=password)
        self.cur = self.conn.cursor()

    def end(self):
        self.cur.close()
        self.conn.close()

    def clear_db(self):
        self.cur.execute('''
        DROP TABLE public.email;
        DROP TABLE public.telephone;
        DROP TABLE public.person;
        ''')
        self.conn.commit()

    def create_table(self):
        self.cur.execute('''CREATE TABLE public.person(
                    "id" SERIAL PRIMARY KEY, 
                    "name" VARCHAR NOT NULL, 
                    "family" VARCHAR NOT NULL);''')
        self.cur.execute('''CREATE TABLE public.email(
                    "id" SERIAL PRIMARY KEY,
                    "person_id" INTEGER NOT NULL REFERENCES public.person(id),
                    "email" VARCHAR NOT NULL);''')
        self.cur.execute('''CREATE TABLE public.telephone(
                    "id" SERIAL PRIMARY KEY,
                    "person_id" INTEGER NOT NULL REFERENCES public.person(id),
                    "phone_num" VARCHAR NOT NULL);''')
        self.conn.commit()
        print('Таблицы созданы')

    def add_new_person(self, name_person, family_person, tel_num=None, email=None):
        self.cur.execute(
            '''INSERT INTO person("name", "family")
            VALUES (%s, %s) RETURNING id''', (name_person, family_person)
        )
        id_person = self.cur.fetchone()[0]
        if tel_num:
            self.cur.execute(
                '''INSERT INTO telephone("person_id", "phone_num")
                VALUES (%s, %s)''', (id_person, tel_num)
            )
        if email:
            self.cur.execute(
                '''INSERT INTO email("person_id", "email")
                VALUES (%s, %s)''', (id_person, email)
            )
        self.conn.commit()

    def insert_phone_number(self, name_person, family_person):
        person_id = self.test_person(name_person, family_person)
        if person_id:
            id_person = person_id[0]
            print('Введите номер телефона в формате +79ххххххххх')
            tel_num = input()
            self.cur.execute(
                '''INSERT INTO telephone("person_id", "phone_num")
                VALUES (%s, %s)''', (id_person, tel_num))
            self.conn.commit()
        else:
            print('Пользователь не найден')

    def change_person(self, name_person, family_person):
        person_id = self.test_person(name_person, family_person)
        if person_id:
            print('Введите новое имя:')
            name_person = input()
            print('Введите новую фамилию:')
            family_person = input()
            self.cur.execute(
                '''UPDATE person SET "name" = %s, "family" = %s
                WHERE "id" = %s''', (name_person, family_person, person_id[0])
            )
            self.conn.commit()
        else:
            print('Пользователь не найден')

    def test_person(self, *person_info):
        self.cur.execute(
            ''' SELECT p.id FROM person p
            WHERE "name" = %s AND "family" = %s''', (person_info[0], person_info[1])
        )
        person_id = self.cur.fetchone()
        return person_id

    def del_person_telephone(self, name_person, family_person):
        person_id = self.test_person(name_person, family_person)
        if person_id:
            self.cur.execute(
                ''' SELECT t.id FROM telephone t
                WHERE t.person_id = %s''', person_id
            )
            telephone_id = self.cur.fetchall()
        else:
            print('Нет такого пользователя.')
            return
        if telephone_id:
            for number in telephone_id:
                self.cur.execute(
                    '''DELETE FROM telephone t
                    WHERE t.id = %s''', (number,)
                )
                self.conn.commit()
        else:
            print('У данного пользователя нет зарегистрированных телефонов.')

    def _del_email_person(self, person_id):
        self.cur.execute(
            ''' SELECT e.id FROM email e
            WHERE e.person_id = %s''', person_id
        )
        email_id = self.cur.fetchall()
        if email_id:
            for number in email_id:
                self.cur.execute(
                    '''DELETE FROM email e
                    WHERE e.id = %s''', (number,)
                )
                self.conn.commit()
        else:
            print('У данного пользователя нет зарегистрированных email.')

    def del_person(self, name_person, family_person):
        person_id = self.test_person(name_person, family_person)
        if person_id:
            self.del_person_telephone(name_person, family_person)
            self._del_email_person(person_id)
            self.cur.execute(
                '''DELETE FROM person p 
                WHERE p.id=%s''', (person_id,)
            )
        else:
            print('Нет такого пользователя')

    def __search_person_id(self, person_id):
        pass

    def search_name(self, name):
        self.cur.execute(
            '''SELECT p.id
            FROM person p
            WHERE p.name = %s''', (name,)
        )
        self.__search_person_id(self.cur.fetchall())

    def search_family(self, family):
        self.cur.execute(
            '''SELECT p.id
            FROM person p
            WHERE p.family = %s''', (family,)
        )
        self.__search_person_id(self.cur.fetchall())

    def search_email(self, email):
        self.cur.execute(
            ''' SELECT e.personal_id
            FROM email e
            WHERE e.email = %s
            ''', (email,)
        )
        self.__search_person_id(self.cur.fetchall())

    def search_telephone(self, tel_num):
        self.cur.execute(
            ''' SELECT t.personal_id
            FROM telephone t
            WHERE t.phone_num = %s
            ''', (tel_num,)
        )
        self.__search_person_id(self.cur.fetchall())

    def __print_result(self, result):
        if result:
            for res in result:
                print(f'Найдены пользователи: {res[0]} {res[1]}')
        else:
            print('Нет таких пользователей')


def text_menu():
    print('-' * 20)
    lst_menu = ("Что бы добавить нового пользователя нажмите 1.",
                "Что бы добавить телефон к пользователю нажмите 2.",
                "Что бы изменить данные о пользователе нажмите 3.",
                "Что бы удалить телефон у пользователя нажмите 4.",
                "Чnо бы удалить пользователя нажмите 5.",
                "Поиск клиента по базе нажмите 6.",
                "Что бы прекратить нажмите 0.")
    for text in lst_menu:
        print(text)


def name_family() -> list:
    person_info = []
    print('Введите имя пользователя.')
    person_info.append(input())
    print('Введите фамилию пользователя')
    person_info.append(input())
    return person_info


def menu(db):
    while True:
        text_menu()
        command = input()
        person_info = []
        if command == '1':
            person_info = name_family()
            print('Если хотите добавить номер телефона нажмите 1')
            command1 = input()
            if command1 == '1':
                print('Введите номер телефона в формате +79ххххххххх')
                person_info.append(input())
            else:
                print('Ввод номера телефона пропущен.')
            print('Если хотите добавить email нажмите 1')
            command2 = input()
            if command2 == '1':
                print('Введите email')
                person_info.append(input())
            else:
                print('Ввод email пропущен.')
            db.add_new_person(*person_info)
        elif command == '2':
            person_info = name_family()
            db.insert_phone_number(*person_info)
        elif command == '3':
            person_info = name_family()
            db.change_person(*person_info)
        elif command == '4':
            person_info = name_family()
            db.del_person_telephone(*person_info)
        elif command == '5':
            person_info = name_family()
            db.del_person(*person_info)
        elif command == '6':
            print('По какому параметру будем искать пользователя?\n1.Имя\n2.Фамилия\n3.Email\n4.Номер телефона')
            command3 = input()
            if command3 == '1':
                db.search_name(input('Введите имя: '))
            elif command3 == '2':
                db.search_family(input('Ведите фамилию: '))
            elif command3 == '3':
                db.search_email(input('Введите email: '))
            elif command3 == '4':
                db.search_telephone(input('Введите номер телефона'))
            else:
                print('Неизвестная команда')
        elif command == '0':
            db.end()
            break
        else:
            print('Неизвестная команда.')


def main():
    print('Введите название базы данных:')
    database_name = 'netology_db'
    #   database_name = input()
    print('Введите имя пользователя:')
    user = 'postgres'
    #   user = input()
    print('Введите пароль от базы данных:')
    password = '24081986'
    #   password = input()

    db_connect = Db(database_name, user, password)
    # db_connect.clear_db()
    # db_nnect.create_table()
    menu(db_connect)


if __name__ == '__main__':
    main()
