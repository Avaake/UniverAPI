![img.png](file_image/img.png)

Auth API:\
POST /auth/register\
POST /auth/login\
GET /auth/refresh\
GET /auth/logout

Role API:\
POST /role\
GET /role\
GET /role/{role_id}\q
PETCH /role/{role_id}\
DELETE /role/{role_id}

User API:\
GET /users/me\
GET /users/{user_id}\
GET /users/roles/{role_name}\
PATCH /users/{user_id}/role/{role_id}
PATCH /users/{user_id}qq