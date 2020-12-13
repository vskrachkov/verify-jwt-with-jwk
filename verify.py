import json
import pprint
from http.client import HTTPResponse
from typing import cast, Optional
from urllib.request import urlopen

import jwt
import typer


def main(
    token: str = typer.Argument(..., help="JSON Web Token."),
    jwk_set_endpoint: str = typer.Argument(
        ...,
        help="This endpoint will contain the JSON Web Keys used to sign all issued JWTs.",
    ),
) -> None:
    try:
        jwk: Optional[dict] = get_jwk(token, jwk_set_endpoint)
        payload = decode(token, jwk)
    except Exception as exc:
        typer.secho(
            f"[Error] {exc.__class__.__name__}: {exc}",
            fg=typer.colors.RED,
        )
        typer.Exit(1)
    else:
        typer.secho(
            f"JWT Payload: {pprint.pformat(payload, indent=4)}",
            fg=typer.colors.GREEN,
        )


def get_jwk(token: str, jwk_set_endpoint: str) -> Optional[dict]:
    kid = jwt.get_unverified_header(token)["kid"]
    response: HTTPResponse = urlopen(jwk_set_endpoint)
    body: bytes = response.read()
    parsed = cast(dict, json.loads(body.decode("utf8")))
    keys = parsed["keys"]

    jwk: Optional[dict] = None
    for jwk in keys:
        if jwk["kid"] == kid:
            jwk = jwk
            break

    return jwk


def decode(token, jwk) -> dict:
    key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))
    payload = jwt.decode(
        token, key=key, algorithms=["RS256"], options={"verify_aud": False}
    )
    return payload


if __name__ == "__main__":
    typer.run(main)
