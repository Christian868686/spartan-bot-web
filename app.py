from flask import Flask, render_template_string, jsonify
import scraper
import ia_avancada
import config
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template_string(open("templates/index.html").read())

@app.route("/api/status")
def status():
    try:
        df = pd.read_csv("data/historico.csv")
        win_loss = json.load(open("data/win_loss.json"))
        win = win_loss["win"]
        loss = win_loss["loss"]
        taxa = round(win / (win + loss) * 100, 2) if win + loss > 0 else 0
        ultimo = df.iloc[-1]["multiplicador"] if not df.empty else "--"
        chance = ia_avancada.prever(df) * 100 if not df.empty else 0
        return jsonify({
            "status": "Online" if not df.empty else "Offline",
            "win": win,
            "loss": loss,
            "taxa": taxa,
            "ultimo": float(ultimo) if isinstance(ultimo, (int, float)) else 0,
            "chance": chance
        })
    except Exception as e:
        return jsonify({
            "status": "Offline",
            "win": 0,
            "loss": 0,
            "taxa": 0,
            "ultimo": "--",
            "chance": 0
        })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)