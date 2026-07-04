import subprocess

def download(dataset_url, out_path):
    try:
        dataset_url = dataset_url.strip().strip("\"'")
        result = subprocess.run(
            ["./datahugger", "download", dataset_url, "--to", out_path],
            capture_output=True,
            text=True,
            check=True,
            timeout=300,
        )

        print("✓ Download complete")
        if result.stdout:
            print(result.stdout)

    except FileNotFoundError:
        print("✗ datahugger executable not found")
        print("Check that ./datahugger exists or use 'datahugger' if it is installed on PATH.")

    except subprocess.TimeoutExpired as exc:
        print("✗ Download timed out")
        if exc.stdout:
            print(exc.stdout)
        if exc.stderr:
            print(exc.stderr)

    except subprocess.CalledProcessError as exc:
        print(f"✗ datahugger failed with exit code {exc.returncode}")

        if exc.stdout:
            print("stdout:")
            print(exc.stdout)

        if exc.stderr:
            print("stderr:")
            print(exc.stderr)

    except Exception as exc:
        print(f"✗ Unexpected error: {type(exc).__name__}: {exc}")
