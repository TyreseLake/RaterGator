[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/Snickdx/myproject.git) 

# Before you start
Create a heroku account by following this [link](https://signup.heroku.com/login)
You will also need a github account.

# Creating & Linking your own github repository
Git is used to perform source control. It helps teams manage code bases and merge togher their contributions.
Github is a free Git server for developers to host their git repositories.

When the project is launched on gitpod, it will already be linked to a starter github repository. To link it to a new repository you need to first run the following command.

```
rm - rf .git
```
Now you can initialize a new git workspace by executing the following.


```
git init
```

Next, create your respository on github by following this [link](https://github.com/new). Give it a name and click on the green "Create Repository" button below.
The next page would give you instructions on how to link the repository to an existing workspace.

Copy the command which looks like.

```
git remote add origin https://github.com/<username>/<reponame>.git
```
Paste and run the command in gitpod.

Your workspace should now be linked to your repository

# Heroku Setup
To login to heroku open a new terminal in gitpod and enter run the following command:

```
heroku login --interactive
```
You will then be prompted to enter you heroku credentials. Then to create a new heroku application run the following command:

```
heroku create
```
The app should be created with a random name and can be seen on your [heroku dashboard](https://dashboard.heroku.com/apps/)

# Pushing changes to Git
Now the workspace is linked with a git repository it will track all the changes you make to its files.
Run the following command to select which files will be **staged** (tracked for changes)

```
git stage *
```

This will stage all files in the workspace.
Then You prepare the changes to be sent to the repository by making a **commit**. You must supply a custom commit message when making commits.
Run the following command

```
git commit -m "first commit"
```

Finally you can send your changes to the repository by performing a **push**.

```
git push -u origin master
```

Heroku is setup to auto deploy the application for every push to the master branch the github repo. You can view the application by opening it from your [heroku dashboard](https://dashboard.heroku.com/apps/). Click on the newly created app then click on the "Open App" button.

You application should now be deployed on heroku!

