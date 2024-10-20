#!/usr/bin/env bash
set -e

main() {
  local project_path="$(pwd)"
  local output_path="${project_path}/dist"

  source "${project_path}/.venv/bin/activate"
  rm -rf "${output_path}"

  uv pip compile pyproject.toml > requirements.txt
  uv pip install \
    --no-color \
    --quiet \
    --platform manylinux2014_x86_64 \
    --implementation cp --python-version 3.12 --only-binary=:all: \
    --requirement "${project_path}/requirements.txt" \
    --target "${output_path}/layer/python"

  zip -qr "${output_path}/lambda.zip" "maverik_backend"

  cd "${output_path}/layer"
  zip -qr "${output_path}/layer.zip" .

  mkdir "${output_path}/to_publish"
  mv "${output_path}/lambda.zip" "${output_path}/to_publish/"
  mv "${output_path}/layer.zip" "${output_path}/to_publish/"

  aws s3 cp --recursive "${output_path}/to_publish" "s3://maverik-backend-s3"

  cd - &>/dev/null
}

# call main
main "${@}"
