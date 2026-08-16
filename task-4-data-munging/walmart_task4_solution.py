import csv
import sqlite3


class DatabaseConnector:
    """
    Manages a connection to a SQLite database.
    """

    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def populate(self, spreadsheet_folder):
        """
        Populate the database with data imported from each spreadsheet.
        """
        with open(f"{spreadsheet_folder}/shipping_data_0.csv", "r", newline="", encoding="utf-8") as spreadsheet_file_0, \
             open(f"{spreadsheet_folder}/shipping_data_1.csv", "r", newline="", encoding="utf-8") as spreadsheet_file_1, \
             open(f"{spreadsheet_folder}/shipping_data_2.csv", "r", newline="", encoding="utf-8") as spreadsheet_file_2:

            csv_reader_0 = csv.reader(spreadsheet_file_0)
            csv_reader_1 = csv.reader(spreadsheet_file_1)
            csv_reader_2 = csv.reader(spreadsheet_file_2)

            self.populate_first_shipping_data(csv_reader_0)
            self.populate_second_shipping_data(csv_reader_1, csv_reader_2)

    def populate_first_shipping_data(self, csv_reader_0):
        """
        Populate the database with data from shipping_data_0.csv.
        """
        for row_index, row in enumerate(csv_reader_0):

            # Skip header
            if row_index > 0:

                product_name = row[2]
                product_quantity = row[4]
                origin = row[0]
                destination = row[1]

                self.insert_product_if_it_does_not_already_exist(product_name)

                self.insert_shipment(
                    product_name,
                    product_quantity,
                    origin,
                    destination
                )

    def populate_second_shipping_data(self, csv_reader_1, csv_reader_2):
        """
        Combine shipping_data_1.csv and shipping_data_2.csv
        using the shipping identifier.
        """

        shipment_info = {}

        # Read shipment information from spreadsheet 2
        for row_index, row in enumerate(csv_reader_2):

            # Skip header
            if row_index > 0:

                shipment_identifier = row[0]
                origin = row[1]
                destination = row[2]

                shipment_info[shipment_identifier] = {
                    "origin": origin,
                    "destination": destination,
                    "products": {}
                }

        # Read products from spreadsheet 1
        for row_index, row in enumerate(csv_reader_1):

            # Skip header
            if row_index > 0:

                shipment_identifier = row[0]
                product_name = row[1]

                products = shipment_info[shipment_identifier]["products"]

                # Count how many times each product appears
                if product_name not in products:
                    products[product_name] = 1
                else:
                    products[product_name] += 1

        # Insert combined shipment data
        for shipment_identifier, shipment in shipment_info.items():

            origin = shipment["origin"]
            destination = shipment["destination"]

            for product_name, product_quantity in shipment["products"].items():

                self.insert_product_if_it_does_not_already_exist(product_name)

                self.insert_shipment(
                    product_name,
                    product_quantity,
                    origin,
                    destination
                )

    def insert_product_if_it_does_not_already_exist(self, product_name):
        """
        Insert product if it does not already exist.
        """

        query = """
            INSERT OR IGNORE INTO product (name)
            VALUES (?);
        """

        self.cursor.execute(query, (product_name,))
        self.connection.commit()

    def insert_shipment(
        self,
        product_name,
        product_quantity,
        origin,
        destination
    ):
        """
        Insert shipment into the database.
        """

        # Find product ID
        query = """
            SELECT id
            FROM product
            WHERE product.name = ?;
        """

        self.cursor.execute(query, (product_name,))

        product_id = self.cursor.fetchone()[0]

        # Insert shipment
        query = """
            INSERT OR IGNORE INTO shipment
                (product_id, quantity, origin, destination)
            VALUES (?, ?, ?, ?);
        """

        self.cursor.execute(
            query,
            (
                product_id,
                product_quantity,
                origin,
                destination
            )
        )

        self.connection.commit()

    def close(self):
        self.connection.close()


if __name__ == "__main__":

    database_connector = DatabaseConnector(
        "shipment_database.db"
    )

    database_connector.populate("./data")

    database_connector.close()

    print("Database populated successfully.")