from flask import Flask, render_template, request
import os
app = Flask(__name__)


def diagnose(params):
    """
    Very simple rule-based diagnostic engine.
    In real life this would be our ML model inference.
    """
    issues = []

    engine_temp = params["engine_temp"]
    oil_pressure = params["oil_pressure"]
    battery_voltage = params["battery_voltage"]
    vibration_level = params["vibration_level"]
    brake_wear = params["brake_wear"]
    coolant_level = params["coolant_level"]
    km_since_service = params["km_since_service"]

    # Engine overheating
    if engine_temp > 110 and coolant_level < 40:
        issues.append({
            "component": "Engine cooling system",
            "severity": "High",
            "reason": f"High engine temp ({engine_temp}°C) and low coolant level ({coolant_level}%).",
            "action": "Immediate service recommended. Possible coolant leak, faulty pump or thermostat."
        })
    elif engine_temp > 100:
        issues.append({
            "component": "Engine",
            "severity": "Medium",
            "reason": f"Engine temp is elevated at {engine_temp}°C.",
            "action": "Check coolant level, radiator and fan. Avoid long idling in traffic."
        })

    # Oil system issues
    if oil_pressure < 1.2 and km_since_service > 8000:
        issues.append({
            "component": "Lubrication / Oil system",
            "severity": "High",
            "reason": f"Low oil pressure ({oil_pressure} bar) and high distance since last service ({km_since_service} km).",
            "action": "Change oil and filter immediately. Possible pump or blockage issue."
        })
    elif oil_pressure < 1.5:
        issues.append({
            "component": "Oil system",
            "severity": "Medium",
            "reason": f"Oil pressure is on the lower side ({oil_pressure} bar).",
            "action": "Check oil level and quality at next service."
        })

    # Battery / charging issues
    if battery_voltage < 11.8:
        issues.append({
            "component": "Battery / Charging system",
            "severity": "High",
            "reason": f"Battery voltage is very low ({battery_voltage} V).",
            "action": "Check battery health and alternator. Risk of no-start condition."
        })
    elif battery_voltage < 12.2:
        issues.append({
            "component": "Battery",
            "severity": "Medium",
            "reason": f"Battery voltage is slightly low ({battery_voltage} V).",
            "action": "Monitor starting behavior. Consider battery test."
        })
    elif battery_voltage > 14.8:
        issues.append({
            "component": "Alternator / Regulator",
            "severity": "High",
            "reason": f"Charging voltage is unusually high ({battery_voltage} V).",
            "action": "Possible regulator fault. Risk of battery damage."
        })

    # Drivetrain / mechanical vibration
    if vibration_level > 1.2:
        issues.append({
            "component": "Drivetrain / Suspension",
            "severity": "High",
            "reason": f"Excessive vibration level detected ({vibration_level} g).",
            "action": "Check wheel balance, suspension components and mounts."
        })
    elif vibration_level > 0.8:
        issues.append({
            "component": "Chassis / Tyres",
            "severity": "Medium",
            "reason": f"Vibration is higher than normal ({vibration_level} g).",
            "action": "Inspect tyres and alignment during next visit."
        })

    # Brakes
    if brake_wear > 80:
        issues.append({
            "component": "Brake pads",
            "severity": "High",
            "reason": f"Brake pad wear is {brake_wear}%.",
            "action": "Replace pads as soon as possible to maintain braking performance."
        })
    elif brake_wear > 60:
        issues.append({
            "component": "Brake pads",
            "severity": "Medium",
            "reason": f"Brake pad wear is {brake_wear}%.",
            "action": "Plan pad replacement in upcoming service."
        })

    # Service interval
    if km_since_service > 15000:
        issues.append({
            "component": "General maintenance",
            "severity": "Medium",
            "reason": f"{km_since_service} km since last service.",
            "action": "Overdue for general service. Fluids and filters may be degraded."
        })
    elif km_since_service > 10000:
        issues.append({
            "component": "General maintenance",
            "severity": "Low",
            "reason": f"{km_since_service} km since last service.",
            "action": "Plan regular service soon."
        })

    # If nothing found
    if not issues:
        issues.append({
            "component": "No critical issues detected",
            "severity": "Low",
            "reason": "All monitored parameters are within normal range.",
            "action": "Continue normal use. Re-check after some time or before long trips."
        })

    return issues


@app.route("/", methods=["GET", "POST"])
def index():
    issues = None

    # Default slider values
    defaults = {
        "engine_temp": 90,
        "oil_pressure": 2.5,
        "battery_voltage": 12.5,
        "vibration_level": 0.5,
        "brake_wear": 30,
        "coolant_level": 80,
        "km_since_service": 6000
    }

    if request.method == "POST":
        params = {
            "engine_temp": float(request.form.get("engine_temp")),
            "oil_pressure": float(request.form.get("oil_pressure")),
            "battery_voltage": float(request.form.get("battery_voltage")),
            "vibration_level": float(request.form.get("vibration_level")),
            "brake_wear": float(request.form.get("brake_wear")),
            "coolant_level": float(request.form.get("coolant_level")),
            "km_since_service": float(request.form.get("km_since_service")),
        }
        issues = diagnose(params)
    else:
        params = defaults

    return render_template("index.html", issues=issues, params=params)


if __name__ == "__main__":
    app.run(debug=True)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
