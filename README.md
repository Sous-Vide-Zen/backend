# Sous-Vide Zen Backend

Sous-Vide Zen is a website for sharing and discovering recipes for sous-vide cooking, a technique that involves cooking food in vacuum-sealed bags at precise temperatures. Users can create their own recipes, browse popular and featured recipes, follow other users, react and comment on recipes, and save their favorites.

## Features

- **Main page**: The main page consists of two tabs: a feed of popular recipes for the last 24 hours and a feed of subscriptions, sorted by time.
- **Recipe page**: This page contains recipes from the website itself, for those who do not need all the social features. Recipes here are divided by categories, and there is a search function for recipes.
- **User page**: Information about the user and avatar, a feed of user's posts, and an option to subscribe.
- **Authorization page**: The ability to register and log in using email or social networks (Yandex and VK).
- **Favorites**: A page of favorite recipes.
- **Recipes**: All recipes can have reactions and comments, be added to favorites, and be reposted to one's own feed.

## Structure

The backend should consist of the following applications:

- **User**: This application handles user authentication, authorization, profile editing, and subscription management.
- **Recipe**: This application handles recipe creation, editing, deletion, viewing, and categorization.
- **Feed**: This application handles the generation of feeds for popular and subscribed recipes.
- **Favorite**: This application handles the addition and removal of recipes to favorites.
- **Reaction**: This application handles the creation and deletion of reactions to recipes.
- **Tag**: This application handles the creation and deletion of tags for recipes.
- **Ingredient**: This application handles the creation and deletion of ingredients for recipes.
- **Comment**: This application handles the creation and deletion of comments on recipes.
- **Views**: This application handles the counting and displaying of views on recipes.
- **Category**: This application handles the creation and deletion of categories for admin recipes.
- **Search**: This application handles the search function for recipes.

## Models

Each application has its own models that define the data structure and relations. Here are some examples:

### User

Model:
- Username - Nickname (required, 30 characters)
- email - Email (required, 150 characters)
- join_date - Registration date (auto)
- country - Country (30 characters)
- City - City (30 characters)
- First name - First name (30 characters)
- Second name - Last name (30 characters)
- bio - About me (200 characters)
- avatar - Avatar (jpg/png, no more than 5 megabytes)
- Role - superuser/admin - full access to all functionality, moderator - Ability to edit/delete/add content, ban users
- Is_banned - True if the user is banned

### Recipe

Model:
- Author: References User model
- Title: Recipe name
- full_text: Text description with HTML markup (5000 characters)
- short_text: Short text description of the recipe, takes about the first 100 characters from the full text (rounded to the word)
- Ingredient: Can be many, references Ingredient model, if ingredient is not in the database, it is added (50 characters)
- Tag: Can be many, references Tag model, if tag is not in the database, it is added
- Category: Categories only for admin recipes. References Category model
- Cooking time: Cooking time in minutes
- Views: Views, references Views model
- Reactions: Reactions, references Reaction model
- pub_date: Creation date, automatically
