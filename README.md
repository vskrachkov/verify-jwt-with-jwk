###Usage
``` 
JWT=eyJhbGciOiJSUYxNWY2YIn0.eyJpmYxNWY.zI1NiIsImtpZCI6Im.very.long.string..
JWK_SET_ENDPOINT=http://<identity-server>/openid/jwks
python verify.py $JWT $JWK_SET_ENDPOINT
```