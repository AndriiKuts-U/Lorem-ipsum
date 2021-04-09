# Copyright (c) [2021] [Andrii Kuts, Oleksandr Tsepkov]
import sqlite3 as sq
import csv

with sq.connect("data/server.db") as con:
    cur = con.cursor()

    def create_table_teams():
      cur.execute("""CREATE TABLE IF NOT EXISTS teams (
          team_id INTEGER PRIMARY KEY,
          team_name TEXT
          )""")
      con.commit()


    def create_table_users():
      cur.execute("""CREATE TABLE IF NOT EXISTS users (
          user_id INTEGER PRIMARY KEY,
          nickname TEXT,
          team_id INTEGER,
          CONSTRAINT FK_team FOREIGN KEY (team_id) REFERENCES teams(team_id)
          )""")
      con.commit()


    def create_table_restaurants():
      cur.execute("""CREATE TABLE IF NOT EXISTS restaurants (
          restaurant_id INTEGER PRIMARY KEY,
          restaurant_name TEXT,
          city TEXT
          )""")
      con.commit()

    
    def create_table_dishes():
      cur.execute("""CREATE TABLE IF NOT EXISTS dishes (
          dish_id INTEGER PRIMARY KEY,
          dish_name TEXT,
          category TEXT,
          restaurant_id INTEGER,
          CONSTRAINT FK_rest FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
          )""")
          
      con.commit()


    def create_table_orders():
      cur.execute("""CREATE TABLE IF NOT EXISTS orders (
          order_id INTEGER PRIMARY KEY,
          user_id INTEGER,
          dish_id INTEGER,
          order_date DATE,
          CONSTRAINT FK_users FOREIGN KEY (user_id) REFERENCES users(user_id),
          CONSTRAINT FK_dish FOREIGN KEY (dish_id) REFERENCES dishes(dish_id)
          )""")
      con.commit()

    def create_table_chefs():
      cur.execute("""CREATE TABLE IF NOT EXISTS chefs (
          user_id INTEGER,
          team_id INTEGER,
          CONSTRAINT FK_teams FOREIGN KEY (team_id) REFERENCES teams(team_id),
          CONSTRAINT FK_user FOREIGN KEY (user_id) REFERENCES users(user_id)
          )""")
      con.commit()

   
    def add_team(team_name):
      cur.execute(f"INSERT INTO teams(team_name) VALUES('{team_name}')")
      con.commit()

    def add_chef(user_id,team_id):
      cur.execute(f"DELETE FROM chefs WHERE team_id={team_id}")
      cur.execute(f"INSERT INTO chefs(user_id,team_id) VALUES({user_id},{team_id})")
      con.commit()
    
    def get_chef(team_id):
      cur.execute(f"SELECT u.nickname FROM users u INNER JOIN chefs s ON u.team_id=s.team_id WHERE s.team_id={team_id}")
      return cur.fetchone()[0]

    def get_users_team_id(user_id):
      cur.execute(f"SELECT team_id FROM users WHERE user_id = ('{user_id}')")
      return cur.fetchone()[0]

    def leave_team(user_id):
      cur.execute(f"DELETE FROM users WHERE user_id = ({user_id})")
      con.commit()


    def add_user(user_id, nickname, team_id):
      cur.execute("INSERT INTO users VALUES(?, ?, ?)", (user_id, nickname, team_id))
      con.commit()


    def add_order(user_id, dish_id, order_date):
      if not user_exists(user_id):
        return "You are not on any team. A great chance to create a new one!\nUse the following command:\n`$create <TEAM_NAME>`\n"
      if not dish_exists(dish_id):
        return "Dish with id `{}` does not exist".format(dish_id)
      cur.execute("INSERT INTO orders(user_id, dish_id, order_date) VALUES(?, ?, ?)", (user_id, dish_id, order_date))
      con.commit()

    def get_team_name(team_id):
      cur.execute(f"SELECT team_name FROM teams WHERE team_id={team_id}")
      return cur.fetchone()[0]

    def delete_order(user_id, order_id):
      cur.execute(f"DELETE FROM orders WHERE order_id={order_id} AND user_id={user_id}")
      

    def user_exists(user_id):
      cur.execute(f"SELECT EXISTS(SELECT * FROM users WHERE user_id={user_id} LIMIT 1)")
      return cur.fetchone()[0]


    def dish_exists(dish_id):
      cur.execute(f"SELECT EXISTS(SELECT * FROM dishes WHERE dish_id={dish_id} LIMIT 1)")
      return cur.fetchone()[0]


    def restaurant_exists(restaurant_id):
      cur.execute(f"SELECT EXISTS(SELECT * FROM restaurants WHERE restaurant_id={restaurant_id} LIMIT 1)")
      return cur.fetchone()[0]


    def get_restaurant_name(restaurant_id):
      cur.execute(f"SELECT restaurant_name FROM restaurants WHERE restaurant_id={restaurant_id}")
      return cur.fetchone()[0]


    def order_exists(order_id, user_id):
      cur.execute(f"SELECT EXISTS(SELECT * FROM orders WHERE order_id={order_id} AND user_id={user_id} LIMIT 1)")
      return cur.fetchone()[0]


    def team_exists(team_id):
      cur.execute(f"SELECT EXISTS(SELECT * FROM teams WHERE team_id={team_id} LIMIT 1)")
      return cur.fetchone()[0]


    def get_users_team_info(user_id):
      cur.execute(f"SELECT t.team_id, t.team_name FROM teams t WHERE t.team_id=(SELECT u.team_id FROM users u WHERE u.user_id={user_id} LIMIT 1)")
      get = cur.fetchone()
      if get is None:
          return "You are not on any team. A great chance to create a new one!\nUse the following command:\n`$create <TEAM_NAME>`\n"
      else:
          return "Your team name is: `{}`\nTeam_id: `{}`\nTeam members:\n{}".format(get[1], get[0], get_team_members(user_id))


    def get_order_info(user_id):
      cur.execute("SELECT DATE()")
      current_date = cur.fetchone()
      cur.execute(f"SELECT o.order_id, d.dish_id, d.dish_name, o.order_date FROM dishes d INNER JOIN orders o ON o.dish_id=d.dish_id WHERE o.user_id={user_id} AND o.order_date='{current_date[0]}'")
      info = ""
      var = cur.fetchone()
      if var is None:
          return "You don't make any order yet!\nUse the following command:\n`$order <YOUR_ORDER>`\n"
      while var is not None:
        info += ('\n' +  "order_id: " + '`' + str(var[0]) + '`' + '\tdish_id: ' + '`' + str(var[1]) + '`\t`' + var[2] +  '`\t`' + var[3] + '`')
        var = cur.fetchone()
      return "Your order is: {}".format(info)


    def get_team_members(user_id):
        cur.execute(f"SELECT nickname FROM users WHERE team_id=(SELECT team_id FROM users WHERE user_id={user_id})")
        return str(cur.fetchall()).replace('[', '').replace('(', '').replace(',', '').replace(')', '').replace(']', '').replace("'", '`')
    
    def get_restaurants():
      cur.execute("SELECT * FROM restaurants")
      l = cur.fetchall()
      info = ""
      for i in l:
        info +=  ('\n' + "restaurant id: " + '`' + str(i[0]) + '`' + '\t' + '`' + i[1] + '`' + '\t' + '`' + i[2] + '`')
      return info

    def get_menu(restaurant_id):
      cur.execute(f"SELECT * FROM dishes WHERE restaurant_id={restaurant_id}")
      l = cur.fetchall()
      info = ""
      for i in l:
        info +=  ('\n' + "dish id: "  +  '\t' + '`' +  str(i[0]) + '`' + '\t' + '`' + i[1] + '`' + '\t' + '`' + i[2] + '`' )
      return info

    def insert_into_restaurants():
      with open("data/restaurants.csv", "r") as file:
        rows = csv.reader(file)
        cur.executemany("INSERT INTO restaurants VALUES (?,?,?)", rows)
        con.commit()
      # cur.execute("SELECT * FROM restaurants")
      # print(cur.fetchall())
      
    def insert_into_dishes():
      with open("data/dishes.csv", "r") as file:
        rows = csv.reader(file)
        cur.executemany("INSERT INTO dishes VALUES (?,?,?,?)", rows)
        con.commit()
      # cur.execute("SELECT * FROM dishes")
      # print(cur.fetchall())
    

    def get_my_favorite_list(user_id):
      cur.execute(f"SELECT o.dish_id, r.restaurant_name, d.dish_name, COUNT(*) FROM orders o INNER JOIN dishes d ON d.dish_id=o.dish_id INNER JOIN restaurants r ON d.restaurant_id=r.restaurant_id WHERE o.user_id={user_id} GROUP BY d.dish_id ORDER BY COUNT(*) DESC LIMIT 5")
      info = ""
      get = cur.fetchone();
      if get is None:
        return "You need to make some orders first\n"
      while get is not None:
        info += "dish_id: " + '`' + str(get[0]) + '` ' + '`' + get[1] + '` ' + '`' + get[2] + '`''\n'
        get = cur.fetchone()
      return info
  

    def get_my_team_orders(user_id):
      team_id = get_users_team_id(user_id)
      cur.execute("SELECT DATE()")
      current_date = cur.fetchone()
      cur.execute(f"SELECT u.nickname, r.restaurant_name, d.dish_name FROM orders o INNER JOIN users u ON u.user_id=o.user_id INNER JOIN dishes d ON d.dish_id=o.dish_id INNER JOIN restaurants r ON d.restaurant_id=r.restaurant_id WHERE o.order_date='{current_date[0]}' AND u.team_id={team_id}")
      info = "Orders from your teammates:\n"
      get = cur.fetchone()
      while get is not None:
        info += '`' + get[0] + '` `' + get[1] + '` `' + get[2] + '`' + '\n'
        get = cur.fetchone()
      return info



    def drop_all():
      cur.execute("PRAGMA foreign_keys = OFF")
      cur.execute("DROP TABLE IF EXISTS users")
      cur.execute("DROP TABLE IF EXISTS teams")
      cur.execute("DROP TABLE IF EXISTS orders")
      cur.execute("DROP TABLE IF EXISTS dishes")
      cur.execute("DROP TABLE IF EXISTS restaurants")
      cur.execute("DROP TABLE IF EXISTS chefs")
      cur.execute("PRAGMA foreign_keys = ON")
      con.commit()