def accesstoken_from_impersonated_credentials(
    impersonated_service_account: str, scope: str
):
    from google.auth import impersonated_credentials
    import google.auth.transport.requests

    """
      Use a service account (SA1) to impersonate another service account (SA2)
      and obtain an ID token for the impersonated account.
      To obtain a token for SA2, SA1 should have the
      "roles/iam.serviceAccountTokenCreator" permission on SA2.

    Args:
        impersonated_service_account: The name of the privilege-bearing service account for whom the credential is created.
            Examples: name@project.service.gserviceaccount.com

        scope: Provide the scopes that you might need to request to access Google APIs,
            depending on the level of access you need.
            For this example, we use the cloud-wide scope and use IAM to narrow the permissions.
            https://cloud.google.com/docs/authentication#authorization_for_services
            For more information, see: https://developers.google.com/identity/protocols/oauth2/scopes
    """

    # Construct the GoogleCredentials object which obtains the default configuration from your
    # working environment.
    credentials, project_id = google.auth.default()

    # Create the impersonated credential.
    target_credentials = impersonated_credentials.Credentials(
        source_credentials=credentials,
        target_principal=impersonated_service_account,
        # delegates: The chained list of delegates required to grant the final accessToken.
        # For more information, see:
        # https://cloud.google.com/iam/docs/create-short-lived-credentials-direct#sa-credentials-permissions
        # Delegate is NOT USED here.
        delegates=[],
        target_scopes=[scope],
        lifetime=300,
    )

    # Get the OAuth2 token.
    # Once you've obtained the OAuth2 token, use it to make an authenticated call
    # to the target audience.
    request = google.auth.transport.requests.Request()
    target_credentials.refresh(request)
    return target_credentials
