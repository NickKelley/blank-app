import streamlit as st
import pandas as pd

st.set_page_config(page_title="Paint Estimator", page_icon="🎨", layout="centered")

st.title("🎨 Paint Estimator")
st.write("Add rooms, enter measurements, and export totals to CSV.")

# Initialize session storage
if "rooms" not in st.session_state:
    st.session_state.rooms = []

# ---- Add Room Form ----
st.header("Add a Room")

with st.form("add_room", clear_on_submit=True):
    name = st.text_input("Room name", placeholder="e.g., Living Room")
    length = st.number_input("Length (ft)", min_value=0.0, step=0.1)
    width = st.number_input("Width (ft)", min_value=0.0, step=0.1)
    height = st.number_input("Wall height (ft)", min_value=0.0, step=0.1)
    doors = st.number_input("Number of doors", min_value=0, step=1)
    windows = st.number_input("Number of windows", min_value=0, step=1)
    coats = st.number_input("Coats", min_value=1, value=2, step=1)

    submitted = st.form_submit_button("➕ Add Room")

if submitted and name.strip():
    # wall area = perimeter * height
    wall_area = 2 * (length + width) * height
    # ceiling area = length * width
    ceiling_area = length * width
    # openings
    opening_area = doors * 21 + windows * 15  # standard approx
    paintable = max(wall_area - opening_area, 0) + ceiling_area

    st.session_state.rooms.append({
        "Room": name.strip(),
        "Length (ft)": length,
        "Width (ft)": width,
        "Height (ft)": height,
        "Doors": doors,
        "Windows": windows,
        "Wall Area (sqft)": round(wall_area, 2),
        "Ceiling Area (sqft)": round(ceiling_area, 2),
        "Openings (sqft)": round(opening_area, 2),
        "Paintable Area (sqft)": round(paintable, 2),
        "Coats": coats,
        "Total Area × Coats (sqft)": round(paintable * coats, 2),
    })
    st.success(f"Added room: {name.strip()}")

# ---- Room Table ----
st.header("Rooms Added")

if st.session_state.rooms:
    df = pd.DataFrame(st.session_state.rooms)
    st.dataframe(df, use_container_width=True)

    total_area = df["Total Area × Coats (sqft)"].sum()
    st.metric("Total Paintable Area × Coats", f"{total_area:.0f} sq ft")

    # CSV export
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download CSV", data=csv, file_name="paint_estimate.csv", mime="text/csv")
else:
    st.info("No rooms yet. Add one above to begin.")

def delete_room(rooms):
    if not rooms:
        print("No rooms to delete.\n")
        return rooms

    print("\nCurrent rooms:")
    for i, r in enumerate(rooms, 1):
        print(f"{i}. {r.name} | {r.area_all_coats:.1f} sq ft (with coats)")
    print("")

    try:
        idx = int(input("Enter the number of the room to delete: "))
        if 1 <= idx <= len(rooms):
            removed = rooms.pop(idx - 1)
            print(f"✓ Removed room: {removed.name}\n")
        else:
            print("Invalid number.\n")
    except ValueError:
        print("Please enter a valid integer.\n")

    return rooms

def main():
    rooms = []
    while True:
        print("=== Paint Estimator ===")
        print("[A]dd room   [L]ist rooms   [E]xport CSV   [D]elete room   [Q]uit")
        choice = input("Choose: ").strip().lower()

        if choice == "a":
            r = add_room()
            if r:
                rooms.append(r)
        elif choice == "l":
            list_rooms(rooms)
        elif choice == "e":
            export_csv(rooms)
        elif choice == "d":
            rooms = delete_room(rooms)
        elif choice == "q":
            print("Goodbye!")
            break
        else:
            print("Invalid option.\n")
