if [[ $(uname -m) == 'arm64' ]]; then
	echo "Building dockerfile on ARM with linux support..."
	docker build -t nlattice:v1.0 --platform linux/arm64/v8 .
else
	echo "Building dockerfile with standard linux support..."
	docker build -t nlattice:v1.0
fi