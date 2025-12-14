import streamlit as st
import re
import statistics

# --- Helper Functions ---
def extract_wr(weapon_str):
    match = re.search(r'WR\s*(\d+)', weapon_str)
    return int(match.group(1)) if match else 0

def get_mod(score, table, per=1, start=21):
    if score < start:
        return table[score - 1]
    return table[start - 2] + ((score - (start - 1)) // per)

# --- Title ---
st.title("Fiendish Fate Monster Builder")

# --- Monster Basics ---
st.header("Monster Basics")
name = st.text_input("Monster Name", "Unnamed Monster")
level = st.number_input("Level", 1, 100, 10)
creature_type = st.selectbox("Creature Type", [
    "Abyssal", "Beast", "Beast (Magical)", "Construct", "Dissonant", "Dragon",
    "Elemental", "Empyrean", "Humanoid", "Humanoid (Fae)", "Humanoid (Giant)",
    "Infernal", "Monstrosity", "Phantom", "Undead", "Vegetal"
])
monster_role = st.selectbox("Monster Role", ["Brute", "Caster", "Skirmisher", "Leader"])
size = st.selectbox("Size", ["Diminutive", "Tiny", "Small", "Medium", "Large", "Huge", "Gigantic", "Colossal"])
apv = st.number_input("Action Points", 1, 7, 3)

# Auto-fill movement based on Size
movement_table = {
    "Diminutive": 15, "Tiny": 20, "Small": 25, "Medium": 30, "Large": 35,
    "Huge": 40, "Gigantic": 50, "Colossal": 60
}
default_move = movement_table.get(size, 30)
if 'Override Movement' not in st.session_state:
    st.session_state['Override Movement'] = False
override_movement = st.checkbox("Override Movement", value=st.session_state['Override Movement'])
move = st.number_input("Movement", 0, 100, default_move) if override_movement else default_move
initiative = st.number_input("Initiative", 0, 100, 6)

# --- Attributes ---
st.header("Attributes")
col_a1, col_a2, col_a3, col_a4 = st.columns(4)
with col_a1:
    str_score = st.number_input("STR", 1, 40, 10)
    int_score = st.number_input("INT", 1, 40, 10)
with col_a2:
    dex_score = st.number_input("DEX", 1, 40, 10)
    con_score = st.number_input("CON", 1, 40, 10)
with col_a3:
    pow_score = st.number_input("POW", 1, 40, 10)
    cha_score = st.number_input("CHA", 1, 40, 10)
with col_a4:
    tou_score = st.number_input("TOU", 1, 40, 10)

str_mod = get_mod(str_score, [-3, -2, -2, -1, -1, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6], 2)
int_mod = get_mod(int_score, [-3, -2, -2, -1, -1, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6], 2)
dex_mod = get_mod(dex_score, [-3, -2, -2, -1, -1, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6], 2)
con_mod = get_mod(con_score, [-5, -4, -3, -2, -1, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 1)
pow_mod = get_mod(pow_score, [-3, -2, -2, -1, -1, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6], 2)
cha_mod = get_mod(cha_score, [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6], 2)
resilience = get_mod(tou_score, list(range(6, 26)), 1)
grit = get_mod(tou_score, [-3, -2, -2, -1, -1, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6], 2)

# --- Vitals ---
st.subheader("Vitals")
col_a1, col_a2, col_a3, col_a4 = st.columns(4)
with col_a1:
    hpv = st.number_input("HP", 1, 999, 50)
with col_a2:
    fpv = st.number_input("FP", 1, 999, 40)
with col_a3:
    epv = st.number_input("EP", 1, 999, 25)
stun = int(hpv * 0.75)
stagger = resilience

# --- Weapons ---
st.subheader("Weapons")
weapons = []
wr_values = []
for i in range(1, 4):
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        wname = st.text_input(f"Weapon {i} Name", f"Weapon {i}")
    with col2:
        base_wr = st.number_input(f"WR {i}", 0, 40, 10)
    with col3:
        dtype = st.selectbox(f"Damage Type {i}", ["", "A", "B", "C", "E", "F", "N", "P", "Ps", "R", "S"], key=f"type_{i}")
    final_wr = base_wr + str_mod
    wr_values.append(base_wr)  # use base WR, not modified
    # Only add to the weapons list if the name is not blank
    if wname.strip():
        weapons.append(f"{wname}, WR {final_wr} ({dtype})")
 #   weapons.append(f"{wname}, WR {final_wr} ({dtype})")



# --- DV Breakdown ---
st.subheader("Armor (DV)")
dv_input = {}
dv_types = ["A", "B", "C", "E", "F", "N", "P", "Ps", "R", "S"]
dv_rows = [st.columns(5), st.columns(5)]
for i, k in enumerate(dv_types):
    with dv_rows[i // 5][i % 5]:
        base_val = st.number_input(f"{k}", 0, 35, 5, key=f"dv_{k}")
        dv_input[k] = base_val + grit
dv_line = " | ".join([f"{k} {dv_value}" for k, dv_value in dv_input.items()])

# Calculate average DV
average_dv = sum(dv_input.values()) / len(dv_input) - grit if dv_input else 0
st.text(f"Average DV: {average_dv:.2f}")

# Calculate median DV
#dv_values = [v - grit for v in dv_input.values()] if dv_input else []
#median_dv = statistics.median(dv_values) if dv_values else 0
#st.text(f"Median DV: {median_dv:.2f}")

# --- Skills ---
st.subheader("Skills (max 85)")
skill_list = [
    "Acrobatics", "Athletics", "Ballistics", "Cast Spells", "Countervail",
    "Dodge", "IW", "Parry", "Perception", "Rune Casting",
    "Stealth", "Throw", "Unarmed", "Vigor", "Weaponry"
]
skills = {}
skill_cols = st.columns(3)
for i, s in enumerate(skill_list):
    with skill_cols[i % 3]:
        skills[s] = st.number_input(s, 0, 85, 16)

# --- Specials ---
#st.subheader("Specials")
specials_table = {
    # Core Effects
    "Aura": {"mp": 2, "ap": 0, "cost": "—", "desc": "Aura that grants a modifier or applies a magical effect (e.g., fear (4), charm (6), polymorph (6), sleep (6), paralysis (8), petrification (10),death (12)). Adjust MP by severity; modifiers +/-2 per 2 MP; max MP 12."},
    "Breath Weapon": {"mp": 8, "ap": 2, "cost": "FP 14", "desc": "Exhales energy in a cone. Increase FP cost for larger affected areas."},
    "Burrow": {"mp": 3, "ap": 1, "cost": "FP 4", "desc": "Can tunnel through terrain."},
    "Corpse Explosion": {"mp": 10, "ap": 3, "cost": "EP 16", "desc": "Detonates a corpse for AoE damage."},
    "Disease": {"mp": 3, "ap": 2, "cost": "FP 10", "desc": "Inflicts a disease. Multiply MP by number of targets."},
    "Entangle": {"mp": 6, "ap": 2, "cost": "FP 8", "desc": "Restrains or slows enemies with webbing, tendrils, or other physical means."},
    "Essence Drain": {"mp": 4, "ap": 2, "cost": "EP 8", "desc": "Drains target's attributes, EP, FP, HP, or levels."},
    "Essence Stealing": {"mp": 8, "ap": 2, "cost": "EP 10", "desc": "Absorbs EP, FP, or HP from targets."},
    "Exploding Corpse": {"mp": 10, "ap": 0, "cost": "—", "desc": "The creatures corpse explodes in an AoE upon its death."},
    "Extra Damaging": {"mp": 4, "ap": 0, "cost": "—", "desc": "Deals +1D6 bonus damage. Set MP to 4 × number of dice; maximum 4D6."},
    "Fast Healing": {"mp": 4, "ap": 0, "cost": "—", "desc": "Regenerates 1D6 HP per round (up to 4D6). MP = 4 × number of dice."},
    "Fear Aura": {"mp": 4, "ap": 0, "cost": "—", "desc": "Passive aura causes fear; can be suppressed."},
    "Fly": {"mp": 4, "ap": 1, "cost": "FP 6", "desc": "Can fly or levitate."},
    "Gaze Attack": {"mp": 6, "ap": 2, "cost": "FP 8", "desc": "Line-of-sight effect (e.g., fear (4), charm (6), polymorph (6), sleep (6), paralysis (8), petrification (10),death (12)). Adjust MP by severity and multiply by targets affected."},
    "Grasping Shadows": {"mp": 6, "ap": 2, "cost": "FP 8", "desc": "Shadows grapple or slow creatures nearby."},
    "Haste": {"mp": 8, "ap": 2, "cost": "EP 14", "desc": "Grants target 1 AP for SR 3 rounds. Adjust EP for addtional duration and multiply MP by targets affected."},
    "Immunity": {"mp": 12, "ap": 0, "cost": "—", "desc": "Immune to one damage type completely. Set MP to 12 x number of immunities."},
    "Invisibility": {"mp": 6, "ap": 3, "cost": "FP 2", "desc": "Turns invisible."},
    "Magical Absorption": {"mp": 8, "ap": 2, "cost": "EP 14", "desc": "Absorbs magic, converting it to EP or FP."},
    "Melee AoE": {"mp": 8, "ap": 2, "cost": "FP 10", "desc": "Wide melee strike, scalable by WR or number of targets. Increase FP cost for larger affected areas."},
    "Mind Shatter": {"mp": 9, "ap": 2, "cost": "EP 12", "desc": "Causes psychic disruption: stun, fear, or disorientation."},
    "Phase": {"mp": 4, "ap": 1, "cost": "EP 8", "desc": "Walks through matter for SR 3 rounds."},
    "Plane Shift": {"mp": 8, "ap": 2, "cost": "EP 16", "desc": "Shifts to another plane of existence."},
    "Poison Effect": {"mp": 4, "ap": 1, "cost": "—", "desc": "Inflicts poison. Effect can be weakening (3), damage (4), paralysis (8), petrification (10), or death (12). Adjust MP by severity."},
    "Ray Attack": {"mp": 6, "ap": 2, "cost": "FP 8", "desc": "Magical beam causing fear (4), charm (6), polymorph (6), sleep (6), paralysis (8), petrification (10),death (12), etc. Adjust MP by severity and multiply by targets affected."},
    "Reduced Damage": {"mp": 2, "ap": 0, "cost": "FP 8", "desc": "Increases all DV by 2 for SR 3 rounds. Rule of thumb +1 DV per 1 MP; max MP 10."},
    "Regeneration": {"mp": 12, "ap": 3, "cost": "FP 24", "desc": "Regrows lost limbs or body over time."},
    "Resistances": {"mp": 6, "ap": 0, "cost": "—", "desc": "Takes half damage from one damage type. Set MP to 6 x number of resistances."},
    "Shape Shift": {"mp": 10, "ap": 3, "cost": "FP 20", "desc": "Transforms into a different form."},
    "Shatter Weapon": {"mp": 5, "ap": 2, "cost": "FP 10", "desc": "Destroys a mundane weapon on a successful parry."},
    "Slime Trail": {"mp": 3, "ap": 0, "cost": "—", "desc": "Leaves difficult or damaging terrain behind."},
    "Slow": {"mp": 8, "ap": 2, "cost": "EP 14", "desc": "Lowers targets AP by 1 for SR 3 rounds. Adjust EP for addtional duration and multiply MP by targets affected."},
    "Spell Reflection": {"mp": 8, "ap": 0, "cost": "EP 16", "desc": "Reflects a spell back at caster once per round."},
    "Swallow Whole": {"mp": 10, "ap": 2, "cost": "FP 10", "desc": "Swallows target on successful attack if targer failed defense check."},
    "Summon": {"mp": 6, "ap": 3, "cost": "EP 12", "desc": "Summon 1D3 + 1 creatures for SR 3 rounds. Increase MP for stronger summons."},
    "Teleport": {"mp": 6, "ap": 3, "cost": "EP 8", "desc": "Teleport to another visible or known location on same plane."},
    "Trample": {"mp": 4, "ap": 1, "cost": "FP 5", "desc": "Charge that knocks down enemies."},
    "Volatile Blood": {"mp": 6, "ap": 0, "cost": "—", "category": "Utility",
        "desc": "Damage from a melee attacks or bleeds cause the creature’s blood to react violently, splashing corrosive ichor, igniting sparks, or releasing noxious fumes. Attacker must succeed a Dodge check or take applicable damaged."}
}

st.subheader("Special Abilities")

specials = []
special_mp_total = 0

for i in range(1, 11):
    col1, col2 = st.columns([2, 1])
    with col1:
        choice = st.selectbox(
            f"Special {i} Type",
            ["None"] + list(specials_table.keys()) + ["Custom"],
            key=f"special_type_{i}"
        )
    with col2:
        if choice == "Custom":
            custom_name = st.text_input(f"Custom Name {i}", "", key=f"custom_name_{i}")
            desc = st.text_input(f"Custom Desc {i}", "", key=f"custom_desc_{i}")
            ap = st.number_input(f"Custom AP {i}", 0, 10, 0, key=f"custom_ap_{i}")
            action_type = st.selectbox(f"Action Type {i}", ["Interrupt","On-Turn", "Passive"], key=f"acttype_{i}")
            ep = st.number_input(f"Custom EP {i}", 0, 100, 0, key=f"custom_ep_{i}")
            fp = st.number_input(f"Custom FP {i}", 0, 100, 0, key=f"custom_fp_{i}")
            mp = st.number_input(f"Custom MP {i}", 0, 50, 0, key=f"custom_mp_{i}")
            wrs = st.number_input(f"Custom WR {i}", 0, 40, 0, key=f"custom_wrs_{i}")
            wr_type = st.selectbox(f"Damage Type {i}", ["","A", "B", "C", "E", "F", "N", "P", "Ps", "R", "S"], key=f"wtype_{i}")
            if desc:
                display_name = custom_name if custom_name else "Custom Ability"
                cost_string = []
                if ap: cost_string.append(f"AP {ap}")
                if action_type: cost_string.append(f"{action_type}")
                if ep: cost_string.append(f"EP {ep}")
                if fp: cost_string.append(f"FP {fp}")
                if wrs: cost_string.append(f"WR {wrs} ({wr_type})")
                cost_str = ", ".join(cost_string) if cost_string else "—"
                specials.append(f"- {display_name} [{cost_str}]: {desc}")
                special_mp_total += mp
        elif choice != "None":
            info = specials_table[choice]

            default_ap = info.get("ap", 0)
            default_ep = int(info.get("cost").split("EP ")[1]) if "EP " in info.get("cost", "") else 0
            default_fp = int(info.get("cost").split("FP ")[1]) if "FP " in info.get("cost", "") else 0
            default_desc = info.get("desc", "")
            default_mp = info.get("mp", 0)

            custom_name = st.text_input(f"Name override for {choice}", choice, key=f"custom_named_{i}")
            custom_desc = st.text_area(f"Description override for {choice}", default_desc, key=f"custom_desc_{i}")
            ap = st.number_input(f"Override AP {i}", 0, 10, default_ap, key=f"custom_ap_{i}")
            action_type = st.selectbox(f"Action Type {i}", ["Interrupt", "On-Turn", "Passive"], index=1, key=f"acttype_{i}")
            ep = st.number_input(f"Override EP {i}", 0, 100, default_ep, key=f"custom_ep_{i}")
            fp = st.number_input(f"Override FP {i}", 0, 100, default_fp, key=f"custom_fp_{i}")
            mp = st.number_input(f"Override MP {i}", 0, 100, default_mp, key=f"custom_mp_{i}")
            wrs = st.number_input(f"Override WR {i}", 0, 40, 0, key=f"custom_wrs_{i}")
            wr_type = st.selectbox(f"Damage Type {i}", ["", "A", "B", "C", "E", "F", "N", "P", "Ps", "R", "S"], key=f"wtype_{i}")

            display_name = custom_name if custom_name else choice
            cost_string = []
            if ap: cost_string.append(f"AP {ap}")
            if action_type: cost_string.append(f"{action_type}")
            if ep: cost_string.append(f"EP {ep}")
            if fp: cost_string.append(f"FP {fp}")
            if wrs: cost_string.append(f"WR {wrs} ({wr_type})")
            cost_str = ", ".join(cost_string) if cost_string else "—"

            specials.append(f"- {display_name} [{cost_str}]: {custom_desc}")
            special_mp_total += mp

# --- Flavor and Treasure ---
st.header("Flavor & Treasure")
carried_treasure = st.text_input("Carried Treasure", "3D6 x 10 gold, or 1D4 bone charms.")
lair_treasure = st.text_input("Lair Treasure", "Common treasure table.")
description = st.text_area("Description", "Towering desert brute caked in crimson dust and dried blood...")

# MP Budget from level
mp_budget = level + 50

# --- MP Breakdown ---
with st.expander("MP Cost Breakdown"):
    # Size MP Cost
    size_mp_table = {
        "Diminutive": 0, "Tiny": 1, "Small": 2, "Medium": 4, "Large": 6,
        "Huge": 8, "Gigantic": 10, "Colossal": 12
    }
    mp_size = size_mp_table.get(size, 0)
    st.text(f"Size Cost: {mp_size}")
  
  # Attribute MP (based on actual base scores)
    attribute_mp_table = {
        1: -1.25, 2: -1, 3: -0.75, 4: -0.5, 5: -0.25, 6: 0, 7: 0, 8: 0, 9: 0.2, 10: 0.2,
        11: 0.3, 12: 0.3, 13: 0.4, 14: 0.4, 15: 0.6, 16: 0.6, 17: 0.8, 18: 0.8, 19: 1, 20: 1,
        21: 4, 22: 4, 23: 7, 24: 7, 25: 10, 26: 10, 27: 13, 28: 13, 29: 16, 30: 16,
        31: 19, 32: 19, 33: 22, 34: 22, 35: 25, 36: 25, 37: 28, 38: 28, 39: 31, 40: 31
    }
    attribute_scores = [str_score, int_score, dex_score, con_score, cha_score, pow_score, tou_score]
    mp_attributes = sum(attribute_mp_table.get(score, 0) for score in attribute_scores)
    st.text(f"Attribute Cost: {mp_attributes}")

    # Vitals MP Cost
    mp_hp = hpv / 5
    st.text(f"HP Cost: {mp_hp}")
  
    mp_fp = fpv / 10
    st.text(f"FP Cost: {mp_fp}")  
  
    mp_ep = epv / 10
    st.text(f"EP Cost: {mp_ep}")  
  
    # AP MP Cost
    mp_ap_table = {1: -3, 2: 0, 3: 3, 4: 6, 5: 9, 6: 12, 7: 15}
    mp_ap = mp_ap_table.get(apv, 0)
    st.text(f"AP Cost: {mp_ap}")
  
    # Weapon WR MP
    mp_weapons = max(0, max(wr_values, default=0) - 4)
    st.text(f"Weapon Cost: {mp_weapons}")

    # DV MP Cost
    mp_dv = average_dv * 2.8
#    mp_dv = median_dv * 2.5
    
    st.text(f"DV Cost: {mp_dv}")
  
    # Skills MP Cost
    mp_skills = 0
    for val in skills.values():
        if val >= 80:
            mp_skills += 2.5
        elif val >= 70:
            mp_skills += 2
        elif val >= 60:
            mp_skills += 1.5
        elif val >= 50:
            mp_skills += 1
        elif val >= 30:
            mp_skills += 0.5
    st.text(f"Skill Cost: {mp_skills}")

    # Specials MP Cost
    st.text(f"Specials Cost: {special_mp_total}")

# Total MP used
total_mp_used = round(mp_size + mp_attributes + mp_hp + mp_fp + mp_ep + mp_ap + mp_weapons + mp_dv + mp_skills + special_mp_total, 2)
if total_mp_used > mp_budget:
    color = "red"
elif total_mp_used < mp_budget - 5:
    color = "orange"
else:
    color = "green"

st.markdown(
    f"### <span style='color:{color}'>**Total MP Used: {total_mp_used} / {mp_budget}**</span>",
    unsafe_allow_html=True
)

if total_mp_used > mp_budget:
    st.error(f"Over MP Budget by {total_mp_used - mp_budget:.2f}! Monster may be overpowered")
elif total_mp_used < mp_budget - 5:
    st.warning(f"MP Budget underused by {mp_budget - total_mp_used:.2f}. Monster may be underpowered.")
else:
    st.success("MP Budget is balanced.")

# --- XP Lookup Table ---
xp_table = {
    1: 17, 2: 24, 3: 33, 4: 42, 5: 51, 6: 60, 7: 69, 8: 78, 9: 89, 10: 100,
    11: 113, 12: 128, 13: 145, 14: 164, 15: 185, 16: 210, 17: 239, 18: 272, 19: 311, 20: 358,
    21: 413, 22: 478, 23: 555, 24: 646, 25: 755, 26: 884, 27: 1037, 28: 1220, 29: 1439, 30: 1700,
    31: 2013, 32: 2388, 33: 2837, 34: 3374, 35: 4017, 36: 4788, 37: 5713, 38: 6822, 39: 8151, 40: 9746,
    41: 11351, 42: 12956, 43: 14561, 44: 16166, 45: 17771, 46: 19376, 47: 20981, 48: 22586, 49: 24191, 50: 25796,
    51: 27401, 52: 29006, 53: 30611, 54: 32216, 55: 33821, 56: 35426, 57: 37031, 58: 38636, 59: 40241, 60: 41846,
    61: 43451, 62: 45056, 63: 46661, 64: 48266, 65: 49871, 66: 51476, 67: 53081, 68: 54686, 69: 56291, 70: 57896,
    71: 59501, 72: 61106, 73: 62711, 74: 64316, 75: 65921, 76: 67526, 77: 69131, 78: 70736, 79: 72341, 80: 73946,
    81: 75551, 82: 77156, 83: 78761, 84: 80366, 85: 81971, 86: 83576, 87: 85181, 88: 86786, 89: 88391, 90: 89996,
    91: 91601, 92: 93206, 93: 94811, 94: 96416, 95: 98021, 96: 99626, 97: 101231, 98: 102836, 99: 104441, 100: 106046
}
monster_xp = xp_table.get(level, 0)

# --- Statblock Preview ---
st.header("Stat Block Preview")
statblock = f"""{name.upper()} (L{level} {creature_type.upper()})
STR {str_score} ({str_mod}) | INT {int_score} ({int_mod}) | DEX {dex_score} ({dex_mod}) | CON {con_score} ({con_mod}) | POW {pow_score} ({pow_mod}) | CHA {cha_score} ({cha_mod}) | TOU {tou_score} ({resilience} / {grit})
AP {apv} | Move {move} | Initiative {initiative} | Size {size}
HP {hpv} | FP {fpv} | EP {epv} | Stun {stun} | Stagger {stagger}
DV: {dv_line}
Attack: {" | ".join(weapons)}
Skills: {" | ".join(f"{k} {v}" for k, v in skills.items())}
Specials:
{chr(10).join(specials)}
Carried Treasure: {carried_treasure}
Lair Treasure: {lair_treasure}
Description: {description}
XP: {monster_xp:,}
"""
st.text_area("Formatted Stat Block", statblock, height=400)
