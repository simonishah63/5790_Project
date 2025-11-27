#!/bin/bash

echo "🔧 Safety-Critical Verification Experimental Setup"
echo "=================================================="

# ----------------------------
# Check if Docker is running
# ----------------------------
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# ----------------------------
# Check for Docker Compose
# ----------------------------
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
else
    echo "❌ Docker Compose is not installed. Please install Docker Compose."
    exit 1
fi

echo "✅ Using Docker Compose command: $COMPOSE_CMD"

# ----------------------------
# 1. Create Python virtual environment
# ----------------------------
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi
source venv/bin/activate

# ----------------------------
# 2. Install required Python packages
# ----------------------------
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt


# ----------------------------
# 3. Build all Docker images (no cache)
# ----------------------------
echo "🐳 Building Docker images for all tools..."
$COMPOSE_CMD build --no-cache
#$COMPOSE_CMD build

# ----------------------------
# 4. Generate benchmarks
# ----------------------------
echo "📝 Generating benchmarks..."
# Run benchmark generator in the Python/tools container
$COMPOSE_CMD run --rm tools python3 src/benchmark_generator.py

echo "✅ Benchmarks generated!"

# ----------------------------
# 5. Test tool installations individually
# ----------------------------
echo "🔍 Testing tool installations..."

echo "▶ CBMC:"
$COMPOSE_CMD run --rm cbmc --version

echo "▶ Frama-C:"
$COMPOSE_CMD run --rm frama-c -version

echo "▶ Python/tools:"
$COMPOSE_CMD run --rm tools python3 --version
$COMPOSE_CMD run --rm tools python3 -c "import pandas, matplotlib, seaborn; print('Python libraries OK')"

echo "✅ All tools verified!"

# ----------------------------
# Usage instructions
# ----------------------------
echo ""
echo "🚀 To run experiments:"
echo "   source venv/bin/activate"
echo "   python3 run_experiments.py"
echo ""
echo "📊 Start Jupyter notebook for analysis:"
echo "   docker compose run -p 8888:8888 tools jupyter notebook --ip=0.0.0.0 --no-browser --allow-root"
echo ""
echo "✅ Access your analysis notebooks inside the tools container at the mapped port 8888."