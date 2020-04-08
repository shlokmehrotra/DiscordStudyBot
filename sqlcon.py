import mysql.connector

mydb = mysql.connector.connect(host = "localhost", user = "root", password = "bruhprenk", database = "toughguy")

mycursor = mydb.cursor()

mycursor.execute("INSERT INTO userlog VALUES ( 'value1', 'value2', 'value3')")
mycursor.execute("select * from userlog")
for prenk in mycursor:
	print(prenk)

class MySQLConverterBase(object):
    """Base class for conversion classes
    All class dealing with converting to and from MySQL data types must
    be a subclass of this class.
    """

    def __init__(self, charset='utf8', use_unicode=True):
        self.python_types = None
        self.mysql_types = None
        self.charset = None
        self.charset_id = 0
        self.use_unicode = None
        self.set_charset(charset)
        self.set_unicode(use_unicode)
        self._cache_field_types = {}

    def set_charset(self, charset):
        """Set character set"""
        if charset == 'utf8mb4':
            charset = 'utf8'
        if charset is not None:
            self.charset = charset
        else:
            # default to utf8
            self.charset = 'utf8'
        self.charset_id = CharacterSet.get_charset_info(self.charset)[0]

    def set_unicode(self, value=True):
        """Set whether to use Unicode"""
        self.use_unicode = value

    def to_mysql(self, value):
        """Convert Python data type to MySQL"""
        type_name = value.__class__.__name__.lower()
        try:
            return getattr(self, "_{0}_to_mysql".format(type_name))(value)
        except AttributeError:
            return value
