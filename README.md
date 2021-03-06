## Casting Agency Flask API

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. I (Amna) created a system that simplify and streamline your process.

### Specifications:
#### Models:
1. Movies with attributes id, title and release date
2. Actors with attributes id, name, age and gender
3. Genre
4. Assistant
5. Director

![ERD](https://github.com/amnaw/Casting-Agency-Flask/blob/main/ERD.PNG)


#### Endpoints:
1. GET /actors and /movies
2. DELETE /actors/ and /movies/
3. POST /actors and /movies and
4. PATCH /actors/ and /movies/


#### Roles:
1. Casting Assistant
    - Can view actors and movies
2. Casting Director
    - All permissions a Casting Assistant has and…
    - Add or delete an actor from the database
    - Modify actors or movies
3. Executive Producer
    - All permissions a Casting Director has and…
    - Add or delete a movie from the database


#### Tests:
- One test for success behavior of each endpoint
- One test for error behavior of each endpoint
- At least two tests of RBAC for each role


### Try it out:
Authentication Instructions:
there are pre-defined users accounts each of which associated with one role, to authenticate refer to their credentials to login or the Tokens and try different endpoints using [Postman](https://www.postman.com/).

Follow this [link](https://dev-04zvrt8l.us.auth0.com/authorize?audience=Casting-Agency&response_type=token&client_id=im6QhIeQHzMYvYXFRreaakuhUutPdmlF&redirect_uri=https://casting-agency-flask.herokuapp.com/) to login

1. Casting Assistant
    - assistant@casting.agency.com
    - [24h Token](https://github.com/amnaw/Casting-Agency-Flask/blob/main/Casting%20Assistant%20Token.txt)
2. Casting Director
    - director@casting.agency.com
    - [24h Token](https://github.com/amnaw/Casting-Agency-Flask/blob/main/Casting%20Director%20Token.txt)
3. Executive Producer
    - producer@casting.agency.com
    - [24h Token](https://github.com/amnaw/Casting-Agency-Flask/blob/main/Executive%20Producer%20Token.txt)

passwoed: Password1*

The password is the same for all.



