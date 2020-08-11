import pyodbc

class Text(object):
    VISION = 'vision'
    SPEECH = 'speech'
    expected_sources = (VISION, SPEECH)

    def __init__(self, connection_string):
        self.connection = pyodbc.connect(connection_string)
        self.cursor = self.connection.cursor()

    def insert_text(self, source, text):
        """The source should being either 'vision' or 'speech' and text should be a string."""
        assert source in self.expected_sources
        insert_into_text_query = f"INSERT INTO ProcessedText VALUES (DEFAULT, '{source}', '{text}')"
        self.cursor.execute(insert_into_text_query)
        self.connection.commit()

class TextAdmin(Text):
    def ensure_tables_exist(self):
        """Create any missing tables.  Safe to run even when some or all of the tables already exists."""
        create_table_query = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ProcessedText' and xtype='U')
            CREATE TABLE ProcessedText (
                Timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                Source CHAR(6) NOT NULL,
                Text TEXT NOT NULL,
                PRIMARY KEY(Timestamp, Source)
            )
        """

        self.cursor.execute(create_table_query)
        self.connection.commit()
