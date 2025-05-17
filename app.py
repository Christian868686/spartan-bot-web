@app.route("/api/status")
def status_api():
    try:
        df = pd.read_csv("data/historico.csv")
        win_loss = json.load(open("data/win_loss.json"))
        win = win_loss["win"]
        loss = win_loss["loss"]
        taxa = round(win / (win + loss) * 100, 2) if win + loss > 0 else 0
        ultimo = df.iloc[-1]["multiplicador"] if not df.empty else "--"

        return jsonify({
            "status": "Online" if not df.empty else "Offline",
            "win": win,
            "loss": loss,
            "taxa": taxa,
            "ultimo": float(ultimo) if isinstance(ultimo, (int, float)) else 0,
            "chance": 0  # Você pode atualizar isso com base no último modelo
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