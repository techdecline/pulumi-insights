terraform {
  after_hook "run_uv_python" {
    commands = ["apply"]
    execute = [
      "sh", "-c",
      "terraform output -json > output.json && uv run main.py --terraform-output output.json"
    ]
  }
}