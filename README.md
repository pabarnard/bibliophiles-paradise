# Bibliophile's Paradise

This application allows book lovers to search for and save books they've read, and they can keep a journal of what they've read.  These thoughts can be public or private.  Users can rate books as well, and even discuss the books with other users as well.

This project will be built in phases:
1. Prototyping (DONE):
    - Built out the wireframe with **Balsamiq** to foster collaboration with nontechnical stakeholders and developers 
2. Utilizing MySQL for a database management system (DBMS) and designing the schema (current phase):
    - The wireframe will inform the tables and relationships required for the application to run.  
    - Information from **Google Books API** will be saved locally so that API calls are minimized and thus limited to only searching for new books no users have read or added yet.
3. Back end with using the **Flask** microframework:
    - Define the routes, models, and more using the Models-Views-Controllers (MVC) design paradigm.
    - Tie in the Google Books API to allow users to add books to the database and their libraries.
    - Create queries to retrieve relevant books, reviews and thoughts accordingly.
4. Front end: 
    - Building out the basic HTML *only* and the needed forms and features.
    - No styling will be applied yet.  This will happen in a later phase.
    - Utilize a trie or similar data structure for the search feature when adding a book; this allows a user to quickly identify a book from the database that can be added to their library without needing to call the Google Books API to retrieve the same info that's already saved locally.
5. Unit testing - utilizing a testing framework (to be determined) to make sure the app works correctly; this is test-driven development (TDD)
6. Logging - to keep track of the app while it runs; this becomes especially important when deploying
7. Stylizing the app - Tailwind CSS will now be applied to make the app mobile-friendly and give a clear user interface (UI) and improve the user experience (UX)
8. Deployment - likely will use AWS and find a suitable domain name