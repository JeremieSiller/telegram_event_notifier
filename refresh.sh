# Exchange a refresh token for a new access token.
curl \
--request POST \
--data 'client_id=8187b1956521b380a86c2e054f4f10e80e3f737f6474eda1480f00bdc4fa8c05&client_secret=497f9a7249f1494fbb46cb6e1a53c131928d662aec21029a7e3503267793b6d6&refresh_token=b3f4470ce1ccc0255ecf6a93de45a87f7c57bf18cf2813b8b9534f3d854a7f8a&grant_type=refresh_token' \
http://localhost:8070