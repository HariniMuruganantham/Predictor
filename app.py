from flask import Flask, jsonify
import datetime, random, os

app = Flask(__name__)

def fake_pipeline_run():
    return {
        "id": random.randint(1000, 9999),
        "branch": "develop",
        "status": random.choice(["success", "failed", "success", "success"]),
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "duration_seconds": random.randint(45, 300)
    }

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/pipelines')
def pipelines():
    return jsonify([fake_pipeline_run() for _ in range(10)])

@app.route('/pipelines/failed')
def failed_pipelines():
    all_runs = [fake_pipeline_run() for _ in range(20)]
    failed = [r for r in all_runs if r['status'] == 'failed']
    return jsonify(failed)

@app.route('/config')
def config():
    log_level = os.environ.get('LOG_LEVEL', 'info')
    return jsonify({"log_level": log_level})

@app.route('/')
def home():
    return jsonify({
        "message": "Pipeline API is running",
        "endpoints": [
            "/health",
            "/pipelines",
            "/pipelines/failed",
            "/config"
        ]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
