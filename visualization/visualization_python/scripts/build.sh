build_wheel() {
maturin build --release --target "$1" -i 3.11
}

build_manylinux() {
  cd ..
  docker run --rm -v "$(pwd)":"$(pwd)" -w "$(pwd)"/visualization_python ghcr.io/pyo3/maturin build --release -i 3.11
  cd - > /dev/null
}

echo "Clear wheels directory!"
rm -f wheels/*

echo "Building wheels!"
build_wheel x86_64-pc-windows-msvc
build_manylinux

echo "Collecting wheels!"
mv target/wheels/* wheels