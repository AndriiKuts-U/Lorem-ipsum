# Hack Kosice Marathon: Lunch assistant

## Team

Lorem Ipsum

### Team members

- Andrii Kuts, Technical University of Kosice
- Oleksandr Tsepkov, Technical University of Kosice

## Description
Our goal was to ease the routine of ordering food for a group of people. To solve this problem, we decided to create a discord bot, because discord is a popular platform that provides all the necessary tools to create this kind of assistant. Our team has made a bot, the functionality of which is suitable for both a small circle of friends and for large companies.
## Protoype

*Describe the basic functionality of your prototype. What are the features you were able to implement? What features would you like to implement?*
Наш бот в данный момент поддерживает следующие комманды:
***$help*** - Shows all available commands and their description;
***$my_favorite*** - Shows the top of your favorite dishes;
***$my_team***: Shows the info of your team and all its members;
***$create <TEAM_NAME>***: creates team with ***<TEAM_NAME>***;
***$join <TEAM_ID>***: join team which id is ***<TEAM_ID>***;
***$leave***: Leave the current team;
***$restaurant***: shows list of restaurants;
***$restaurant <RESTAURANT_ID>***: choose a restaurant with ***<RESTAURANT_ID>***;
***$order <DISH_ID>***: make order ***<DISH_ID>***;
***$my_order***: shows your last order;
***$show_orders***: shows the orders of all your teammates;
***$chef***: Makes you chef of your team for today;
***$whoIsChef***: Shows the current chef of your team;
***$cancel <ORDER_ID>***: cancels your order which id is ***<ORDER_ID>***;

To use the full functionality of the bot, you need to be in a team. To do this, you can create your own using the ***$create <TEAM_NAME>*** command and you will automatically become a member of it, or you can join an existing team using ***$join <TEAM_ID>***. To find out the ***<TEAM_ID>*** of your team, you can use the command ***$my_team***, which at the same time will show you all members of your team. To leave the current team, you will have to use the ***$leave*** command.

How, in our view, the daily ordering food of the company takes place using our bot:
Each team member places orders by choosing from a list of restaurants that are in the database, which can be viewed by writing to the bot ***$restaurant***. The list of dishes for a particular restaurant will be displayed after entering the command ***$restaurant <RESTAURANT_ID>***.
Next, you can order a dish using the ***$order <DISH_ID>*** command. ***$my_order*** Displays a list of orders placed by the user today. To cancel a specific order, you will need to write to the command ***$cancel <ORDER_ID>*** and enter the id of the required order.
Further, anyone can become today's chef  (place orders/delivery) using the ***$chef*** command, while there can be only one chef in the team. You can see who today dared to take on this role by writing the command ***$whoIsChef***.
To avoid a situation where no one wants to be a chef, it would be possible to add the opportunity to take advantage of the great power of random.


## How to try

You can join our [Discord server](https://discord.gg/jNHVUYdz) to try Lunch assistant bot.
Also, you can run Bot's code on our [Replit project](https://replit.com/@Megu5ta/Lorem-ipsum#main.py)


## Challenges and accomplishments

Almost everything was a challenge for our team while working on this project. Creating a bot, launching it, giving it some functionality, working with databases - we have achieved all this thanks to several videos on YouTube, a bit of code that generates errors, and an endless set of documentation and googling.
Also, teamwork was initially a little problematic for us due to the fact that before that we always worked separately and plus to this we have every slightly different view of the way to solve the problem (this is probably even a positive feature). We did not know how to divide tasks among ourselves, how to cooperate, and in general how we imagine our product. But after *n* hours of teamwork, we got much better at it.


## Next steps

In the future, it would be possible to add the ***$recommendation*** command, which, using data from the *orders* table, could recommend the user dishes that he might like based on the orders of other users with similar tastes.

It would also be nice to fill the tables with restaurants and dishes or add an api to automatically fill in the tables of restaurants and their menus.

*What do you need to do next to turn this prototype into a working solution?*

## License

*This repository includes an [unlicense](http://unlicense.org/) statement though you may want [to choose a different license](https://choosealicense.com/).*
