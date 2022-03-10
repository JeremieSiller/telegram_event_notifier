# Exchange a refresh token for a new access token.
curl \
--request POST \
--data 'client_id=8187b1956521b380a86c2e054f4f10e80e3f737f6474eda1480f00bdc4fa8c05&client_secret=497f9a7249f1494fbb46cb6e1a53c131928d662aec21029a7e3503267793b6d6&refresh_token=79e1cb8d8b7e66aa3e19f82e2ab185946c67f03e280fa7d9ca5eb701bb4a8087&grant_type=refresh_token' \
https://api.intra.42.fr/oauth/token