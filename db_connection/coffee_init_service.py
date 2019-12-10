from mysql.connector import Error, errorcode

from db_connection.db_connection import ConnectionPool
from configparser import ConfigParser


class CoffeeProj:
    OPTION = """
        CHARACTER SET 'UTF8'
        FIELDS TERMINATED by ','
        LINES TERMINATED by '\r\n'
        """

    def __init__(self, source_dir='/home/pjs/PycharmProjects/coffee_proj/data/'):
        self._db = CoffeeProj.read_ddl_file()
        self.source_dir = source_dir

    @classmethod
    def read_ddl_file(cls, filename='coffee_ddl.ini'):
        parser = ConfigParser()
        parser.read(filename, encoding='UTF8')

        db = {}
        for sec in parser.sections():
            items = parser.items(sec)
            if sec == 'name':
                for key, value in items:
                    db[key] = value
            if sec == 'sql':
                sql = {}
                for key, value in items:
                    sql[key] = " ".join(value.splitlines())
                db['sql'] = sql
                print(db['sql'])
            if sec == 'user':
                for key, value in items:
                    db[key] = value

        return db

    def __create_database(self):
        try:
            sql = CoffeeProj.read_ddl_file()
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self._db['database_name']))
            print('CREATE DATABASE {}'.format(self._db['database_name']))
        except Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                cursor.execute("DROP DATABASE {}".format(self._db['database_name']))
                print('DROP DATABASE {}'.format(self._db['database_name']))
                cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self._db['database_name']))
                print('CREATE DATABASE {}'.format(self._db['database_name']))
            else:
                print(err.msg)
        finally:
            cursor.close()
            conn.close()

    def __create_table(self):
        global cursor, conn
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            cursor.execute('USE {}'.format(self._db['database_name']))
            for table_name, table_sql in self._db['sql'].items():
                try:
                    print('Creating {}:'.format(table_name), end='')
                    cursor.execute(table_sql)
                except Error as err:
                    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                        print('already exists.')
                    else:
                        print(err.msg)
                else:
                    print('ok')
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def __create_user(self):
        global cursor, conn
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            print('Creating user:', end='')
            cursor.execute(self._db['user_sql'])
            print('ok')
        except Error as err:
            print(err)
        finally:
            cursor.close()
            conn.close()

    def data_backup(self, table_name):
        filename = table_name + '.txt'
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            source_path = self.source_dir + filename  # /tmp/product.txt
            # if os.path.exists(source_path):
            #     os.chown(source_path, uid, gid)
            #     os.remove(source_path)

            backup_sql = "SELECT * FROM {} INTO OUTFILE '{}' {}".format(table_name, source_path, CoffeeProj.OPTION)
            print(backup_sql)
            cursor.execute(backup_sql)

            # if not os.path.exists(self.data_dir):
            #     os.makedirs(os.path.join('data'))
            # shutil.move(source_path, self.data_dir + '/' + filename)  # 파일이 존재하면 overwrite
            # shutil.copy(source_path, self.data_dir + '/' + filename)
            print(table_name, "backup complete!")
        except Error as err:
            print(err)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def data_restore(self, table_name):
        filename = table_name + '.txt'
        try:
            conn = ConnectionPool.get_instance().get_connection()
            cursor = conn.cursor()
            source_path = self.source_dir + filename  # /tmp/product.txt

            restore_sql = "LOAD DATA INFILE '{}' INTO TABLE {} {}".format(source_path, table_name,
                                                                              CoffeeProj.OPTION)
            print(restore_sql)
            cursor.execute(restore_sql)
            conn.commit()

            print(table_name, "restore complete!")
        except Error as err:
                print(err)
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


    def service(self):
        self.__create_database()
        self.__create_table()
        self.__create_user()