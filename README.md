## Build client

Install parcel@1.12.3

```
NODE_ENV=environment_name parcel build --no-source-maps --public-url ./ index.html
```

## Generate Http client

1. Install openapi-generator `community/openapi-generator`
2. Start server
3. `openapi-generator generate -i http://127.0.0.1:5000/apispec_1.json -g typescript-rxjs -o client/generated-api --skip-validate-spec`

## Create a new database revision

1. Install python-alembic
2. ```alembic revision -m "Name of revision"```
