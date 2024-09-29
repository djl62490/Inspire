import psycopg2

def insert(text, author, sourceType, sourceTitle):
    # connect to db
    conn = psycopg2.connect(database = "postgres",user = "postgres",password = "molSon!9",host = "localhost")
    
    # create cursor
    cursor = conn.cursor()

    # INSERT command
    cursor.execute("INSERT INTO public.quotes (text, author, \"sourceType\", \"sourceTitle\") VALUES (%s, %s, %s, %s)",(text, author, sourceType, sourceTitle))
    conn.commit()




