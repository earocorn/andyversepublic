# AndyVerseUser action URLs:
-   **/andyverseusers/?firebase_id_token=<FIREBASE_ID_TOKEN>**
    - List ALL users when authorized via firebase_id_token parameter.
    - Create only new AndyVerseUser object in database when authorized. see **/andyverseusers/create_dual_user**
    - *Accepts GET and POST*


-   **/andyverseusers/retrieve_from_uid/?uid=<UID>&firebase_id_token=<FIREBASE_ID_TOKEN>**
    - Get a user's database information based on uid and firebase token. Response will always go through if user is an admin. If not admin, user can only access their own information.
    - *Accepts GET*


-   **/andyverseusers/delete_by_uid/?uid=<UID>&firebase_id_token=<FIREBASE_ID_TOKEN>**
    - Delete a user by uid if authorized.
    - *Accepts DELETE*
    - **TODO: Change to allow user to delete their own account and let admin delete any account.**


-   **/andyverseusers/update_by_uid/?uid=<UID>&firebase_id_token=<FIREBASE_ID_TOKEN>**
    - Update any user if authorized, update self if uid matches firebase token for any role.
    - *Accepts PUT*
    - **NOTE: Non-admin users can only update username and profile_img**


-   **/andyverseusers/create_dual_user/?email=<EMAIL>&username=<USERNAME>&firebase_id_token=<FIREBASE_ID_TOKEN>**
    - Create new AndyVerseUser and Firebase user given email and username. Sets randomly generated password.
    - *Accepts POST*


# MovieReview action URLs:
-   **/moviereviews/?firebase_id_token=<FIREBASE_ID_TOKEN>**
    - List ALL movie reviews when authorized via firebase_id_token parameter.
    - Create new movie review when authorized.
    - *Accepts GET and POST*


-   **/moviereviews/public_reviews**
    - List all reviews where public parameter = True
    - *Accepts GET*


-   **/moviereviews/delete_by_movie_id/?movie_id=<MOVIE_ID>&firebase_id_token=<FIREBASE_ID_TOKEN>**
    - Delete movie review post using movie_id and authenticating w/ firebase_id_token
    - *Accepts DELETE*


-   **/moviereviews/retrieve_by_movie_id/?movie_id=<MOVIE_ID>&firebase_id_token=<FIREBASE_ID_TOKEN>**
    - Retrieve details of a post using movie_id. Allows anyone to retrieve public posts
    while authorized users can retrieve any post.
    - *Accepts GET*


-   **/moviereviews/update_by_movie_id/?movie_id=<MOVIE_ID>&firebase_id_token=<FIREBASE_ID_TOKEN>**
    - Update a review using its movie_id when authorized.
    - *Accepts PUT and PATCH*


# Message URLs
-   **/messages/<OPTIONAL_MESSAGE_ID>/?firebase_id_token=<FIREBASE_ID_TOKEN>**
    - Allow creation for any user with throttle rate of 3 requests per minute.
    - Allow list, retrieve, delete functions for authorized users w/ firebase_id_token.
    - *Accepts GET, POST, DELETE*