# Hack Kosice Marathon: Lunch assistant

*A template for projects submitted to HK Marathon 2021. You can [fork this repository](https://docs.github.com/en/github/getting-started-with-github/fork-a-repo) and use it as a starting point.*

## Team

Lorem Ipsum

### Team members

- Andrii Kuts, Technical University of Kosice
- Oleksandr Tsepkov, Technical University of Kosice

## Description

*A clear statement of the challenges, issues, problems or gaps that your project solves and a brief description of how your project tackles the areas. What is the value of your solution? Who are the target users?*

Нашей целью было облегчить рутину заказа еды для компании людей. Для решения этой проблемы мы решили создать дискорд бота, потому что дискорд это популярная площадка, которая предоставляет все необходимые инструменты для создания такого рода помощника. Наша команда сделала бота, функционал которого подходит как для небольшого круга друзей так и для больших компаний.
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
***$show_orders***: "shows the orders of all your teammates";
***$chef***: "Makes you chef of your team for today";
***$whoIsChef***: "Shows the current chef of your team";
***$cancel <ORDER_ID>***: cancels your order which id is ***<ORDER_ID>***;

Для использования полного функционала бота нужно состоять в команде. Для этого можно создать свою с помощью комманды ***$create <TEAM_NAME>*** и вы автоматически станете её участником, или же присоедениться к уже существующей комманде с помощью ***$join <TEAM_ID>***. Чтобы узнать ***<TEAM_ID>*** своей комманды можно воспользоваться коммандой ***$my_team***, которая заодно выпишет и всех её участников. Чтобы покинуть текущую команду придеться воспользоваться коммандой ***$leave***.

Как в нашем представлении происходит ежедневное оформление заказов в компании с помощью нашего бота:
каждый член команды делает заказы, выбирая из списка ресторанов, который можно посмотреть, написав боту ***$restaurant***, после этого бот выпишет все рестораны, которые находятся в базе данных. Список блюд конкретного ресторана отображается после комманды ***$restaurant <RESTAURANT_ID>***.
Далее, можно сделать заказ блюда, с помощью комманды ***order <DISH_ID>***. ***$my_order*** Отображает список заказов, сделанных пользователем сегодня. Чтобы отменить какой-то конкретный заказ нужно будет написать комманду ***cancel <ORDER_ID>*** и указать id нужного заказа.
Далее любой желающий может стать шефом на сегодня(оформлять заказы/доставку) использовав комманду ***$chef***, при этом шеф в комманде может быть только один. Посмотреть кто сегодня насмелился взять на себя эту роль можно написав комманду ***$whoIsChef***.

В будущем можно было бы ещё добавить комманду ***$rec***, которая используя данные из таблицы *orders* могла бы подсказать пользователю то блюдо, которое может ему понравится, на основе заказов пользователей с похожими вкусами.

Также не помешало бы наполнить 

## How to try

You can join our [Discord server](https://discord.gg/jNHVUYdz) to try Lunch assistant bot.
Also, you can run Bot's code on our [Replit project](https://replit.com/@Megu5ta/Lorem-ipsum#main.py)


## Presentation

*List any links to your presentation or additional materials that you want to share with the judges.*

## Challenges and accomplishments

*Is there anything unexpected that you learned over the course of this project?*

*Is there something your team is particularly proud of, related to this project?*

## Next steps

*What do you need to do next to turn this prototype into a working solution?*

## License

*This repository includes an [unlicense](http://unlicense.org/) statement though you may want [to choose a different license](https://choosealicense.com/).*
