import psycopg2


def empty_DB():
	con = psycopg2.connect(
		host='localhost',
		database='postgres',
		user='postgres',
		password='winding1127!'
	)

	cur = con.cursor()

	# Delete all rows
	cur.execute("DELETE FROM product")
	con.commit()

	cur.close()
	con.close()


if __name__ == '__main__':
	empty_DB()
