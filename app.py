"""HondaForge - AI Honda customizer.  Run with:  streamlit run app.py

Tabs: 2D Studio (studio-style render), 3D Viewer (three.js), AI Real Photo
(photoreal image of YOUR build), AI Assistant (chat), Stats & Advice.
"""
import base64
import json
import os
import pathlib
import streamlit as st
import streamlit.components.v1 as components

HERE = pathlib.Path(__file__).parent
ASSETS = HERE / "assets"
SAVE_FILE = HERE / "builds.json"

MODELS = {
    "civic": ("Civic", 170, 8.2), "city": ("City", 119, 10.5),
    "accord": ("Accord", 190, 7.6), "hrv": ("HR-V", 140, 10.8), "jazz": ("Jazz", 100, 11.5),
    "crv": ("CR-V", 190, 9.5), "brv": ("BR-V", 119, 12.0), "amaze": ("Amaze", 90, 13.0), "brio": ("Brio", 90, 13.5),
}
COLORS = ["Platinum White Pearl", "Rallye Red", "Crystal Black Pearl", "Aegean Blue",
          "Modern Steel Metallic", "Lunar Silver", "Meteoroid Gray", "Phoenix Orange"]
# option lists: (label, price in PKR thousands). Order must match the JS arrays.
OPT = {
    "fin": [("Gloss", 0), ("Matte wrap", 90)],
    "kit": [("Stock", 0), ("Sport", 85), ("Aggressive", 160)],
    "spo": [("None", 0), ("Lip", 15), ("Ducktail", 25), ("GT wing", 55)],
    "light": [("Stock halogen", 0), ("LED white", 35), ("Ice blue LED", 40), ("Amber DRL", 40)],
    "tint": [("Clear", 0), ("Factory", 0), ("Dark", 12), ("Limo", 15)],
    "str": [("None", 0), ("White side stripe", 20), ("Black side stripe", 20), ("Red side stripe", 25)],
    "roof": [("Body colour", 0), ("Gloss black", 45), ("Carbon", 120)],
    "ug": [("Off", 0), ("Ice blue", 25), ("Red", 25), ("Purple", 25), ("Green", 25)],
    "rim": [("Stock 5-spoke", 0), ("Multi-spoke", 120), ("Mesh", 160), ("Turbine", 190)],
    "rimc": [("Silver", 0), ("Black", 0), ("Gold", 0), ("Bronze", 0)],
    "size": [("16 inch", 0), ("17 inch", 30), ("18 inch", 60), ("19 inch", 90)],
    "cal": [("Red", 0), ("Yellow", 12), ("Blue", 12), ("Black", 8)],
    "dash": [("Stock", 0), ("Carbon", 30), ("Wood", 35), ("Red", 30)],
    "seat": [("Fabric", 0), ("Black leather", 85), ("Red leather", 95), ("Tan leather", 95), ("Blue leather", 95)],
    "steer": [("Stock", 0), ("Sport stitched", 25), ("Flat carbon", 45)],
    "amb": [("Off", 0), ("Red", 15), ("Blue", 15), ("Purple", 15), ("Green", 15)],
    "eng": [("Stock", 0), ("Stage 1 intake + exhaust", 90), ("Stage 2 ECU tune", 190), ("Turbo kit", 650)],
    "gear": [("Stock", 0), ("Short shifter", 22), ("Close-ratio gears", 140)],
}
LABEL = {"fin": "Finish", "kit": "Body kit and side skirts", "spo": "Spoiler", "light": "Headlights",
         "tint": "Window tint", "str": "Stripes", "roof": "Roof", "ug": "Underglow", "rim": "Rim style",
         "rimc": "Rim colour", "size": "Rim size", "cal": "Brake calipers", "dash": "Dashboard trim",
         "seat": "Seat covers", "steer": "Steering wheel", "amb": "Ambient light", "eng": "Engine",
         "gear": "Gear setup"}
SCENES = ["Studio", "Night city", "Sunset"]
GOALS = ["Daily drive", "Street look", "Track day", "Luxury cruiser"]
BUDGETS = [("PKR 300k", 3e5), ("PKR 600k", 6e5), ("PKR 1M", 1e6), ("PKR 2M", 2e6), ("No limit", 1e12)]
DEF = {"model": "civic", "color": 0, "drop": 0, "goal": 0, "bud": 4, "scene": 0, **{k: 0 for k in OPT}}
DEF["tint"] = 1  # factory tint
PRESETS = [  # one per goal
    dict(color=0, kit=0, spo=1, light=1, drop=2, rim=1, rimc=0, size=1, dash=0, seat=1, steer=0, amb=2, eng=0, gear=0),
    dict(color=4, kit=1, spo=2, light=2, drop=9, rim=2, rimc=3, size=2, dash=1, seat=2, steer=1, amb=1, eng=1, gear=1),
    dict(color=1, kit=2, spo=3, light=1, drop=8, rim=0, rimc=1, size=1, dash=1, seat=1, steer=2, amb=0, eng=2, gear=2),
    dict(color=2, kit=1, spo=1, light=1, drop=3, rim=3, rimc=0, size=2, dash=2, seat=3, steer=0, amb=3, eng=0, gear=0),
]
WEIGHTS = [dict(c=.5, l=.2, p=.15, h=.15), dict(c=.1, l=.5, p=.2, h=.2),
           dict(c=.1, l=.1, p=.4, h=.4), dict(c=.45, l=.4, p=.15, h=0)]

# ----------------------------------------------------------- build logic
def current_build():
    return {k: st.session_state[k] for k in DEF}


def cost(b):
    total = (60 if b["color"] else 0) + (120 if b["drop"] else 0)  # repaint / coilovers
    total += sum(OPT[k][b[k]][1] for k in OPT)
    return total * 1000


def stats(b):
    e, g, d, c = b["eng"], b["gear"], b["drop"], lambda v: int(max(0, min(100, round(v))))
    power = 40 + [0, 12, 25, 45][e] + [0, 3, 8][g]
    handling = 45 + d * 1.6 + b["size"] * 3 + [0, 4, 8][b["kit"]] + [0, 2, 3, 6][b["spo"]] - max(0, d - 10) * 3
    comfort = (80 - d * 2.2 - b["size"] * 3 - (4 if b["kit"] == 2 else 0) - e * 2.5
               + (6 if b["seat"] else 0) + (3 if b["amb"] else 0))
    looks = (25 + (6 if b["color"] else 0) + (5 if b["fin"] else 0) + [0, 10, 16][b["kit"]]
             + [0, 5, 8, 10][b["spo"]] + [0, 8, 12, 14][b["rim"]] + b["size"] * 3 + (6 if b["light"] else 0)
             + d * 1.3 + (4 if b["seat"] else 0) + (3 if b["dash"] else 0) + (3 if b["steer"] else 0)
             + (4 if b["amb"] else 0)) * 1.15
    return {"Power": c(power), "Handling": c(handling), "Comfort": c(comfort), "Looks": c(looks)}


def rating(b):
    s, w = stats(b), WEIGHTS[b["goal"]]
    return int(round(s["Comfort"] * w["c"] + s["Looks"] * w["l"] + s["Power"] * w["p"] + s["Handling"] * w["h"]))


def performance(b):
    _, hp0, t0 = MODELS[b["model"]]
    hp = round(hp0 * [1, 1.06, 1.15, 1.4][b["eng"]] * (1.01 if b["gear"] == 2 else 1))
    t = t0 * (hp0 / hp) ** 0.85 - 0.15 * b["gear"]
    return hp, round(t, 1)


def advice(b):
    out, c, budget = [], cost(b), BUDGETS[b["bud"]][1]
    suv = b["model"] in ("hrv", "jazz", "crv", "brv", "brio")
    if c > budget:
        out.append(("warn", f"You are PKR {int(c - budget):,} over budget. Cut the priciest items first (turbo, 19 inch wheels, aggressive kit)."))
    if b["eng"] == 3 and b["gear"] == 0:
        out.append(("warn", "A turbo adds a lot of torque. The stock clutch and gearbox will wear fast, so add close-ratio gears and a proper ECU tune."))
    if b["kit"] == 2 and b["drop"] < 4:
        out.append(("info", "The aggressive kit looks best on a lowered car. Try a drop of 6 to 10."))
    if b["goal"] == 0 and b["drop"] > 8:
        out.append(("warn", "A drop this big will scrape on speed breakers and rough roads. Keep it under 6 for daily driving."))
    if b["goal"] == 0 and b["size"] == 3:
        out.append(("warn", "19 inch wheels with thin tyres ride harsh. 17 inch is the comfort sweet spot."))
    if b["goal"] == 2 and b["eng"] == 0:
        out.append(("info", "For track days, start with Stage 1 (intake + exhaust) before anything cosmetic."))
    if b["goal"] == 2 and b["spo"] == 0:
        out.append(("info", "Add a ducktail or GT wing for stability at speed."))
    if b["goal"] == 3 and not b["amb"]:
        out.append(("info", "Ambient lighting and leather seats give the biggest luxury feel for the money."))
    if b["goal"] == 1 and not b["light"]:
        out.append(("info", "LED headlights are the cheapest big upgrade for a street look."))
    if suv and b["spo"] == 3:
        out.append(("warn", "A GT wing looks out of place on this body. Use a lip spoiler instead."))
    if b["color"] == 0 and b["rimc"] == 2:
        out.append(("ok", "Gold wheels on a white car is a classic JDM pairing."))
    if b["color"] == 2 and b["rimc"] == 1:
        out.append(("info", "Black wheels on a black body look stealthy but lose contrast. Bronze or gold would pop."))
    if b["fin"] and b["goal"] == 3:
        out.append(("info", "Gloss paint suits a luxury build better than matte."))
    if b["ug"] or b["eng"] >= 2:
        out.append(("info", "Check local rules: underglow and engine or exhaust changes can fail inspection or affect warranty."))
    return out[:7] or [("ok", "This build is balanced. Nice work.")]


def describe(b):
    d = {"model": "Honda " + MODELS[b["model"]][0], "paint": COLORS[b["color"]], "ride_drop": b["drop"],
         "goal": GOALS[b["goal"]], "budget": BUDGETS[b["bud"]][0]}
    d.update({LABEL[k]: OPT[k][b[k]][0] for k in OPT})
    return d


def spec_sheet(b):
    hp, t = performance(b)
    lines = ["HONDAFORGE BUILD SHEET", "=" * 30]
    lines += [f"{k}: {v}" for k, v in describe(b).items()]
    lines += ["", f"Estimated cost: PKR {cost(b):,}", f"Approx power: {hp} hp, 0-100 km/h {t}s (estimate)",
              "Stats: " + ", ".join(f"{k} {v}" for k, v in stats(b).items())]
    return "\n".join(lines)


def photo_prompt(b):
    drop = ["", "slightly lowered, ", "lowered stance, ", "very low stance, "][min(3, b["drop"] // 4)]
    finish = "matte wrapped" if b["fin"] else "glossy"
    parts = [f"Ultra realistic automotive photograph of a {drop}modified Honda {MODELS[b['model']][0]}",
             f"in {finish} {COLORS[b['color']]} paint"]
    if b["kit"]: parts.append(f"{OPT['kit'][b['kit']][0].lower()} body kit with side skirts and front lip")
    if b["spo"]: parts.append(f"{OPT['spo'][b['spo']][0].lower()} spoiler")
    parts.append(f"{OPT['size'][b['size']][0]} {OPT['rimc'][b['rimc']][0].lower()} {OPT['rim'][b['rim']][0].lower()} alloy wheels with {OPT['cal'][b['cal']][0].lower()} brake calipers")
    if b["light"]: parts.append(f"{OPT['light'][b['light']][0].lower()} headlights")
    if b["tint"] >= 2: parts.append(f"{OPT['tint'][b['tint']][0].lower()} tinted windows")
    if b["str"]: parts.append(OPT["str"][b["str"]][0].lower())
    if b["roof"]: parts.append(f"{OPT['roof'][b['roof']][0].lower()} roof")
    if b["ug"]: parts.append(f"{OPT['ug'][b['ug']][0].lower()} underglow")
    scene = ["in a clean white photo studio", "on a neon-lit city street at night", "at golden hour sunset on an empty road"][b["scene"]]
    return ", ".join(parts) + f", three-quarter front view, {scene}, 85mm lens, sharp detail, 8k, professional car magazine shoot"


# ---------------------------------------------------------------- AI
SYSTEM = ("You are HondaForge AI, a friendly and honest car-modification advisor for Honda owners, "
          "mostly in Pakistan. Give concise, practical advice. Mention trade-offs, safety, legal or inspection "
          "issues and warranty impact when relevant. Prices are rough PKR estimates. The user's current build:\n{build}")


def offline_answer(q, b):
    q = q.lower()
    name = MODELS[b["model"]][0]
    if "spoiler" in q:
        return f"On a {name}, a lip or ducktail spoiler looks clean and is cheap. A GT wing suits track builds but can hurt resale on daily cars."
    if any(w in q for w in ("rim", "wheel", "tyre", "tire")):
        return "17 inch is the best balance of looks and comfort. 18 to 19 inch looks sharper but rides harsher on rough roads. Bronze or gold rims pop on white, black or grey paint."
    if any(w in q for w in ("colour", "color", "paint")):
        return "Rallye Red and Platinum White are the classic Honda looks. Crystal Black Pearl and Modern Steel look sporty and hide dust better, and matte wraps need extra care."
    if any(w in q for w in ("engine", "turbo", "power", "tune")):
        return "Start with Stage 1 (intake + exhaust), then an ECU tune. Go turbo only if you also upgrade clutch, cooling and brakes. Always check warranty and inspection rules first."
    if any(w in q for w in ("budget", "cheap", "save")):
        return "Best value upgrades are LED headlights, a lip spoiler, rim colour or size and tinted windows. Save the turbo and big body kits for later."
    if any(w in q for w in ("daily", "comfort")):
        return "For daily use, keep the drop under 6, stay at 17 inch wheels and skip the aggressive kit. Seat covers and ambient lighting add comfort for little money."
    return "Here is what I would check on this build: " + " ".join(t for _, t in advice(b)[:2])


def ask_ai(history, b):
    key = os.getenv("ANTHROPIC_API_KEY")
    if not key:
        return offline_answer(history[-1]["content"], b) + "\n\n_(Offline mode.)_"
    import anthropic
    resp = anthropic.Anthropic(api_key=key).messages.create(
        model=os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5"), max_tokens=700,
        system=SYSTEM.format(build=json.dumps(describe(b))), messages=history) 
    return resp.content[0].text


def make_photo(prompt):
    from huggingface_hub import InferenceClient
    client = InferenceClient(token=os.getenv("HF_TOKEN"))
    return client.text_to_image(prompt, model=os.getenv("PHOTO_MODEL", "black-forest-labs/FLUX.1-schnell"))


# ------------------------------------------------------------ rendering
def render(template, b, extra=None):
    html = (ASSETS / template).read_text(encoding="utf-8")
    html = html.replace("/*DATA*/", (ASSETS / "data.js").read_text(encoding="utf-8"))
    html = html.replace("/*R2D*/", (ASSETS / "render2d.js").read_text(encoding="utf-8"))
    glb = ASSETS / "models" / f"{b['model']}.glb"  # optional real 3D model
    html = html.replace("__GLB__", json.dumps(base64.b64encode(glb.read_bytes()).decode() if glb.exists() else None))
    return html.replace("__BUILD__", json.dumps({**b, **(extra or {})}))


def load_slots():
    try:
        return json.loads(SAVE_FILE.read_text())
    except Exception:
        return {}


def apply(values):
    st.session_state.update(values)


# ------------------------------------------------------------------ UI
st.set_page_config(page_title="HondaForge", page_icon="🏎️", layout="wide")
for k, v in DEF.items():
    st.session_state.setdefault(k, v)


def pick(k):
    st.selectbox(LABEL[k], range(len(OPT[k])), format_func=lambda i, k=k: OPT[k][i][0], key=k)


with st.sidebar:
    st.title("HondaForge")
    st.selectbox("Model", list(MODELS), format_func=lambda k: "Honda " + MODELS[k][0], key="model")
    with st.expander("Exterior", expanded=True):
        st.selectbox("Paint", range(len(COLORS)), format_func=lambda i: COLORS[i], key="color")
        for k in ("fin", "kit", "spo", "light", "tint", "str", "roof", "ug"):
            pick(k)
        st.slider("Ride height drop", 0, 14, key="drop")
    with st.expander("Wheels and brakes"):
        for k in ("rim", "rimc", "size", "cal"):
            pick(k)
    with st.expander("Interior"):
        for k in ("dash", "seat", "steer", "amb"):
            pick(k)
    with st.expander("Performance"):
        for k in ("eng", "gear"):
            pick(k)
    st.selectbox("Backdrop", range(3), format_func=lambda i: SCENES[i], key="scene")
    st.divider()
    slot = st.radio("Garage slot", [1, 2, 3], horizontal=True)
    c1, c2 = st.columns(2)
    slots = load_slots()
    if c1.button("Save build"):
        slots[str(slot)] = current_build()
        SAVE_FILE.write_text(json.dumps(slots))
        st.toast(f"Saved to slot {slot}")
    c2.button("Load build", disabled=str(slot) not in slots, on_click=apply, args=(slots.get(str(slot), {}),))
    st.button("Reset to stock", on_click=apply, args=({**DEF, "model": st.session_state["model"]},))

b = current_build()
hp, t100 = performance(b)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Honda " + MODELS[b["model"]][0], COLORS[b["color"]])
m2.metric("Estimated mod cost", f"PKR {cost(b):,}")
m3.metric("Power (approx)", f"{hp} hp")
m4.metric("0-100 km/h (approx)", f"{t100} s")

t2d, t3d, tphoto, tchat, tstats = st.tabs(
    ["2D Studio", "3D Viewer", "AI Real Prompt", "AI Assistant", "Stats and Advice"])

with t2d:
    c1, c2, c3 = st.columns(3)
    view = c1.radio("View", ["exterior", "interior"], horizontal=True)
    compare = c2.checkbox("Before / after slider")
    roll = c3.checkbox("Roll wheels")
    components.html(render("viewer2d.html", b, {"view": view, "cmp": int(compare), "spin": roll}), height=440)

with t3d:
    roll3 = st.checkbox("Spin wheels", key="roll3")
    components.html(render("viewer3d.html", b, {"spin": roll3}), height=510)
    st.caption("Procedural 3D model: drag to orbit, scroll to zoom. Covers paint, finish, tint, rims, body kit, spoiler, lights, ride height and underglow.")

with tphoto:
    st.write("Turn your build into a photorealistic image with an AI image model. Edit the prompt if you like.")
    prompt = st.text_area("Prompt", photo_prompt(b), height=130, key=f"prompt_{hash(photo_prompt(b))}")


with tchat:
    st.session_state.setdefault("chat", [])
    for msg in st.session_state.chat:
        st.chat_message(msg["role"]).write(msg["content"])
    if q := st.chat_input("Ask anything: What spoiler suits a white Civic? Is a turbo worth it?"):
        st.session_state.chat.append({"role": "user", "content": q})
        st.chat_message("user").write(q)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    ans = ask_ai(st.session_state.chat, b)
                except Exception as e:
                    ans = f"The AI service had a problem ({e}). Offline tip: " + offline_answer(q, b)
            st.write(ans)
        st.session_state.chat.append({"role": "assistant", "content": ans})

with tstats:
    st.selectbox("What is this car for?", range(len(GOALS)), format_func=lambda i: GOALS[i], key="goal")
    st.selectbox("Budget", range(len(BUDGETS)), format_func=lambda i: BUDGETS[i][0], key="bud")
    st.button(f"Auto-build for {GOALS[b['goal']]}", on_click=apply, args=(PRESETS[b["goal"]],))
    st.subheader(f"Build rating for this goal: {rating(b)}/100")
    cols = st.columns(4)
    for col, (name, val) in zip(cols, stats(b).items()):
        col.write(f"**{name}** {val}")
        col.progress(val / 100)
    for level, text in advice(b):
        {"warn": st.warning, "info": st.info, "ok": st.success}[level](text)
    rows = [{"Part": LABEL[k], "Choice": OPT[k][b[k]][0], "PKR": OPT[k][b[k]][1] * 1000} for k in OPT]
    st.dataframe(rows, use_container_width=True, hide_index=True)
    st.download_button("Download build sheet", spec_sheet(b), file_name="hondaforge_build.txt")
    st.caption("Prices and performance numbers are rough estimates for planning, not quotes.")
