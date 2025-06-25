from database.DB_connect import DBConnect
from model.order import Order
from model.store import Store


class DAO():

    @staticmethod
    def getAllStore():
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)

        result = []

        query = """ select * from stores"""

        cursor.execute(query)

        for row in cursor:
            result.append(Store(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getAllNodes(store):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select *
                    from orders o
                    where store_id = %s"""

        cursor.execute(query, (store,))

        for row in cursor:
            result.append(Order(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getAllArchi(store, nMax, idMap):
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)

        result = []

        query = """select distinct o1.order_id as o1, o2.order_id as o2,  (COUNT(oi1.quantity+oi2.quantity)) as peso
                from orders o1,orders o2, order_items oi1, order_items oi2
                where o1.store_id = o2.store_id 
                and o1.store_id = %s
                and datediff(o1.order_date, o2.order_date) < %s
                and o1.order_id = oi1.order_id
                and o2.order_id = oi2.order_id
                and o1.order_date > o2.order_date 
                group by o1.order_id, o2.order_id """


        cursor.execute(query, (store,nMax,))

        for row in cursor:
            result.append((idMap[row["o1"]], idMap[row["o2"]], row["peso"]))

        cursor.close()
        conn.close()

        return result