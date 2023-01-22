## endpoints 

If you are local 
- http://0.0.0.0:15400  
the deployed URL 
- https://wolf-and-badger-profile-app.herokuapp.com/

If a user is not logged In, you will not be able to execute the endpoints, you will get session invalid instead

- /github-login
  ✔️This endpoint is in charge of redirect to the GitHub login With Oauth that receive the code send to /github-code

- /github-code
   ✔️This endpoint receive the code parameter from /github-login and create the new user session, as well it create a new user
     in the database with the information of the user profile 

- /user-profile
   ✔️This endpoint returns the information from the user logged In, Profile information

- /update-user
   ✔️This endpoint receive parameters to create and update new fields pre-defined 

- /delete-profile
   ✔️It allows to delete the complete user profile of the logged In 

- /whoami
   ✔️ Who I am let see what is the current user logged In

- /logout
    ✔️ log Out, this endpoint is in charge to delete the session od the user 
