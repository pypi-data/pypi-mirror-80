import psycopg2


class Database:
    """
    Classe per la connessione un database SQL e le successive interrogazioni verso lo stesso
    """

    __database_cursor = None            # cursore del database da utilizzare per le query

    # connessione al database da utilizzare nel caso di commit manuale
    __database_connection = None
    
    __ISOLATION_LEVELS = {
        'AUTOCOMMIT': psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT, 
        'READ UNCOMMITTED': psycopg2.extensions.ISOLATION_LEVEL_READ_UNCOMMITTED,
        'READ COMMITTED': psycopg2.extensions.ISOLATION_LEVEL_READ_COMMITTED,
        'REPEATABLE READ': psycopg2.extensions.ISOLATION_LEVEL_REPEATABLE_READ,
        'SERIALIZABLE': psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE,
        'DEFAULT': psycopg2.extensions.ISOLATION_LEVEL_DEFAULT
    }

    def __init__(self, host, port, database, user, password, autocommit=True, isolation_level=None, readonly=None):
        """
        Inizializza la connessione con il database SQL
        :param host:            indirizzo dell'host del database
        :param port:            porta di connessione del database
        :param database:        nome del database al quale ci si vuole connettere
        :param user:            utente con cui connettersi e autenticarsi
        :param password:        password dell'utente specificato
        :param autocommit:      passa alla modalità autocommit, ogni comando ha effetto immediatamente
        :throw Connection:      se la connessione non ha avuto successo     
        :throw TypeError:       se un argomento passato non ha il tipo corretto        
        """
        try:
            # apro la connessione ed ottengo il cursore
            db_connection = psycopg2.connect(port=port, host=host, dbname=database, user=user, password=password)

            # inizializzo lo stato interno dell'oggetto
            self.__database_connection = db_connection

            self.set_session(autocommit=autocommit, isolation_level=isolation_level, readonly=readonly)

            self.__database_cursor = db_connection.cursor()

        except (Exception, psycopg2.Error) as error:
            # nel caso ci siano problemi con la connessione sollevo un'eccezione
            raise ConnectionError('Exception connetcting to Database: {}:{}. Exception: {}.'.format(host, port, error)) from error

    def set_session(self, autocommit=None, isolation_level=None, readonly=None, deferrable=None):
        """
        Funzione per la modifica della sessione, ha effetto dalla prossima transazione
        I parametri a None non vengono modificati
        :param autocommit:              se a True, ogni comando eseguito ha effetto immediatamente. Se a False si devono usare rollback e commit
        :param isolation_level:         indica l'isolation level delle transizioni 'READ UNCOMMITTED', 'READ COMMITTED', 'REPEATABLE READ', 'SERIALIZABLE', 'DEFAULT'
        :param readonly:                indica se le transizioni devono essere read-only
        :param deferrable:              imposta la deferrable mode
        :throw TypeError:               se un argomento passato non ha il tipo corretto
        """
        # controllo i tipi degli argomenti passati
        if autocommit is not None and not isinstance(autocommit, bool):
            raise TypeError('Autocommit must be None or boolean.')

        if isolation_level is not None and isolation_level not in self.__ISOLATION_LEVELS:
            raise TypeError('Isolation level must be None or one of [{}]'.format(','.join(list(self.__ISOLATION_LEVELS.keys()))))

        isolation_level = self.__ISOLATION_LEVELS.get(isolation_level)

        if readonly is not None and not isinstance(readonly, bool):
            raise TypeError('Readonly must be None or boolean.')

        if deferrable is not None and not isinstance(deferrable, bool):
            raise TypeError('Deferrable must be None or boolean.')

        self.__database_connection.set_session(autocommit=autocommit, isolation_level=isolation_level, readonly=readonly, deferrable=deferrable)

    def query_first(self, query, params=None, return_n_of_rows=False):
        """
        Esegue la query <query> con parametri <params> sul database e ritorna al massimo una entry
        I placeholders nella query hanno formato %(placeholder)s
        :param query:                   stringa contenente la query da eseguire
        :param params:                  placeholder da sostituire
        :param return_n_of_rows:        flag che indica se deve essere ritornato il numero di rige coinvolte dalla query
        :throw SyntaxError:             se ci sono problemi con il formato della query o dei parametri
        :throw ConnectionError:         se ci sono problemi di comunicazione con il database

        :return:                        - risultato della query (solo una entry) se return_n_of_rows == False
                                        - risultato della query (solo una entry) e numero di entries coinvolte se return_n_of_rows == True        
        """
        try:
            params = {} if params is None else params
            # eseguo la query e restituisco solo il primo risultato
            self.__database_cursor.execute(query, params)

            if return_n_of_rows:
                return self.__database_cursor.fetchone(), self.__database_cursor.rowcount
            else:
                return self.__database_cursor.fetchone()

        except (psycopg2.errors.SyntaxError, ValueError, TypeError, KeyError, psycopg2.errors.InvalidTextRepresentation) as error:
            raise SyntaxError('Something is wrong with the query requested "{}" with params: "{}". Exception: {}.'.format(query, params, error))
        except (Exception, psycopg2.Error) as error:
            # qualcosa è andato storto nella query, sollevo un'eccezione
            raise ConnectionError('Exception while executing query "{}" with params "{}". Exception: {}.'.format(query, params, error)) from error

    def query_all(self, query, params=None, return_n_of_rows=False):
        """
        Esegue la query <query> con parametri <params> sul database e ritorna tutte le entries
        I placeholders nella query hanno formato %(placeholder)s
        :param query:                   stringa contenente la query da eseguire
        :param params:                  placeholder da sostituire
        :param return_n_of_rows:        flag che indica se deve essere ritornato il numero di rige coinvolte dalla query
        :throw SyntaxError:             se ci sono problemi con il formato della query o dei parametri
        :throw ConnectionError:         se ci sono problemi di comunicazione con il database

        :return:                        - risultato della query (tutte le entries) se return_n_of_rows == False
                                        - risultato della query (tutte le entries) e numero di entries coinvolte se return_n_of_rows == True
        """

        try:
            params = {} if params is None else params
            # eseguo la query e restituisco tutti i risultati
            self.__database_cursor.execute(query, params)

            if return_n_of_rows:
                return self.__database_cursor.fetchall(), self.__database_cursor.rowcount
            else:
                return self.__database_cursor.fetchall()

        except (psycopg2.errors.SyntaxError, ValueError, TypeError, KeyError, psycopg2.errors.InvalidTextRepresentation) as error:
            raise SyntaxError('Something is wrong with the query requested "{}" with params: "{}". Exception: {}.'.format(query, params, error))
        except (Exception, psycopg2.Error) as error:
            # qualcosa è andato storto nella query, sollevo un'eccezione
            raise ConnectionError('Exception while executing query "{}" with params "{}". Exception: {}.'.format(query, params, error)) from error

    def query_no_result(self, query, params=None, return_n_of_rows=False):
        """
        Esegue la query <query> con parametri <params> sul database senza ottenere risultati
        I placeholders nella query hanno formato %(placeholder)s
        :param query:                   stringa contenente la query da eseguire
        :param params:                  placeholder da sostituire
        :param return_n_of_rows:        flag che indica se deve essere ritornato il numero di rige coinvolte dalla query
        :throw SyntaxError:             se ci sono problemi con il formato della query o dei parametri
        :throw ConnectionError:         se ci sono problemi di comunicazione con il database

        :return:                        numero di entries coinvolte dalla query SOLO SE return_n_of_rows == True
        """
        try:
            params = {} if params is None else params
            self.__database_cursor.execute(query, params)

            if return_n_of_rows:
                return None, self.__database_cursor.rowcount
            else:
                return None

        except (psycopg2.errors.SyntaxError, ValueError, TypeError, KeyError, psycopg2.errors.InvalidTextRepresentation) as error:
            raise SyntaxError('Something is wrong with the query requested "{}" with params: "{}". Exception: {}.'.format(query, params, error))
        except (Exception, psycopg2.Error) as error:
            # qualcosa è andato storto nella query, sollevo un'eccezione
            raise ConnectionError('Exception while executing query "{}" with params "{}". Exception: {}.'.format(query, params, error)) from error

    def connection_rollback(self):
        """
        Esegue un rollback della connessione aperta, utilizzabile solo nel caso la sessione non sia autocommit
        :throw ConnectionError:         se ci sono problemi con la transazione
        """
        try:
            self.__database_connection.rollback()
        except (Exception, psycopg2.Error) as error:
            # nel caso ci siano problemi con la connessione sollevo un'eccezione
            raise ConnectionError('Exception during connection rollback.') from error

    def connection_commit(self):
        """
        Esegue un commit della connessione aperta, utilizzabile solo nel caso la sessione non sia autocommit
        :throw ConnectionError:         se ci sono problemi con la transazione
        """
        try:
            self.__database_connection.commit()
        except (Exception, psycopg2.Error) as error:
            # nel caso ci siano problemi con la connessione, faccio un rollback e sollevo un'eccezione
            self.connection_rollback()
            raise ConnectionError('Exception during connection commit. Rollbacking.') from error