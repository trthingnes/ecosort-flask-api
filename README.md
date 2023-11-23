# ecosort-flask-api

Flask API used for project in BTM481 Business Solutions with AI @ KAIST

## Run locally

1. Install the packages listed in the `Dockerfile` run commands.

2. Create a file named `.env` in the project root and add following content to it:
   ```js
   AZURE_OPENAI_API_ENDPOINT=
   AZURE_OPENAI_API_KEY=
   AZURE_OPENAI_API_VERSION=2023-05-15
   ```

3. Run `python api.py` to start the API.

## Deploy to Kyma

1. Save the `kubeconfig.yml` file belonging to your Kyma environment as `Users/<Username>/.kube/config`.

2. Install `kubectl`, `krew` and `oidc-login`.

3. In the `resources` folder, make a copy of `deployment.yaml` called `deployment-with-env.yaml` and insert URL and key to Azure.

4. Select the correct namespace for the project by running `kubectl config set-context --current --namespace=kaist-ecosort`.

5. From the project root run `kubectl apply -f ./resources/deployment-with-env.yaml`
