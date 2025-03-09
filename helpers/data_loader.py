import csv
import os
from typing import Callable, Any
from db import db


class DataLoader:

    async def load_csv(self, csv_path: str, model: Any, unique_keys: list[str], transform_functions: list[ Callable ] | None = None) -> None:
        if not os.path.exists(csv_path):
            raise AttributeError("Csv file not found")

        async with db.session.begin():
            with open(csv_path, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)

                for record in reader:
                    model_record = model()
                    for function in (transform_functions or []):
                        function(model_record, record)

                    filters = {key: getattr(model_record, key) for key in unique_keys}

                    existing_record = await db.session.execute(
                        db.select(model).filter_by(**filters)
                    )
                    if existing_record.scalar():
                        print(f"⚡ Skipping existing record: {filters}")
                        continue

                    db.session.add(model_record)
            await db.session.commit()