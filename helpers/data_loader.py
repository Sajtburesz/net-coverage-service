import csv
import os
from typing import Callable, Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError

class DataLoader:
    """
        Class for loading any data.
        -> Currently it allows to load any csv
        Parameters:
            :param db: any kind of SQLAlchemy db session
            :param batch_size: Any integer. Data insertion will happen in batches of size batch_size
    """
    def __init__(self, db: SQLAlchemy, batch_size: int):
        self.db = db
        self.batch_size = batch_size

    def load_csv(self, csv_path: str, model: Any, unique_keys: list[str],
                 transform_functions: list[Callable] | None = None) -> None:
        """
        Function to load any csv data into the database
        :param csv_path:
        :param model: Any SQLAlchemy model that corresponds to the format the data will be inserted into the db
        :param unique_keys: Left it in here in case some checks need to be done against some keys
        :param transform_functions: Functions which take a model_instance type of model and a line from the csv(record)
               as parameter, and they do something with the data essentially populating the model_instance

        In its current form this dataloader is quite slow for large datasets. A good solution would be to process data in chunks in parallel.
        """
        if not os.path.exists(csv_path):
            raise AttributeError("CSV file not found")


        with open(csv_path, newline="", encoding="utf-8") as csvfile:

            sample = csvfile.read(1024)
            dialect = csv.Sniffer().sniff(sample)
            csvfile.seek(0)
            reader = csv.DictReader(csvfile, dialect=dialect)

            stmt = insert(model).prefix_with("IGNORE")

            records = []
            for record in reader:
                model_instance = model()
                try:
                    for function in (transform_functions or []):
                        function(model_instance, record)
                except:
                    continue

                model_data = {column.name: getattr(model_instance, column.name) for column in
                              model.__table__.columns}

                records.append(model_data)

                if len(records) >= self.batch_size:
                    with self.db.session.begin():
                        try:
                            print("Inserting into db...")
                            # self.db.session.bulk_insert_mappings(model, records)
                            self.db.session.execute(stmt, records)
                            self.db.session.commit()
                            records = []
                        except IntegrityError:
                            self.db.session.rollback()
                            raise

            if records:
                with self.db.session.begin():
                    try:
                        print("Inserting into db...")
                        # self.db.session.bulk_insert_mappings(model, records)
                        self.db.session.execute(stmt, records)
                        self.db.session.commit()
                    except IntegrityError:
                        self.db.session.rollback()
                        raise
