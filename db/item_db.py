import pyodbc


class ItemDatabase:
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=AryantNigam;DATABASE=restaurent;')
    cursor = conn.cursor()

    @classmethod
    def get_item(cls, item_id=None):
        query = ''
        if item_id:
            query = f"SELECT * FROM items WHERE id = '{item_id}';"
        else:
            query = f"SELECT * FROM items"
        cls.cursor.execute(query)
        items_data = cls.cursor.fetchall()

        response = []
        if items_data:
            for item in items_data:
                response.append(
                    {
                        'id': item[0],
                        'item':
                            {
                               'name': item[1],
                               'price': item[2]
                            }
                    }
                )
        return response

    @classmethod
    def add_item(cls, new_item):
        query = f"INSERT INTO items (id, name, price) VALUES ('{new_item['id']}','{new_item['item']['name']}',{new_item['item']['price']});"
        cls.cursor.execute(query)
        cls.conn.commit()

    @classmethod
    def update_item(cls, item_id, new_item):
        query = f"UPDATE items SET name = '{new_item['name']}', price = {new_item['price']} WHERE id = '{item_id}';"
        affected_rows = cls.cursor.execute(query).rowcount
        cls.conn.commit()
        return affected_rows

    @classmethod
    def delete_item(cls, item_id):
        query = f"DELETE FROM items WHERE id = '{item_id}';"
        affected_rows = cls.cursor.execute(query).rowcount
        cls.conn.commit()
        return affected_rows


# idb = ItemDatabase()
# ItemDatabase.delete_item('7333c3e29c7b4da895d7b0542c044c6c')
# ItemDatabase.update_item(
#     item_id='7333c3e29c7b4da895d7b0542c044c6c',
#     new_item={
#         "name": "Hakka Noodles",
#         "price": 149}
# )
# from uuid import  uuid4
# print(uuid4().hex)