import os
from typing import Optional

AWS_PROFILE = None

ANYSCALE_PRODUCTION_NAME = "anyscale-prod.dev"

if "ANYSCALE_HOST" in os.environ:
    ANYSCALE_HOST = os.environ["ANYSCALE_HOST"]
elif os.environ.get("DEPLOY_ENVIRONMENT") == "staging":
    ANYSCALE_HOST = "https://anyscale-staging.dev"
else:
    # The production server.
    ANYSCALE_HOST = "https://" + ANYSCALE_PRODUCTION_NAME

# Global variable that contains the server session token.
CLI_TOKEN: Optional[str] = None

TEST_MODE = False
TEST_V2 = False

USER_SSH_KEY_FORMAT = "anyscale-user-{creator_id}_{region}"
