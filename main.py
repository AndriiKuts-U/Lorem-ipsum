# Copyright (c) [2021] [Andrii Kuts, Oleksandr Tsepkov]

import discord
import os
import requests
import json
# import random
# from replit import db
from keep_alive import keep_alive
import my_db

client = discord.Client()

command_list = {"$help": "Shows all available commands and their description",
"$my_favorite": "Shows the top of your favorite dishes",
"$my_team": "Shows the info of your team and all its members",
"$create <TEAM_NAME>": "creates team with `<TEAM_NAME>`",
"$join <TEAM_ID>": "join team which id is `<TEAM_ID>`",
"$leave": "Leave the current team",
"$restaurant": "shows list of restaurants",
"$restaurant <RESTAURANT_ID>": "choose a restaurant with `<RESTAURANT_ID>`",
"$order <DISH_ID>": "make order `<DISH_ID>`",
"$my_order": "shows your last order",
"$show_orders": "shows the orders of all your teammates",
"$chef": "Makes you chef of your team for today",
"$whoIsChef": "Shows the current chef of your team",
"$cancel <ORDER_ID>": "cancels your order which id is `<ORDER_ID>`"}


def get_help_info():
  info = ""
  for key, value in command_list.items():
    info += '`' + key + '`' + ": " + value + "\n"
  return (info)


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)


def is_command_correct(msg_to_check):
  if (len(msg_to_check) < 2 or msg_to_check[1] == "" or msg_to_check[1] is None):
    return False
  return True


@client.event
async def on_ready():
  # my_db.drop_all()
  my_db.create_table_teams()
  my_db.create_table_users()
  my_db.create_table_restaurants()
  my_db.create_table_dishes()
  # my_db.insert_into_restaurants()
  # my_db.insert_into_dishes()
  my_db.create_table_orders()
  my_db.create_table_chefs()
  print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content


  if message.content.startswith('$help'):
    embedVar = discord.Embed(title="Help", description="You can use these commands:\n\n" + get_help_info(), color=0x00ff00)
    await message.channel.send(embed=embedVar)


  if message.content.startswith('$my_favorite'):
    info = my_db.get_my_favorite_list(message.author.id)
    embedVar = discord.Embed(title="$my_favorite", description=info, color=0x00ff00)
    await message.channel.send(embed=embedVar)


  # show team members with '\n' separator
  if message.content.startswith('$my_team'):
    info = my_db.get_users_team_info(message.author.id)
    embedVar = discord.Embed(title="$my_team", description=info, color=0x00ff00)
    await message.channel.send(embed=embedVar)


  # DONE?
  if message.content.startswith('$create'):
    team_name = msg.split(' ', 1)
    info = ""
    border_color = 0x00ff00
    if (not is_command_correct(team_name)):
      info = "Wrong `<TEAM_NAME>`. Use `$help`\n"
      border_color = 0xff0000
    else:
      team_name = team_name[1]
      if not my_db.user_exists(message.author.id):
        my_db.add_team(team_name)
        team_id = my_db.cur.lastrowid
        
        my_db.add_user(message.author.id, message.author.name, team_id)
        info = "The team was successfully created.\nYour team ID: `{}`\nTell it to your mates so they can join you".format(team_id)
      else:
        info = "You already have a team. You first need to leave the current team."
        border_color = 0xff0000

    embedVar = discord.Embed(title="$create <TEAM_NAME>", description=info, color=border_color)
    await message.channel.send(embed=embedVar)


  # TODO Check if it works
  if message.content.startswith('$join'):
    team_id = msg.split(' ', 1)
    info = ""
    border_color = 0x00ff00
    if (not is_command_correct(team_id)):
      info = "Wrong `<TEAM_ID>`. Use `$help`\n"
      border_color = 0xff0000
    else:
      try:
        team_id = int(team_id[1])
      except ValueError:
        info = "Wrong `<TEAM_ID>`. Use `$help`\n"
        border_color = 0xff0000
      else:
        if my_db.team_exists(team_id):
          if not my_db.user_exists(message.author.id):
            my_db.add_user(message.author.id, message.author.name, team_id)
            team_name = my_db.get_team_name(team_id);
            info = "You have joined the team `{}`\n".format(team_name)
          else:
            info = "You already have a team. You cant join another one.\nUse `$my_team` to see details.\n"
            border_color = 0xff0000
        else:
          info = "Team with id `{}` not exists. You can create a new one!\nUse the following command:\n`$create <TEAM_NAME>`\nOr use `$help`\n".format(team_id)
          border_color = 0xff0000
    
    embedVar = discord.Embed(title="$join <TEAM_ID>", description=info, color=border_color)
    await message.channel.send(embed=embedVar)


  # DONE
  if message.content.startswith('$leave'):
    my_db.leave_team(message.author.id)
    embedVar = discord.Embed(title="$leave", description="Сongratulations! You don't have a team.\n", color=0x00ff00)
    await message.channel.send(embed=embedVar)


  if message.content.startswith('$order'):
    dish_id = msg.split(' ', 1)
    info = ""
    border_color = 0x00ff00
    if (not is_command_correct(dish_id)):
      info = "Wrong `<DISH_ID>`. Use `$help`\n"
      border_color = 0xff0000
    else:
      try:
        dish_id = int(dish_id[1])
      except ValueError:
        info = "Wrong `<DISH_ID>`. Use `$help`\n"
        border_color = 0xff0000
      else:
        my_db.cur.execute("SELECT DATE()")
        current_date = my_db.cur.fetchone()[0]
        info = my_db.add_order(message.author.id, dish_id, current_date)
        if info is None:
          info = "Your order was added.\n"
        else:
          border_color = 0xff0000
    embedVar = discord.Embed(title="$order <NAME>", description=info, color=border_color)
    await message.channel.send(embed=embedVar)


  if message.content.startswith('$my_order'):
    info = my_db.get_order_info(message.author.id)
    embedVar = discord.Embed(title="$my_order", description=info, color=0x00ff00)
    await message.channel.send(embed=embedVar)


  if message.content.startswith('$cancel'):
    order_id = msg.split(' ', 1)
    info = ""
    border_color = 0x00ff00
    if (not is_command_correct(order_id)):
      info = "Wrong `<ORDER_ID>`. Use `$help`\n"
      border_color = 0xff0000
    else:
      try:
        order_id = int(order_id[1])
      except ValueError:
        info = "Wrong `<ORDER_ID>`. Use `$help`\n"
        border_color = 0xff0000
      else: 
        if my_db.order_exists(order_id):
          my_db.delete_order(message.author.id, order_id)
          info = "Your order was deleted\n"
        else:
          info = "You did not make this order\nUse `$my_order` to see your orders\n"
          border_color = 0xff0000
    embedVar = discord.Embed(title="$cancel", description=info, color=border_color)
    await message.channel.send(embed=embedVar)


  if message.content.startswith('$rec'):
    embedVar = discord.Embed(title="$rec", description="Not yet implemented\n", color=0x00ff00)
    await message.channel.send(embed=embedVar)

  ##################### only 1 chef per team ############
  if message.content.startswith('$chef'):
    info = ""
    border_color = 0x00ff00
    if my_db.user_exists(message.author.id):
      team_id = my_db.get_users_team_id(message.author.id)
      my_db.add_chef(message.author.id,team_id)
      info = "Congratulations, you are ordering food today\n"
    else:
      info = "You are not on any team.\n"
      border_color = 0xff0000
    embedVar = discord.Embed(title="$chef", description=info, color=border_color)
    await message.channel.send(embed=embedVar)


  if message.content.startswith('$show_orders'):
    info = my_db.get_my_team_orders(message.author.id)
    embedVar = discord.Embed(title="$show_orders", description=info, color=0x00ff00)
    await message.channel.send(embed=embedVar)


  if message.content.startswith('$whoIsChef'):
    info = ""
    border_color = 0x00ff00
    if my_db.user_exists(message.author.id):
      team_id = my_db.get_users_team_id(message.author.id)
      border_color = 0x00ff00
      nickname = my_db.get_chef(team_id)
      if(nickname is None):
        info = "You team don't have chef yet!\n"
        border_color = 0xff0000
      else:
        info = "Your teams chef is `{}`\n".format(nickname)
    else:
      info = "You are not on any team.\n"
      border_color = 0xff0000
    embedVar = discord.Embed(title="$whoIsChef", description=info, color=border_color)
    await message.channel.send(embed=embedVar)


  if message.content.startswith('$restaurant'):
    restaurant_id = msg.split(' ', 1)
    info = ""
    border_color = 0x00ff00
    if not is_command_correct(restaurant_id):
      restaurants = my_db.get_restaurants()
      info = "List of all restaurants:{}\n Use `$restaurant <RESTAURANT_ID>` to see restaurant menu".format(restaurants)
      border_color = 0x00ff00
    else:
      try:
        restaurant_id = int(restaurant_id[1])
      except ValueError:
        info = "List of all restaurants:{}\n Use `$restaurant <RESTAURANT_ID>` to see restaurant menu".format(restaurants)
        border_color = 0xff0000
      else:
        if my_db.restaurant_exists(restaurant_id):
          restaurant_name = my_db.get_restaurant_name(restaurant_id)
          menu = my_db.get_menu(restaurant_id)
          info = "Menu of restaurant `{}`: {}\n ".format(restaurant_name,menu)
        else:
          info = "Restaurant with id `{}` does not exists".format(restaurant_id)
          border_color = 0xff0000
    embedVar = discord.Embed(title="$restaurants", description=info, color=border_color)
    await message.channel.send(embed=embedVar)




  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send(quote)


keep_alive()
client.run(os.getenv('TOKEN'))