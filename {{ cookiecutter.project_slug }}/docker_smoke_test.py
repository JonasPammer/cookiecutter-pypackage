"""https://pythonspeed.com/articles/test-your-docker-build/"""
from __future__ import annotations

from subprocess import CalledProcessError
from subprocess import check_call
from subprocess import check_output
from subprocess import STDOUT
from time import sleep


def _print(_: str) -> None:
    print(f"[{__file__}] {_}")


def _get_docker_logs(docker_container_id: str) -> str:
    return check_output(["docker", "logs", "docker_container_id"]).decode("utf-8")


def main() -> int:
    _print("Building local version of Docker Image...")
    check_call(
        "docker buildx build . "
        "--tag {{ cookiecutter.dockerhub_username }}/{{ cookiecutter.project_slug }}:smoke-please-ignore".split()
    )

    # FIXME: adjust run command here as needed
    #        e.g. exposing ports to be used in upcoming tests
    _print("Running local version of Docker Image in detached mode...")
    docker_container_id: str = (
        check_output(
            "docker run --detach --pull=never "
            "{{ cookiecutter.dockerhub_username }}/{{ cookiecutter.project_slug }}:smoke-please-ignore".split()
        )
        .strip()
        .decode("utf-8")
    )

    # Wait for the server to start or program to exit
    sleep(5)

    try:
        _print("FIXME: Implement actual Smoke Tests here if any!")

        # Example 1: Check output
        # assert "xyz" in _get_docker_logs(docker_container_id)

        # Example 2: Check if a http server started
        # (urlopen throws an URLError on http protocol errors):
        # urlopen("http://localhost:8080").read()
        pass
    finally:
        docker_container_entrypoint_exit_code: str = (
            check_output(
                [
                    "docker",
                    "inspect",
                    docker_container_id,
                    "--format={% raw %}{{.State.ExitCode}}{% endraw %}",
                ]
            )
            .strip()
            .decode("utf-8")
        )
        if docker_container_entrypoint_exit_code != "0":
            # raise right here so container is not killed/removed
            # in order to allow for debugging
            raise Exception(
                f"Docker Container '{docker_container_id}' exited with "
                f"{docker_container_entrypoint_exit_code}"
            )

        try:
            _print("Killing Container...")
            check_output(f"docker kill {docker_container_id}".split(), stderr=STDOUT)
            # FIXME: remove the below exception catch if the dockerfile
            #        actually shouldve actually started a server
        except CalledProcessError as ex:
            if "not running" not in ex.output.decode():
                raise ex
        finally:
            _print("Removing Container...")
            check_call(f"docker rm {docker_container_id}".split())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
