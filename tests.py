import unittest
from unittest.mock import MagicMock
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, inspect
import pandas as pd
import etl

class TestETL(unittest.TestCase):
    """
    Unit test class for the ETL process.
    """

    def setUp(self):
        """
        Set up the test environment. This method is called before each test.
        """
        # Create an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        self.metadata = MetaData()

        # Create a sample DataFrame for testing
        self.data_frame = pd.DataFrame({
            'column1': [1, 2, 3],
            'column2': ['a', 'b', 'c'],
            'column3': [1.1, 2.2, 3.3]
        })

        # Check if table exists in the database, if not create it
        inspector = inspect(self.engine)
        if not inspector.has_table('test_table'):
            self.table = Table(
                'test_table', self.metadata,
                Column('column1', Integer),
                Column('column2', String),
                Column('column3', Float),
                extend_existing=True
            )
            self.metadata.create_all(self.engine)
        else:
            self.table = Table('test_table', self.metadata, autoload_with=self.engine)

    def test_validate_schema(self):
        """
        Test the validate_schema function.
        """
        # Test the method
        try:
            etl.validate_schema(self.data_frame, self.table)
        except Exception as e:
            # If an exception is raised, the test fails
            self.fail(f"validate_schema raised Exception unexpectedly: {e}")

    def test_load_data(self):
        """
        Test the load_data function.
        """
        # Mock the validate_schema function
        etl.validate_schema = MagicMock()

        # Test the method
        try:
            etl.load_data(self.data_frame, self.table, self.engine)
        except Exception as e:
            # If an exception is raised, the test fails
            self.fail(f"load_data raised Exception unexpectedly: {e}")

        # Check that validate_schema was called once with the correct arguments
        etl.validate_schema.assert_called_once_with(self.data_frame, self.table)

if __name__ == '__main__':
    unittest.main()