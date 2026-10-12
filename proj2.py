#ตาข่าย 
import numpy as np
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# Page Configuration
# ==============================================================================
st.set_page_config(
    page_title="Parabola in Volleyball Spike",
    page_icon="🏐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# 1. พารามิเตอร์คงที่ทางฟิสิกส์
# ==============================================================================
m = 0.27  # มวลลูกวอลเลย์บอล m (kg)
r = 0.105  # รัศมีลูกวอลเลย์บอล r (m)
A = np.pi * (r**2)  # พื้นที่หน้าตัด A (m^2)
rho = 1.20  # ความหนาแน่นอากาศ rho (kg/m^3)
mu = 1.81e-5  # ความหนืดพลวัตของอากาศ (Pa·s)
g = 9.81  # ความเร่งเนื่องจากแรงโน้มถ่วง g (m/s^2)
CD = 0.50  # ค่าสัมประสิทธิ์แรงต้านอากาศ CD
NET_HEIGHT = 2.43  # ความสูงตาข่าย (m)
NET_HALF_WIDTH = 4.5  # ครึ่งความกว้างตาข่าย (m)

# ==============================================================================
# Sidebar - Presets & Interactive Sliders
# ==============================================================================
st.sidebar.header("🏐 พารามิเตอร์การตีลูก (Spike Controls)")

preset = st.sidebar.selectbox(
    "เลือกค่าตั้งต้น (Presets):",
    [
        "กำหนดเอง (Custom)",
        "Standard Spike (ตบข้ามลงในแดน)",
        "Hit Net (ตบติดตาข่าย - ทดสอบระบบชนเน็ต)",
        "High Arc (ตบมุมโด่ง)",
        "Spike Out (ตบแรงออกหลัง)",
        "Sharp Cross-Court (ตบมุมเฉียงทแยง)",
    ],
)

# กำหนดค่า default ตาม preset
def_h = 3.00
def_x = -1.00
def_y = 0.00
def_alpha = 10.0
def_v0 = 20.0
def_omega = 4.0
def_beta = 0.0

if preset == "Standard Spike (ตบข้ามลงในแดน)":
    def_h, def_x, def_y, def_alpha, def_v0, def_omega, def_beta = 3.00, -1.00, 0.00, 10.0, 20.0, 4.0, 0.0
elif preset == "Hit Net (ตบติดตาข่าย - ทดสอบระบบชนเน็ต)":
    def_h, def_x, def_y, def_alpha, def_v0, def_omega, def_beta = 2.60, -2.00, 0.00, 15.0, 18.0, 4.0, 0.0
elif preset == "High Arc (ตบมุมโด่ง)":
    def_h, def_x, def_y, def_alpha, def_v0, def_omega, def_beta = 2.80, -1.50, 0.00, -5.0, 15.0, 2.0, 0.0
elif preset == "Spike Out (ตบแรงออกหลัง)":
    def_h, def_x, def_y, def_alpha, def_v0, def_omega, def_beta = 3.20, -0.80, 0.00, 2.0, 32.0, 1.0, 0.0
elif preset == "Sharp Cross-Court (ตบมุมเฉียงทแยง)":
    def_h, def_x, def_y, def_alpha, def_v0, def_omega, def_beta = 3.00, -1.00, -2.00, 12.0, 22.0, 5.0, 15.0

h = st.sidebar.slider(
    "Height Z จุดตบ (m):",
    min_value=2.00,
    max_value=4.50,
    value=def_h,
    step=0.05,
    help="ความสูงของจุดสัมผัสบอลในแนวดิ่ง",
)

X_start = st.sidebar.slider(
    "Position X จุดตบ (m):",
    min_value=-8.00,
    max_value=0.00,
    value=def_x,
    step=0.10,
    help="ตำแหน่งแนวลึกจากเน็ต (เน็ตอยู่ที่ X = 0)",
)

Y_start = st.sidebar.slider(
    "Position Y จุดตบ (m):",
    min_value=-4.00,
    max_value=4.00,
    value=def_y,
    step=0.10,
    help="ตำแหน่งแนวขวางขนานกับเน็ต",
)

alpha_deg = st.sidebar.slider(
    "Spike Angle α มุมตบแนวดิ่ง (°):",
    min_value=-10.0,
    max_value=45.0,
    value=def_alpha,
    step=0.5,
    help="มุมก้มลงต่ำหาพื้น (ค่าบวกคือก้มลงต่ำ)",
)

V0 = st.sidebar.slider(
    "Speed V0 ความเร็วต้น (m/s):",
    min_value=10.0,
    max_value=35.0,
    value=def_v0,
    step=0.5,
    help="ความเร็วต้นของลูกวอลเลย์บอล",
)

omega = st.sidebar.slider(
    "Topspin ω การหมุน (rev/s):",
    min_value=0.0,
    max_value=15.0,
    value=def_omega,
    step=0.5,
    help="อัตราการหมุนรอบตัวเองของลูกบอล",
)

beta_deg = st.sidebar.slider(
    "Azimuth Angle β มุมเฉียงแนวระนาบ (°):",
    min_value=-30.0,
    max_value=30.0,
    value=def_beta,
    step=1.0,
    help="มุมเฉียงซ้าย-ขวาของการตบลูก",
)

st.sidebar.markdown("---")
cam_option = st.sidebar.selectbox(
    "มุมมองกล้อง 3D (Camera View):",
    [
        "Isometric View (มุมมอง 3 มิติทั่วไป)",
        "Side View (มุมมองข้างสนาม - ดูเน็ตชัดเจน)",
        "Behind Spiker (มุมมองจากด้านหลังผู้ตบ)",
        "Top-down View (มุมมองด้านบน Bird's Eye)",
    ],
)

cam_dict = {
    "Isometric View (มุมมอง 3 มิติทั่วไป)": dict(x=-1.5, y=-1.8, z=0.8),
    "Side View (มุมมองข้างสนาม - ดูเน็ตชัดเจน)": dict(x=0.0, y=-2.5, z=0.4),
    "Behind Spiker (มุมมองจากด้านหลังผู้ตบ)": dict(x=-2.4, y=0.0, z=0.6),
    "Top-down View (มุมมองด้านบน Bird's Eye)": dict(x=0.0, y=0.0, z=2.5),
}

# ==============================================================================
# 2. ฟังก์ชันคำนวณและแสดงผล 3D
# ==============================================================================
def run_volleyball_simulation(h=3.00, X_start=-1.00, Y_start=0.00, alpha_deg=10.0, V0=20.0, omega=4.0, beta_deg=0.0):
    alpha = np.radians(alpha_deg)
    beta = np.radians(beta_deg)

    # ความเร็วต้นแยกตามแกน X และ Y
    vx0 = V0 * np.cos(alpha)
    vy0 = -V0 * np.sin(alpha)

    # 1. คำนวณระยะเวลาบินรวมจนกระทั่งตกถึงพื้น (z = 0) แบบปกติ
    t_flight_ground = (vy0 + np.sqrt(vy0**2 + 2 * g * h)) / g

    # 2. ตรวจสอบการติดตาข่าย (Net Collision Check at X = 0)
    hit_net = False
    t_flight = t_flight_ground
    z_net = None

    if vx0 > 0 and X_start < 0:
        t_net = -X_start / vx0
        if 0 < t_net <= t_flight_ground:
            # คำนวณตำแหน่ง Y และ Z ณ เวลาที่ผ่านแนวตาข่าย X = 0
            y_net = Y_start + (-X_start) * np.sin(beta)
            z_net = h + vy0 * t_net - 0.5 * g * (t_net**2)

            # ถ้าความสูง Z ต่ำกว่าหรือเท่ากับตาข่าย และอยู่ในขอบเขตความกว้างตาข่าย
            if -NET_HALF_WIDTH <= y_net <= NET_HALF_WIDTH and z_net <= NET_HEIGHT:
                hit_net = True
                t_flight = t_net  # ตัดเวลาการบินให้หยุดที่ตาข่ายทันที

    # 3. คำนวณตำแหน่ง (x, y) ตามเวลา t_flight
    t_arr = np.linspace(0, t_flight, 100)
    x_2d = X_start + vx0 * t_arr
    y_2d = h + vy0 * t_arr - 0.5 * g * (t_arr**2)

    # แปลงพิกัดเป็น 3D
    X_3D = x_2d * np.cos(beta)
    Y_3D = Y_start + (x_2d - X_start) * np.sin(beta)
    Z_3D = y_2d

    num_frames = 40
    frame_idx = np.linspace(0, len(X_3D) - 1, num_frames, dtype=int)
    X_anim = X_3D[frame_idx]
    Y_anim = Y_3D[frame_idx]
    Z_anim = Z_3D[frame_idx]

    x_land, y_land, z_land = X_3D[-1], Y_3D[-1], Z_3D[-1]

    # ตรวจสอบการลงในเขตสนาม / ชนตาข่าย
    if hit_net:
        result_text = "NET!"
        result_color = "#dc3545"
        result_desc = "ลูกชนตาข่าย (ติดเน็ต)"
    else:
        in_opponent_x = 0.0 <= x_land <= (9.0 + r)
        in_own_x = -(9.0 + r) <= x_land < 0.0
        in_y = (-4.5 - r) <= y_land <= (4.5 + r)

        if in_opponent_x and in_y:
            result_text = "IN!"
            result_color = "#28a745"
            result_desc = "ลูกลงในแดนคู่แข่งถูกต้อง"
        elif in_own_x and in_y:
            result_text = "FAULT!"
            result_color = "#fd7e14"
            result_desc = "ลูกตกในแดนตัวเอง (Fault)"
        else:
            result_text = "OUT!"
            result_color = "#dc3545"
            result_desc = "ลูกตกออกนอกสนาม"

    fig = go.Figure()

    # พื้นสนาม (Court Surface)
    fig.add_trace(
        go.Mesh3d(
            x=[-9, 9, 9, -9],
            y=[-4.5, -4.5, 4.5, 4.5],
            z=[0, 0, 0, 0],
            color="orange",
            opacity=0.55,
            name="Court Surface",
        )
    )

    # เส้นสนาม (Court Boundary Lines)
    lines = [
        ([-9, 9, 9, -9, -9], [-4.5, -4.5, 4.5, 4.5, -4.5], [0, 0, 0, 0, 0]),
        ([0, 0], [-4.5, 4.5], [0, 0]),
        ([-3, -3], [-4.5, 4.5], [0, 0]),
        ([3, 3], [-4.5, 4.5], [0, 0]),
    ]
    for lx, ly, lz in lines:
        fig.add_trace(
            go.Scatter3d(
                x=lx,
                y=ly,
                z=lz,
                mode="lines",
                line=dict(color="white", width=6),
                showlegend=False,
            )
        )

    # ตาข่าย (Net Surface & Top Band)
    fig.add_trace(
        go.Mesh3d(
            x=[0, 0, 0, 0],
            y=[-4.5, 4.5, 4.5, -4.5],
            z=[0, 0, NET_HEIGHT, NET_HEIGHT],
            color="gray",
            opacity=0.35,
            name=f"Net ({NET_HEIGHT}m)",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=[0, 0],
            y=[-4.5, 4.5],
            z=[NET_HEIGHT, NET_HEIGHT],
            mode="lines",
            line=dict(color="white", width=8),
            showlegend=False,
        )
    )

    # จุดตบเริ่มต้น (Spike Starting Point)
    fig.add_trace(
        go.Scatter3d(
            x=[X_3D[0]],
            y=[Y_3D[0]],
            z=[Z_3D[0]],
            mode="markers",
            marker=dict(size=8, color="royalblue"),
            name=f"Spike Point ({h:.2f}m)",
        )
    )

    # รอยเงากระทบพื้น / จุดชนตาข่าย
    theta = np.linspace(0, 2 * np.pi, 30)
    if hit_net:
        # วงกลมบนระนาบตาข่าย (X = 0)
        circle_x = np.zeros_like(theta)
        circle_y = y_land + r * np.cos(theta)
        circle_z = z_land + r * np.sin(theta)
        circle_z = np.clip(circle_z, 0, NET_HEIGHT)
    else:
        # วงกลมบนพื้นสนาม (Z = 0)
        circle_x = x_land + r * np.cos(theta)
        circle_y = y_land + r * np.sin(theta)
        circle_z = np.zeros_like(circle_x)

    fig.add_trace(
        go.Scatter3d(
            x=circle_x,
            y=circle_y,
            z=circle_z,
            mode="lines",
            surfaceaxis=2 if not hit_net else 0,
            surfacecolor=result_color,
            line=dict(color=result_color, width=3),
            name=f"Impact Spot ({result_text})",
        )
    )

    # วิถีและตำแหน่งลูกบอล (Trajectory Trail & Ball Marker)
    fig.add_trace(
        go.Scatter3d(
            x=[X_anim[0]],
            y=[Y_anim[0]],
            z=[Z_anim[0]],
            mode="lines",
            line=dict(color="gold", width=7),
            name="Trajectory Trail",
        )
    )
    fig.add_trace(
        go.Scatter3d(
            x=[X_anim[0]],
            y=[Y_anim[0]],
            z=[Z_anim[0]],
            mode="markers",
            marker=dict(
                size=11,
                color="yellow",
                symbol="circle",
                line=dict(color="black", width=1),
            ),
            name="Ball Position",
        )
    )

    # สร้าง Animation Frames
    frames = []
    for k in range(num_frames):
        frame_data = [
            go.Scatter3d(
                x=X_anim[: k + 1],
                y=Y_anim[: k + 1],
                z=Z_anim[: k + 1],
                mode="lines",
            ),
            go.Scatter3d(
                x=[X_anim[k]],
                y=[Y_anim[k]],
                z=[Z_anim[k]],
                mode="markers",
                marker=dict(
                    size=11,
                    color="yellow",
                    symbol="circle",
                    line=dict(color="black", width=1),
                ),
            ),
        ]
        frames.append(go.Frame(data=frame_data, traces=[9, 10], name=f"frame{k}"))

    fig.frames = frames

    anim_slider = [
        {
            "steps": [
                {
                    "method": "animate",
                    "label": f"{i+1}",
                    "args": [
                        [f"frame{i}"],
                        {
                            "mode": "immediate",
                            "frame": {"duration": 0, "redraw": True},
                            "transition": {"duration": 0},
                        },
                    ],
                }
                for i in range(num_frames)
            ],
            "transition": {"duration": 0},
            "x": 0.1,
            "y": -0.05,
            "currentvalue": {
                "font": {"size": 13},
                "prefix": "Frame Progress: ",
                "visible": True,
                "xanchor": "center",
            },
            "len": 0.85,
        }
    ]

    updatemenus = [
        {
            "type": "buttons",
            "showactive": False,
            "x": 0.0,
            "y": -0.05,
            "buttons": [
                {
                    "label": "▶ Play",
                    "method": "animate",
                    "args": [
                        None,
                        {
                            "frame": {"duration": 40, "redraw": True},
                            "fromcurrent": True,
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        },
                    ],
                },
                {
                    "label": "⏸ Pause",
                    "method": "animate",
                    "args": [
                        [None],
                        {
                            "frame": {"duration": 0, "redraw": False},
                            "mode": "immediate",
                            "transition": {"duration": 0},
                        },
                    ],
                },
            ],
        }
    ]

    fig.update_layout(
        title=dict(
            text=(
                f"<b>Parabola in Volleyball Spike</b><br>"
                f"ผลการตัดสิน: <span style='color:{result_color}; font-weight:bold;'>{result_text}</span> ({result_desc}) | "
                f"จุดตก/ชน: (X={x_land:.2f}m, Y={y_land:.2f}m, Z={z_land:.2f}m) | "
                f"เวลาบิน: {t_flight:.3f}s"
            ),
            x=0.5,
            xanchor="center",
        ),
        scene=dict(
            xaxis=dict(title="Court Length X (m)", range=[-10, 10]),
            yaxis=dict(title="Court Width Y (m)", range=[-6, 6]),
            zaxis=dict(title="Height Z (m)", range=[0, 5]),
            aspectmode="manual",
            aspectratio=dict(x=2, y=1, z=0.6),
            camera=dict(eye=cam_dict.get(cam_option, dict(x=-1.5, y=-1.8, z=0.8))),
        ),
        sliders=anim_slider,
        updatemenus=updatemenus,
        margin=dict(l=0, r=0, b=50, t=80),
        height=650,
    )

    return fig, {
        "hit_net": hit_net,
        "result_text": result_text,
        "result_color": result_color,
        "result_desc": result_desc,
        "x_land": x_land,
        "y_land": y_land,
        "z_land": z_land,
        "t_flight": t_flight,
        "z_net": z_net,
    }

# ==============================================================================
# UI Main Section
# ==============================================================================
st.title("🏐 Parabola in Volleyball Spike")

# คำนวณแบบจำลอง
fig, res = run_volleyball_simulation(
    h=h,
    X_start=X_start,
    Y_start=Y_start,
    alpha_deg=alpha_deg,
    V0=V0,
    omega=omega,
    beta_deg=beta_deg,
)

# แสดงแถบ Metrics สรุปผล
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "คำตัดสิน (Decision)",
    res["result_text"],
    delta=res["result_desc"],
    delta_color="normal" if res["result_text"] == "IN!" else ("off" if res["result_text"] == "FAULT!" else "inverse"),
)
c2.metric(
    "จุดกระทบ (Impact Point)",
    f"X: {res['x_land']:.2f} m",
    f"Y: {res['y_land']:.2f} m, Z: {res['z_land']:.2f} m",
)
c3.metric(
    "เวลาลอยตัว (Flight Time)",
    f"{res['t_flight']:.3f} s",
)
if res["z_net"] is not None:
    diff_net = res["z_net"] - NET_HEIGHT
    c4.metric(
        "ระดับความสูงผ่านแนวเน็ต (At Net X=0)",
        f"{res['z_net']:.2f} m",
        f"{'+' if diff_net >= 0 else ''}{diff_net:.2f} m vs Net ({NET_HEIGHT}m)",
        delta_color="normal" if not res["hit_net"] else "inverse",
    )
else:
    c4.metric("ระดับความสูงผ่านแนวเน็ต (At Net X=0)", "ลูกเคลื่อนที่ไม่ถึงตาข่าย")

# แสดงกราฟ 3D
st.plotly_chart(fig, use_container_width=True)