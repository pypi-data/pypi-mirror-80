from copy import deepcopy
from functools import partial
import json
import os
from typing import Any, Callable, Dict, MutableMapping, Optional

import wrapt

from anyscale.util import send_json_request


@wrapt.decorator  # type: ignore
def _with_safe_cluster_config(
    wrapped: Callable[..., MutableMapping[str, Any]],
    instance: Optional[Any],
    args: Any,
    kwargs: Any,
) -> Any:
    # for all our _configure_* functions, the first argument should be the cluster config
    def _configure(
        cluster_config: MutableMapping[str, Any], *args: Any, **kwargs: Any
    ) -> MutableMapping[str, Any]:
        cluster_config = deepcopy(cluster_config)

        return wrapped(cluster_config, *args, **kwargs)

    return _configure(*args, **kwargs)


@_with_safe_cluster_config  # type: ignore
def _configure_cluster_name(
    cluster_config: MutableMapping[str, Any], session_id: str
) -> MutableMapping[str, Any]:
    details = send_json_request("/api/v2/sessions/{}/details".format(session_id), {})[
        "result"
    ]

    cluster_config["cluster_name"] = details["cluster_name"]

    return cluster_config


@_with_safe_cluster_config  # type: ignore
def _configure_ssh_key(
    cluster_config: MutableMapping[str, Any], session_id: str,
) -> MutableMapping[str, Any]:
    ssh_key = send_json_request("/api/v2/sessions/{}/ssh_key".format(session_id), {})[
        "result"
    ]

    # TODO (yiran): cleanup SSH keys if session no longer exists.
    def _write_ssh_key(name: str, ssh_key: str) -> str:
        ssh_key_dir = os.path.expanduser("~/.ssh")
        os.makedirs(ssh_key_dir, exist_ok=True)

        key_path = os.path.join(ssh_key_dir, "{}.pem".format(name))
        with open(key_path, "w", opener=partial(os.open, mode=0o600)) as f:
            f.write(ssh_key)

        return key_path

    key_path = _write_ssh_key(ssh_key["key_name"], ssh_key["private_key"])

    cluster_config.setdefault("auth", {})["ssh_private_key"] = key_path

    # Bypass Ray's check for cloudinit key
    cluster_config["head_node"].setdefault(("UserData"), "")
    cluster_config["worker_nodes"].setdefault(("UserData"), "")
    return cluster_config


@_with_safe_cluster_config  # type: ignore
def _configure_autoscaler_credentials(
    cluster_config: MutableMapping[str, Any], session_id: str
) -> MutableMapping[str, Any]:
    credentials = send_json_request(
        "/api/v2/sessions/{}/autoscaler_credentials".format(session_id), {},
    )["result"]

    cloud_provider = cluster_config["provider"]["type"]
    cluster_config["provider"]["{}_credentials".format(cloud_provider)] = credentials[
        "credentials"
    ]

    return cluster_config


def configure_for_session(session_id: str) -> Dict[str, Any]:
    _resp: Dict[str, Any] = send_json_request(
        "/api/v2/sessions/{}/cluster_config".format(session_id), {}
    )["result"]
    cluster_config: Dict[str, Any] = json.loads(_resp["config_with_defaults"])

    cluster_config = _configure_cluster_name(cluster_config, session_id)
    cluster_config = _configure_ssh_key(cluster_config, session_id)
    cluster_config = _configure_autoscaler_credentials(cluster_config, session_id)

    return cluster_config
