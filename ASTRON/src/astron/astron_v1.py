
import math
import matplotlib.pyplot as plot
from google import genai
from google.genai import types

# ==========================================
# 1. ASTRODYNAMICS & PHYSICS ENGINE MODULE
# ==========================================

# Standard Physical Constants
G_EARTH = 9.80665               # Standard gravity at sea level (m/s^2)
MU_EARTH = 3.986004418e14       # Earth gravitational parameter (m^3 / s^2)
R_EARTH = 6371000.0             # Mean Earth radius in meters

def calculate_delta_v(isp: float, m_initial: float, m_final: float) -> float:
    """

    Tsiolkovsky Rocket Equation:
    Delta-v = Isp * g0 * ln(m0 / mf)
    """

    if m_final <= 0 or m_initial <= m_final:
        raise ValueError("Initial mass must be strictly greater than final dry mass.")
    return isp * G_EARTH * math.log(m_initial / m_final)


def circular_orbital_speed(altitude_km: float) -> float:
    """

    Calculates circular orbital velocity at a given altitude above Earth:
    v_c = sqrt(mu / r)
    """

    r = R_EARTH + (altitude_km * 1000.0)
    return math.sqrt(MU_EARTH / r)


def vis_viva_velocity(r_m: float, semi_major_axis_m: float) -> float:
    """
    Vis-Viva Equation for orbital velocity along an elliptical or circular path:
    v = sqrt(mu * (2/r - 1/a) )
    """
    return math.sqrt(MU_EARTH * ((2.0 / r_m) - (1.0 / semi_major_axis_m)))


def propagate_2D_orbit(altitude_km: float = 400.0, num_steps: int = 1000, dt: float = 5.0):
    """
    Propagates a 2D orbit numerically using Newton's law of universal gravitation.
    """
    r_initial = R_EARTH + (altitude_km * 1000.0)
    v_initial = circular_orbital_speed(altitude_km)

    # Initial state vector: [x, y, vx, vy]
    x, y = 0.0, r_initial
    vx, vy = v_initial, 0.0

    x_coords, y_coords = [x / 1000.0], [y / 1000.0]

    for _ in range(num_steps):
        r_current = math.sqrt(x**2 + y**2)

        # Gravitational acceleration components: a = -mu / r^2 * (pos / r)
        ax = -MU_EARTH * x / (r_current**3)
        ay = -MU_EARTH * y / (r_current**3)

        # Velocity Verlet / Euler-cromer integration
        vx += ax * dt
        vy += ay * dt
        x += vx * dt
        y += vy * dt

        x_coords.append(x / 1000.0)
        y_coords.append(y / 1000.0)

    # Plot the propagated trajectory
    plot.figure(figsize=(6, 6))
    plot.plot(x_coords, y_coords, label=f"Orbit Path ({altitude_km} km)", color="crimson")

    # Draw Earth body
    earth_circle = plot.Circle((0, 0), R_EARTH / 1000.0, color="navy", alpha=0.3, label="Earth Radius")
    plot.gca().add_patch(earth_circle)

    plot.title("2D Orbit Propagation")
    plot.xlabel("X (km)")
    plot.ylabel("Y (km)")
    plot.grid(True)
    plot.axis("equal")
    plot.legend()
    plot.show()


  # =========================================
  # 2. RUNTIME AND AI ASSISTANT
  # =========================================

  # Print startup physics calculations directly to console
    print("==========================================")
    print("          ASTRON ENGINE INITIALIZED       ")
    print("==========================================")

    # Define the variables
    effective_exhaust_velocity = 3000.0           # in m/s
    initial_total_mass = 100000.0          # m0 in kg
    final_dry_mass = 15000.0           # mf in kg

    # Calculate Delta-v using the Tsiolkovolsky rocket equation
    sample_dv = effective_exhaust_velocity * math.log(initial_total_mass / final_dry_mass)
    print(f"Sample Rocket Delta-v: {sample_dv / 1000:.2f} km/s")

    vis_viva_sample = vis_viva_velocity(r_m=6771000, semi_major_axis_m=6771000)
    print(f"Vis-Viva Speed @ 400km circular: {vis_viva_sample / 1000:.3f} km/s")
    print("===========================================\n")

  # Connect Gemini Client
API_KEY = "AQ.Ab8RN6Lk9fEuRnNfCZM3gVaIWjML5RtRFBDxawh-VW_Xwooryw"
client = genai.Client(api_key="AQ.Ab8RN6Lk9fEuRnNfCZM3gVaIWjML5RtRFBDxawh-VW_Xwooryw")

  # Start Interactive Chat Loop
while True:
    user_input = input("Ask ASTRON (or type 'plot' / 'quit'): ").strip()
    
    if user_input.lower() in ["quit", "exit"]:
        print("Exiting ASTRON.")
        break

    if "plot" in user_input.lower() or "propagate" in user_input.lower():
        print("Generating orbit plot...")
        propagate_2D_orbit(altitude_km=400.0)
        continue

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction="You are ASTRON, an expert orbital mechanics AI assistant.",
                temperature=0.3,
            )
        )
        print(f"\nASTRON: {response.text}\n")
    except Exception as e:
        print(f"\nError contacting Gemini API: {e}\n")

  

