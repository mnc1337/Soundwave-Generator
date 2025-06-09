from flask import Flask, render_template, jsonify, request, send_file
import soundfile as sf
import numpy as np
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route("/save", methods=["GET", "POST"])
def save():
    if request.method == "POST":
        sampleRateInput = request.form.get("sampleRateInput")
        durationInput = request.form.get("durationInput")
        amplitudeInput = request.form.get("amplitudeInput")
        lowerFrequencyInput = request.form.get("lowerFrequencyInput")
        higherFrequencyInput = request.form.get("higherFrequencyInput")

        try:
            sample_rate = int(sampleRateInput)
            duration = int(durationInput)
            amplitude = float(amplitudeInput)
            freq_start = int(lowerFrequencyInput)
            freq_end = int(higherFrequencyInput)
        except Exception as e:
            return jsonify({
                "error": str(e),
            }), 500
    
        points = np.linspace(0, duration, sample_rate * duration, endpoint=False)
        frequences = np.linspace(freq_start, freq_end, len(points))
        signal = amplitude * np.sin(2 * np.pi * np.cumsum(frequences) / sample_rate)

        filename = "audio.wav"

        sf.write(filename, signal, sample_rate)

        working_dir = os.getcwd()
        full_path = os.path.join(working_dir, filename)

        return send_file(full_path, as_attachment=True)

    return render_template("save.html")

@app.route("/values_error")
def values_error():
    return render_template("values_error.html"), 400

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error_404.html"), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")