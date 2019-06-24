from collections import namedtuple
import datetime


class PlacesGateway:
    @classmethod
    def get(cls, connection):
        connection.execute('''
            SELECT
                id,
                name
            FROM point;
        ''')
        return connection.fetchall()


class UserGateway:
    ROW_COLUMNS = [
        'id',
        'first_name',
        'last_name',
        'username',
        'password',
    ]

    User = namedtuple('User', ROW_COLUMNS)

    @classmethod
    def get_by_username(cls, username, connection):
        connection.execute('''
        SELECT 
            user.id,
            user.first_name,
            user.last_name,
            user.username,
            user.password
        FROM user
        WHERE user.username = ?
        ''', (username, ))

        row = connection.fetchone()
        return cls.User(*row)

    @classmethod
    def get_by_id(cls, id, connection):
        connection.execute('''
        SELECT
            user.id,
            user.first_name,
            user.last_name,
            user.username,
            user.password
        FROM user
        WHERE user.id = ?
        ''', (id, ))

        row = connection.fetchone()
        return cls.User(*row)

    def get_by_ids(self, ids: list):
        pass


class MessageGateway:
    ROW_COLUMNS = [
        'id',
        'sender',
        'text',
        'date',
        'place', ]

    @classmethod
    def get_last_10(cls, connection):
        connection.execute('''
            SELECT 
                messages.id,
                u.first_name || ' ' || u.last_name,
                `text`, 
                `date`, 
                `place`
            FROM messages
            JOIN user u on messages.sender = u.id
            ORDER BY date DESC
            LIMIT 10
        ''')
        Message = namedtuple('Message', cls.ROW_COLUMNS)
        for row in connection.fetchall():
            yield Message(*row)

    @classmethod
    def insert(cls, sender, text, place, connection):
        date = datetime.datetime.now()
        connection.execute('''
            INSERT INTO messages (text, "date", place, sender) VALUES (?, ?, ?, ?);
        ''', (text, date, place, sender))


class ScheduleGateway:
    ROW_COLUMNS = ['weekday',
                   'machinist',
                   'time_start',
                   'point_start',
                   'time_finish',
                   'point_end', ]

    WEEKDAYS = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']


    @classmethod
    def get_current(cls, connection):
        connection.execute('''
            SELECT
                weekday,
                u.first_name || ' ' || u.last_name,
                time_start,
                ps.name,
                time_finish,
                pe.name
            FROM schedule
            JOIN "user" u on schedule.machinist = u.id
            JOIN point pe on schedule.point_end = pe.id
            JOIN point ps on schedule.point_start = ps.id
        ''')
        Schedule = namedtuple('Schedule', cls.ROW_COLUMNS)
        for row in connection.fetchall():
            sch = Schedule(*row)
            sch = sch._replace(weekday=cls.WEEKDAYS[sch.weekday])
            yield sch


