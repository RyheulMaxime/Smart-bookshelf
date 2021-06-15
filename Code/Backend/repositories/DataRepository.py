from .Database import Database


class DataRepository:
    @staticmethod
    def toevoegen_waarde(idsensor, waarde):
        sql = "INSERT INTO hystoriek (idsensor_actuator, waarde) VALUES (%s,%s)"
        params = [idsensor, waarde]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def read_status_positions():
        sql = "SELECT p.idboek, b.idbibliotheek, bi.naam as naambib, b.naam, p.idpositie, date_format(inleverdatum, '%Y-%m-%d') as inleverdatum FROM `positie boekenkast` p join boek b on p.idboek=b.idboek join bibliotheek bi on bi.idbibliotheek=b.idbibliotheek order by idpositie;"
        return Database.get_rows(sql)

    @staticmethod
    def read_info_boek(id):
        sql = "SELECT p.idboek, b.idbibliotheek, bi.naam as naambib, b.author , b.naam, p.idpositie, date_format(inleverdatum, '%Y-%m-%d') as inleverdatum FROM `positie boekenkast` p right join boek b on p.idboek=b.idboek join bibliotheek bi on bi.idbibliotheek=b.idbibliotheek where b.idboek = %s;"
        params = [id]
        return Database.get_one_row(sql, params)
    
    @staticmethod
    def read_previous_books():
        sql = "SELECT b.idboek, b.idbibliotheek, bi.naam as naambib, b.naam FROM `positie boekenkast` p right join boek b on p.idboek=b.idboek join bibliotheek bi on bi.idbibliotheek=b.idbibliotheek where p.idpositie is NULL;"
        return Database.get_rows(sql)

    @staticmethod
    def read_librarys():
        sql = "SELECT * FROM bibliotheek;"
        return Database.get_rows(sql)

    @staticmethod
    def verleng_boek_4_weken(idboek):
        sql = "UPDATE boek SET inleverdatum = date_add(inleverdatum, interval 4 week) where idboek = %s;"
        params = [idboek]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def verleng_boek(idboek,date):
        sql = "UPDATE boek SET inleverdatum = %s where idboek = %s;"
        params = [date, idboek]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def indiennen_boek(idboek):
        sql = "UPDATE `positie boekenkast` SET idboek = NULL ,  `kleur ledstrip`='white' where idboek = %s;"
        params = [idboek]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def uit_kast_nemen(idpositie):
        sql = "UPDATE `positie boekenkast` SET idboek = NULL ,  `kleur ledstrip`='white' where idpositie = %s;"
        params = [idpositie]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def indiennen_boek_RFID(idboek):
        sql = "UPDATE boek SET RFID = NULL  where idboek = %s;"
        params = [idboek]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def aanpassen_boek(naam,author, idbib, datum, idboek):
        sql = "UPDATE boek SET naam = %s ,author = %s ,idbibliotheek =%s ,inleverdatum = %s  where idboek = %s;"
        params = [naam,author, idbib, datum, idboek]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def get_info_rfid():
        sql = "SELECT idboek,rfid, date_format(inleverdatum, '%Y-%m-%d') as inleverdatum FROM boek where rfid is not null;"
        return Database.get_rows(sql)

    @staticmethod
    def get_info_positie():
        sql = "select * from `positie boekenkast`;"
        return Database.get_rows(sql)

    @staticmethod
    def set_position_book(idboek,kleur,idpositie):
        sql = "UPDATE `positie boekenkast` SET idboek = %s ,  `kleur ledstrip`=%s   where idpositie = %s ;"
        params = [idboek,kleur,idpositie]
        return Database.execute_sql(sql, params)

    @staticmethod
    def put_nieuw_book(naam,author,RFID,idbibliotheek,inleverdatum):
        sql = "INSERT INTO boek (naam,author,RFID,idbibliotheek,inleverdatum) VALUES (%s,%s,%s,%s,%s)"
        params = [naam,author,RFID,idbibliotheek,inleverdatum]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def get_id_nieuw_book(naam,author,RFID,idbibliotheek,inleverdatum):
        sql = "SELECT idboek FROM boek where naam = %s and author = %s and RFID = %s and idbibliotheek = %s and inleverdatum = %s ;"
        params = [naam,author,RFID,idbibliotheek,inleverdatum]
        return Database.get_one_row(sql, params)

    @staticmethod
    def get_info_led():
        sql = "select * from `positie boekenkast` order by idpositie desc;"
        return Database.get_rows(sql)

    @staticmethod
    def verander_kleur(idboek,kleur):
        sql = "UPDATE `positie boekenkast` SET `kleur ledstrip`=%s where idboek = %s;"
        params = [kleur, idboek]
        return Database.execute_sql(sql, params)

    @staticmethod
    def get_datum(idboek):
        sql = "SELECT  date_format(inleverdatum, '%Y-%m-%d') as inleverdatum FROM boek where idboek= %s;"
        params = [idboek]
        return Database.get_one_row(sql, params)