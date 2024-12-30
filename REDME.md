![img.png](file_image/img.png)

Auth API:\
POST /auth/register\
POST /auth/login\
GET /auth/refresh\
GET /auth/logout

Role API:\
POST /roles\
GET /roles\
GET /roles/{role_id}\q
PUT /roles/{role_id}\
DELETE /roles/{role_id}

User API:\
GET /users/me\
GET /users/{user_id}\
GET /users/roles/{role_name}\
PATCH /users/{user_id}/role\
PATCH /users/{user_id}\
DELETE /users/{user_id}

Group API:'\
POST /groups\
GET /groups\
PUT /groups/{group_id}\
DELETE /groups/{group_id}

Speciality API:\

POST /speciality\
GET /speciality/{speciality_id}\
PATCH /speciality/{speciality_id}\
DELETE /speciality/{speciality_id}\