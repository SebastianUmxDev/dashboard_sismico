# -*- coding: utf-8 -*-
"""
==============================================================================
PORTAL GEOESPACIAL DE INTELIGENCIA Y RIESGO SÍSMICO EN COLOMBIA  |  v2
==============================================================================
Monitoreo Sísmico Nacional, Análisis Tectónico y Modelo Predictivo Random Forest
Acentos: Rojo Sísmico (#FF4D3D) y Verde Lima Neón (#C6FF4D)
Diseño: Cyber-Geology HUD, escaneo animado, contenedores nativos y micro-interacciones

Ejecutar:  streamlit run app.py
Requiere:  streamlit >= 1.40, pandas, numpy, plotly
"""

import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Riesgo Sísmico en Colombia | Centro de Inteligencia",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# ESTILOS CSS: CYBER-GEOLOGY HUD v2
# ==============================================================================
CSS = r"""
/* ==========================================================================
   CYBER-GEOLOGY HUD v2  |  Riesgo Sísmico en Colombia
   Un solo momento memorable: el barrido de escaneo del hero.
   Todo lo demás: preciso, silencioso y reactivo a la interacción.
   ========================================================================== */

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap');

:root {
    --bg: #05080D;
    --bg-2: #0A1019;
    --panel: rgba(14, 21, 33, 0.78);
    --line: rgba(255, 255, 255, 0.07);
    --line-hot: rgba(198, 255, 77, 0.35);
    --red: #FF4D3D;
    --lime: #C6FF4D;
    --amber: #FFA53D;
    --txt: #E6ECF5;
    --dim: #8A9BB3;
    --glow-red: 0 0 22px rgba(255, 77, 61, 0.38);
    --glow-lime: 0 0 22px rgba(198, 255, 77, 0.35);
    --ease: cubic-bezier(0.22, 1, 0.36, 1);
    --mono: 'JetBrains Mono', ui-monospace, monospace;
}

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

/* --------------------------------------------------------------------------
   FONDO: cuadrícula táctica que deriva lento + viñeta + aura de calor
   -------------------------------------------------------------------------- */
.stApp {
    background-color: var(--bg);
    background-image:
        radial-gradient(ellipse 60% 40% at 85% -10%, rgba(255, 77, 61, 0.10), transparent 70%),
        radial-gradient(ellipse 50% 40% at 0% 100%, rgba(198, 255, 77, 0.07), transparent 70%),
        linear-gradient(rgba(198, 255, 77, 0.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(198, 255, 77, 0.035) 1px, transparent 1px);
    background-size: auto, auto, 44px 44px, 44px 44px;
    animation: gridDrift 40s linear infinite;
    color: var(--txt);
}
@keyframes gridDrift {
    from { background-position: 0 0, 0 0, 0 0, 0 0; }
    to   { background-position: 0 0, 0 0, 44px 44px, 44px 44px; }
}

[data-testid="stHeader"] { background: transparent; }

/* Scrollbar */
::-webkit-scrollbar { width: 9px; height: 9px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, var(--lime), var(--red));
    border-radius: 9px;
    border: 2px solid var(--bg);
}

/* Selección de texto */
::selection { background: var(--lime); color: #05080D; }

/* Foco visible para teclado */
:focus-visible { outline: 2px solid var(--lime) !important; outline-offset: 2px; }

/* --------------------------------------------------------------------------
   HERO: marco HUD con esquinas + barrido de escaneo (momento memorable)
   -------------------------------------------------------------------------- */
.hero-hud {
    position: relative;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(12, 19, 31, 0.96) 0%, rgba(18, 28, 45, 0.86) 100%);
    border: 1px solid var(--line);
    border-radius: 14px;
    padding: 26px 32px 20px;
    margin-bottom: 26px;
    box-shadow: 0 18px 50px rgba(0, 0, 0, 0.55), inset 0 0 60px rgba(198, 255, 77, 0.03);
    backdrop-filter: blur(14px);
    animation: heroIn 0.9s var(--ease) both;
}
@keyframes heroIn {
    from { opacity: 0; transform: translateY(14px) scale(0.99); filter: blur(6px); }
    to   { opacity: 1; transform: none; filter: none; }
}

/* Barrido de escaneo */
.hero-hud::before {
    content: "";
    position: absolute;
    top: 0; bottom: 0; left: -30%;
    width: 30%;
    background: linear-gradient(90deg,
        transparent 0%,
        rgba(198, 255, 77, 0.00) 20%,
        rgba(198, 255, 77, 0.10) 70%,
        rgba(198, 255, 77, 0.55) 99%,
        transparent 100%);
    border-right: 1px solid rgba(198, 255, 77, 0.8);
    filter: drop-shadow(0 0 12px rgba(198, 255, 77, 0.7));
    pointer-events: none;
    animation: scanSweep 7s var(--ease) 1.2s infinite;
}
@keyframes scanSweep {
    0%   { left: -30%; opacity: 0; }
    8%   { opacity: 1; }
    55%  { left: 100%; opacity: 1; }
    56%, 100% { left: 100%; opacity: 0; }
}

/* Esquinas tipo visor (8 trazos) */
.hero-hud::after {
    content: "";
    position: absolute;
    inset: 8px;
    pointer-events: none;
    --c: var(--lime);
    --r: var(--red);
    background:
        linear-gradient(var(--r), var(--r)) top left / 22px 2px no-repeat,
        linear-gradient(var(--r), var(--r)) top left / 2px 22px no-repeat,
        linear-gradient(var(--c), var(--c)) top right / 22px 2px no-repeat,
        linear-gradient(var(--c), var(--c)) top right / 2px 22px no-repeat,
        linear-gradient(var(--r), var(--r)) bottom left / 22px 2px no-repeat,
        linear-gradient(var(--r), var(--r)) bottom left / 2px 22px no-repeat,
        linear-gradient(var(--c), var(--c)) bottom right / 22px 2px no-repeat,
        linear-gradient(var(--c), var(--c)) bottom right / 2px 22px no-repeat;
    opacity: 0.85;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    background: rgba(198, 255, 77, 0.08);
    color: var(--lime);
    border: 1px solid rgba(198, 255, 77, 0.3);
    padding: 5px 14px;
    border-radius: 9999px;
    font-family: var(--mono);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    margin-bottom: 10px;
}
.hero-title {
    color: #fff;
    font-size: clamp(1.9rem, 4vw, 2.9rem);
    font-weight: 800;
    letter-spacing: -0.03em;
    line-height: 1.08;
    margin: 0;
    text-shadow: 0 0 40px rgba(255, 255, 255, 0.08);
}
.hero-title span.col-red  { color: var(--red);  text-shadow: var(--glow-red); }
.hero-title span.col-lime { color: var(--lime); text-shadow: var(--glow-lime); }
.hero-subtitle {
    color: var(--dim);
    font-size: 0.96rem;
    line-height: 1.6;
    margin: 10px 0 0;
    max-width: 880px;
}

/* Punto de monitoreo pulsante */
.pulse-dot-green {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--lime);
    margin-right: 8px;
    vertical-align: middle;
    animation: pulseGreen 1.8s infinite cubic-bezier(0.66, 0, 0, 1);
}
@keyframes pulseGreen {
    0%   { box-shadow: 0 0 0 0 rgba(198, 255, 77, 0.7); }
    70%  { box-shadow: 0 0 0 10px rgba(198, 255, 77, 0); }
    100% { box-shadow: 0 0 0 0 rgba(198, 255, 77, 0); }
}

/* Sismógrafo: trazo que se dibuja con brillo */
.seismograph-container { width: 100%; height: 34px; overflow: hidden; margin-top: 14px; }
.seismic-trace {
    stroke-dasharray: 600;
    stroke-dashoffset: 600;
    filter: drop-shadow(0 0 4px rgba(255, 77, 61, 0.9));
    animation: seismographRun 4.2s linear infinite;
}
@keyframes seismographRun {
    0%   { stroke-dashoffset: 600; opacity: 0.35; }
    50%  { stroke-dashoffset: 0;   opacity: 1; }
    100% { stroke-dashoffset: -600; opacity: 0.35; }
}

/* --------------------------------------------------------------------------
   CONTENEDORES: sirven para .hud-box (HTML) y st.container(border=True)
   -------------------------------------------------------------------------- */
.hud-box,
[data-testid="stVerticalBlockBorderWrapper"]:has(> div > [data-testid="stVerticalBlock"]) {
    position: relative;
}
.hud-box {
    background: linear-gradient(145deg, rgba(16, 24, 38, 0.88), rgba(10, 16, 26, 0.96));
    border: 1px solid var(--line);
    border-radius: 12px;
    padding: 16px 18px;
    margin-bottom: 16px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
}
.hud-box-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px dashed rgba(198, 255, 77, 0.18);
}
.hud-box-title {
    display: flex;
    align-items: center;
    gap: 6px;
    margin: 0;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    color: var(--lime);
}

/* st.container(border=True): ahora SÍ envuelve widgets de verdad */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: linear-gradient(145deg, rgba(16, 24, 38, 0.82), rgba(10, 16, 26, 0.94));
    border: 1px solid var(--line) !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
    transition: border-color 0.3s var(--ease), box-shadow 0.3s var(--ease);
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: var(--line-hot) !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.45), 0 0 0 1px rgba(198, 255, 77, 0.06);
}

/* --------------------------------------------------------------------------
   SIDEBAR
   -------------------------------------------------------------------------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #070C14 0%, #05080D 100%);
    border-right: 1px solid var(--line);
    position: relative;
}
[data-testid="stSidebar"]::after {   /* hilo de luz vertical */
    content: "";
    position: absolute;
    top: 0; right: -1px;
    width: 1px; height: 100%;
    background: linear-gradient(180deg, transparent, var(--lime), var(--red), transparent);
    opacity: 0.5;
    background-size: 100% 300%;
    animation: edgeFlow 6s linear infinite;
    pointer-events: none;
}
@keyframes edgeFlow {
    from { background-position: 0 0; }
    to   { background-position: 0 300%; }
}

/* --------------------------------------------------------------------------
   BOTONES: barrido de luz al pasar el cursor
   -------------------------------------------------------------------------- */
div.stButton > button,
div.stDownloadButton > button {
    position: relative;
    overflow: hidden;
    width: 100% !important;
    border-radius: 10px !important;
    padding: 9px 14px !important;
    font-weight: 600 !important;
    font-size: 0.84rem !important;
    letter-spacing: 0.01em !important;
    color: var(--txt) !important;
    background: linear-gradient(135deg, #131E31, #0D1522) !important;
    border: 1px solid rgba(198, 255, 77, 0.22) !important;
    box-shadow: 0 3px 12px rgba(0, 0, 0, 0.35) !important;
    transition: transform 0.25s var(--ease), box-shadow 0.25s var(--ease),
                border-color 0.25s, color 0.25s !important;
}
div.stButton > button::before,
div.stDownloadButton > button::before {
    content: "";
    position: absolute;
    top: 0; left: -120%;
    width: 60%; height: 100%;
    background: linear-gradient(100deg, transparent, rgba(198, 255, 77, 0.28), transparent);
    transform: skewX(-20deg);
    transition: left 0.6s var(--ease);
}
div.stButton > button:hover::before,
div.stDownloadButton > button:hover::before { left: 140%; }

div.stButton > button:hover {
    transform: translateY(-2px) !important;
    color: var(--lime) !important;
    border-color: var(--lime) !important;
    box-shadow: 0 0 18px rgba(198, 255, 77, 0.35), inset 0 0 10px rgba(198, 255, 77, 0.08) !important;
}
div.stButton > button:active { transform: translateY(0) scale(0.98) !important; }

div.stDownloadButton > button {
    color: #fff !important;
    background: linear-gradient(135deg, rgba(255, 77, 61, 0.28), rgba(14, 21, 33, 0.95)) !important;
    border: 1px solid rgba(255, 77, 61, 0.5) !important;
    font-weight: 700 !important;
}
div.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    background: linear-gradient(135deg, #FF4D3D, #CF2F20) !important;
    border-color: var(--red) !important;
    box-shadow: 0 0 24px rgba(255, 77, 61, 0.55) !important;
}

/* --------------------------------------------------------------------------
   KPI: entrada escalonada (una sola vez) + barra de energía + elevación
   -------------------------------------------------------------------------- */
.kpi-card {
    position: relative;
    overflow: hidden;
    height: 100%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 18px 20px;
    background: linear-gradient(150deg, #0F1827, #142033);
    border: 1px solid var(--line);
    border-radius: 12px;
    box-shadow: 0 8px 26px rgba(0, 0, 0, 0.4);
    transition: transform 0.35s var(--ease), border-color 0.35s, box-shadow 0.35s;
    animation: kpiIn 0.8s var(--ease) both;
}
[data-testid="stColumn"]:nth-child(1) .kpi-card { animation-delay: 0.10s; }
[data-testid="stColumn"]:nth-child(2) .kpi-card { animation-delay: 0.20s; }
[data-testid="stColumn"]:nth-child(3) .kpi-card { animation-delay: 0.30s; }
[data-testid="stColumn"]:nth-child(4) .kpi-card { animation-delay: 0.40s; }
@keyframes kpiIn {
    from { opacity: 0; transform: translateY(22px); }
    to   { opacity: 1; transform: none; }
}
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 16px 38px rgba(0, 0, 0, 0.55); }
.kpi-card.lime-border:hover { border-color: rgba(198, 255, 77, 0.45); }
.kpi-card.red-border:hover  { border-color: rgba(255, 77, 61, 0.5); }

/* Barra lateral de energía */
.kpi-card::before {
    content: "";
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background-size: 100% 250%;
    animation: edgeFlow 4s linear infinite;
}
.kpi-card.lime-border::before {
    background-image: linear-gradient(180deg, var(--lime), transparent, var(--lime));
    box-shadow: var(--glow-lime);
}
.kpi-card.red-border::before {
    background-image: linear-gradient(180deg, var(--red), transparent, var(--red));
    box-shadow: var(--glow-red);
}
/* Retícula en la esquina */
.kpi-card::after {
    content: "";
    position: absolute;
    right: -20px; bottom: -20px;
    width: 90px; height: 90px;
    border-radius: 50%;
    border: 1px solid rgba(255, 255, 255, 0.05);
    box-shadow: 0 0 0 14px rgba(255, 255, 255, 0.02), 0 0 0 28px rgba(255, 255, 255, 0.015);
    pointer-events: none;
}

.kpi-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.kpi-tag { font-size: 0.78rem; font-weight: 700; letter-spacing: 0.05em; color: var(--dim); }
.kpi-icon {
    width: 34px; height: 34px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid var(--line);
    border-radius: 8px;
}
.kpi-main-number {
    font-family: var(--mono);
    font-size: 2.15rem;
    font-weight: 700;
    line-height: 1.1;
    margin-bottom: 6px;
    font-variant-numeric: tabular-nums;
}
.lime-border .kpi-main-number { color: var(--lime); text-shadow: 0 0 18px rgba(198, 255, 77, 0.35); }
.red-border  .kpi-main-number { color: var(--red);  text-shadow: 0 0 18px rgba(255, 77, 61, 0.4); }
.kpi-foot { display: flex; align-items: center; gap: 6px; font-size: 0.78rem; color: var(--dim); }
.kpi-foot b { color: #fff; }

/* --------------------------------------------------------------------------
   PÍLDORAS DE ALERTA (la roja respira)
   -------------------------------------------------------------------------- */
.pill-alerta {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 0.74rem;
    font-weight: 800;
    letter-spacing: 0.04em;
}
.pill-alerta.roja {
    background: rgba(255, 77, 61, 0.16);
    color: #FF6657;
    border: 1px solid var(--red);
    animation: alertBreath 2s ease-in-out infinite;
}
@keyframes alertBreath {
    0%, 100% { box-shadow: 0 0 4px rgba(255, 77, 61, 0.2); }
    50%      { box-shadow: 0 0 16px rgba(255, 77, 61, 0.6); }
}
.pill-alerta.naranja  { background: rgba(255, 165, 61, 0.16); color: var(--amber); border: 1px solid var(--amber); }
.pill-alerta.amarilla { background: rgba(255, 209, 102, 0.16); color: #FFD166; border: 1px solid #FFD166; }

/* --------------------------------------------------------------------------
   PESTAÑAS: la línea activa se desliza (tab-highlight nativo de Streamlit)
   -------------------------------------------------------------------------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    padding: 6px 8px;
    background: rgba(10, 16, 25, 0.9);
    border: 1px solid var(--line);
    border-radius: 12px;
    backdrop-filter: blur(8px);
}
.stTabs [data-baseweb="tab"] {
    height: auto;
    padding: 9px 16px;
    border-radius: 8px;
    font-size: 0.88rem;
    font-weight: 600;
    color: var(--dim);
    transition: color 0.2s, background 0.2s;
}
.stTabs [data-baseweb="tab"]:hover { color: #fff; background: rgba(255, 255, 255, 0.05); }
.stTabs [aria-selected="true"] { color: var(--lime) !important; background: rgba(198, 255, 77, 0.07) !important; }
.stTabs [data-baseweb="tab-highlight"] {
    background: linear-gradient(90deg, var(--red), var(--lime)) !important;
    height: 2px !important;
    box-shadow: 0 0 12px rgba(198, 255, 77, 0.7);
    transition: all 0.45s var(--ease) !important;
}
.stTabs [data-baseweb="tab-border"] { display: none; }

/* Contenido de cada pestaña aparece con un fundido corto */
.stTabs [data-baseweb="tab-panel"] { animation: panelIn 0.5s var(--ease) both; }
@keyframes panelIn {
    from { opacity: 0; transform: translateY(8px); }
    to   { opacity: 1; transform: none; }
}

/* --------------------------------------------------------------------------
   GRÁFICOS Y TABLAS: marco con mira, se iluminan al pasar el cursor
   -------------------------------------------------------------------------- */
[data-testid="stPlotlyChart"],
[data-testid="stDataFrame"] {
    border: 1px solid var(--line);
    border-radius: 12px;
    overflow: hidden;
    background: rgba(14, 21, 33, 0.6);
    transition: border-color 0.3s var(--ease), box-shadow 0.3s var(--ease);
}
[data-testid="stPlotlyChart"]:hover,
[data-testid="stDataFrame"]:hover {
    border-color: var(--line-hot);
    box-shadow: 0 0 0 1px rgba(198, 255, 77, 0.05), 0 10px 30px rgba(0, 0, 0, 0.45);
}

/* --------------------------------------------------------------------------
   MÉTRICAS NATIVAS, INPUTS, SELECT, SLIDERS
   -------------------------------------------------------------------------- */
[data-testid="stMetric"] {
    padding: 12px 16px;
    background: rgba(14, 21, 33, 0.7);
    border: 1px solid var(--line);
    border-left: 3px solid var(--lime);
    border-radius: 10px;
    transition: transform 0.25s var(--ease), border-color 0.25s;
}
[data-testid="stMetric"]:hover { transform: translateX(3px); border-left-color: var(--red); }
[data-testid="stMetricValue"] { font-family: var(--mono); color: var(--lime); }
[data-testid="stMetricLabel"] { color: var(--dim); }

.stTextInput input,
[data-baseweb="select"] > div {
    background: rgba(10, 16, 25, 0.9) !important;
    border: 1px solid var(--line) !important;
    border-radius: 10px !important;
    color: var(--txt) !important;
    transition: border-color 0.25s, box-shadow 0.25s;
}
.stTextInput input:focus,
[data-baseweb="select"] > div:focus-within {
    border-color: var(--lime) !important;
    box-shadow: 0 0 0 3px rgba(198, 255, 77, 0.14), var(--glow-lime) !important;
}

/* Sliders: pulgar lima con halo */
.stSlider [data-baseweb="slider"] { padding-top: 10px; }
.stSlider [role="slider"] {
    background: var(--lime) !important;
    border: 2px solid #05080D !important;
    box-shadow: 0 0 0 3px rgba(198, 255, 77, 0.25), var(--glow-lime) !important;
    transition: transform 0.2s var(--ease), box-shadow 0.2s;
}
.stSlider [role="slider"]:hover { transform: scale(1.25); }
.stSlider [data-testid="stSliderThumbValue"] { color: var(--lime); font-family: var(--mono); }

/* Segmented control (selector de capa del mapa) */
[data-testid="stSegmentedControl"] button[aria-checked="true"],
[data-testid="stSegmentedControl"] [aria-pressed="true"] {
    background: rgba(198, 255, 77, 0.12) !important;
    color: var(--lime) !important;
    border-color: var(--lime) !important;
    box-shadow: var(--glow-lime);
}

/* --------------------------------------------------------------------------
   TARJETA DE LIMITACIONES
   -------------------------------------------------------------------------- */
.box-limitaciones {
    position: relative;
    margin-top: 15px;
    padding: 26px;
    background: linear-gradient(145deg, rgba(22, 30, 46, 0.96), rgba(12, 18, 29, 0.98));
    border: 1px solid rgba(255, 77, 61, 0.35);
    border-left: 5px solid var(--red);
    border-radius: 12px;
    box-shadow: 0 10px 34px rgba(255, 77, 61, 0.08);
    overflow: hidden;
}
.box-limitaciones::before {   /* franjas de advertencia en el borde superior */
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: repeating-linear-gradient(-45deg, var(--red) 0 10px, transparent 10px 20px);
    background-size: 28px 100%;
    opacity: 0.7;
    animation: hazard 1.2s linear infinite;
}
@keyframes hazard { to { background-position: 28px 0; } }

/* --------------------------------------------------------------------------
   RESPONSIVE Y ACCESIBILIDAD
   -------------------------------------------------------------------------- */
@media (max-width: 768px) {
    .hero-hud { padding: 20px 18px 14px; }
    .kpi-main-number { font-size: 1.7rem; }
}
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}
"""
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


# ==============================================================================
# CARGA Y PROCESAMIENTO CON CACHÉ
# ==============================================================================
@st.cache_data(show_spinner=False)
def cargar_sismos():
    """Carga y limpia el catálogo sísmico desde data/."""
    ruta_primaria = os.path.join("data", "sismos_colombia_filtrados.csv")
    ruta_secundaria = os.path.join("data", "sismos_colombia_limpio_v3.csv")

    if os.path.exists(ruta_primaria):
        df = pd.read_csv(ruta_primaria)
    elif os.path.exists(ruta_secundaria):
        df = pd.read_csv(ruta_secundaria)
    else:
        st.error("No se encontró el archivo de sismos en 'data/'.")
        return pd.DataFrame()

    if pd.api.types.is_numeric_dtype(df["fecha_hora_utc"]):
        df["fecha_dt"] = pd.to_datetime(df["fecha_hora_utc"], unit="ms", utc=True)
    else:
        df["fecha_dt"] = pd.to_datetime(df["fecha_hora_utc"], format="mixed", utc=True)

    columnas_clave = ["id_evento", "fecha_dt", "magnitud", "profundidad_km", "latitud", "longitud"]
    cols_existentes = [c for c in columnas_clave if c in df.columns]
    df = df.dropna(subset=cols_existentes)
    df = df[df["magnitud"] > 0].copy()

    df["año"] = df["fecha_dt"].dt.year
    df["fecha_str"] = df["fecha_dt"].dt.strftime("%Y-%m-%d %H:%M UTC")

    df["regimen_profundidad"] = pd.cut(
        df["profundidad_km"],
        bins=[-0.1, 30, 120, 1000],
        labels=["Superficial (<30 km)", "Intermedio (30-120 km)", "Profundo (>120 km)"],
    )

    # Energía sísmica: log10(E) = 4.8 + 1.5 * M (Joules)
    df["energia_joules"] = 10.0 ** (4.8 + 1.5 * df["magnitud"])
    df["energia_tj"] = df["energia_joules"] / 1e12

    if "ubicacion_reportada" not in df.columns and "ubicacion" in df.columns:
        df["ubicacion_reportada"] = df["ubicacion"]
    elif "ubicacion_reportada" not in df.columns:
        df["ubicacion_reportada"] = "Colombia"
    df["ubicacion_reportada"] = df["ubicacion_reportada"].astype(str)

    if "fuente" not in df.columns:
        df["fuente"] = "N/D"

    return df


@st.cache_data(show_spinner=False)
def cargar_predicciones():
    """Carga las predicciones Random Forest y separa id_celda en lat/lon."""
    ruta = os.path.join("data", "predicciones_test_RF.csv")
    if not os.path.exists(ruta):
        return pd.DataFrame()

    df = pd.read_csv(ruta)
    coords = df["id_celda"].astype(str).str.split("_", expand=True)
    df["latitud"] = coords[0].astype(float)
    df["longitud"] = coords[1].astype(float)

    if "fecha_mes" in df.columns:
        df["fecha_mes"] = pd.to_datetime(df["fecha_mes"])

    return df


@st.cache_data(show_spinner=False)
def cargar_alertas():
    """Carga el dataset de alertas tempranas."""
    ruta = os.path.join("data", "alertas.csv")
    if not os.path.exists(ruta):
        return pd.DataFrame()
    df = pd.read_csv(ruta)
    df["nivel"] = df["nivel"].astype(str).str.strip().str.upper()
    return df


@st.cache_data(show_spinner=False)
def cargar_comparacion():
    """Carga la matriz de comparación final de modelos evaluados en test."""
    ruta = os.path.join("data", "comparacion_final_test.csv")
    if not os.path.exists(ruta):
        return pd.DataFrame()
    return pd.read_csv(ruta)


df_sismos_raw = cargar_sismos()
df_pred_raw = cargar_predicciones()
df_alertas = cargar_alertas()
df_comparacion = cargar_comparacion()

if df_sismos_raw.empty:
    st.stop()

min_year_global = int(df_sismos_raw["año"].min())
max_year_global = int(df_sismos_raw["año"].max())
min_mag_global = float(np.floor(df_sismos_raw["magnitud"].min() * 10) / 10)
max_mag_global = float(np.ceil(df_sismos_raw["magnitud"].max() * 10) / 10)
max_prof_global = float(np.ceil(df_sismos_raw["profundidad_km"].max()))


# ==============================================================================
# ESTADO DE SESIÓN Y CALLBACKS
# ==============================================================================
if "slider_ano" not in st.session_state:
    st.session_state["slider_ano"] = (min_year_global, max_year_global)
if "slider_mag" not in st.session_state:
    st.session_state["slider_mag"] = (min_mag_global, max_mag_global)
if "slider_prof" not in st.session_state:
    st.session_state["slider_prof"] = (0.0, max_prof_global)


def cb_preset_todo():
    st.session_state["slider_ano"] = (min_year_global, max_year_global)
    st.session_state["slider_mag"] = (min_mag_global, max_mag_global)
    st.session_state["slider_prof"] = (0.0, max_prof_global)


def cb_preset_mayor():
    st.session_state["slider_mag"] = (5.0, max_mag_global)


def cb_preset_superficial():
    st.session_state["slider_prof"] = (0.0, 30.0)


def cb_preset_decada():
    st.session_state["slider_ano"] = (max(min_year_global, 2015), max_year_global)


def box_header(titulo, etiqueta="", color="#8A9BB3"):
    """Encabezado HUD autocontenido (un solo st.markdown, sin divs abiertos)."""
    st.markdown(
        f'<div class="hud-box-header"><span class="hud-box-title">{titulo}</span>'
        f'<span style="color:{color}; font-size:0.7rem; font-family:\'JetBrains Mono\',monospace;">{etiqueta}</span></div>',
        unsafe_allow_html=True,
    )


# ==============================================================================
# BARRA LATERAL: CONTENEDORES NATIVOS (los widgets quedan DENTRO de las cajas)
# ==============================================================================
with st.sidebar:
    st.markdown(
        """
<div style="text-align:center; padding:6px 0 14px 0;">
<span style="font-size:1.8rem;">🌋</span>
<h3 style="color:#FFFFFF; font-size:1.15rem; margin:4px 0 2px 0; font-weight:800;">Centro de Control</h3>
<p style="color:#8A9BB3; font-size:0.76rem; margin:0;">Filtros tácticos y parámetros sísmicos</p>
</div>
""",
        unsafe_allow_html=True,
    )

    # CAJA 1: PREAJUSTES
    with st.container(border=True):
        box_header("⚡ Preajustes tácticos", "1 clic")
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            st.button("🌐 Total", on_click=cb_preset_todo, key="btn_todo",
                      help="Restablece todos los filtros al rango histórico completo.")
            st.button("💥 M ≥ 5.0", on_click=cb_preset_mayor, key="btn_mayor",
                      help="Sismos con magnitud igual o superior a 5.0.")
        with col_btn2:
            st.button("⚡ Superficial", on_click=cb_preset_superficial, key="btn_sup",
                      help="Hipocentros con profundidad menor a 30 km.")
            st.button("📅 2015+", on_click=cb_preset_decada, key="btn_decada",
                      help="Sismicidad de la última década.")

    # CAJA 2: FILTROS
    with st.container(border=True):
        box_header("🎛️ Filtros de selección", "dinámico", "#C6FF4D")
        rango_años = st.slider(
            "📅 Rango de años",
            min_value=min_year_global, max_value=max_year_global, step=1, key="slider_ano",
        )
        rango_magnitud = st.slider(
            "⚡ Magnitud (Mw/mb)",
            min_value=min_mag_global, max_value=max_mag_global, step=0.1, key="slider_mag",
        )
        rango_profundidad = st.slider(
            "🔻 Profundidad hipocentral (km)",
            min_value=0.0, max_value=max_prof_global, step=5.0, key="slider_prof",
        )
        tam_burbuja = st.slider("🔘 Escala de marcadores", min_value=10, max_value=26, value=18, step=2)

    # Filtrado
    mask_filtro = (
        (df_sismos_raw["año"] >= rango_años[0])
        & (df_sismos_raw["año"] <= rango_años[1])
        & (df_sismos_raw["magnitud"] >= rango_magnitud[0])
        & (df_sismos_raw["magnitud"] <= rango_magnitud[1])
        & (df_sismos_raw["profundidad_km"] >= rango_profundidad[0])
        & (df_sismos_raw["profundidad_km"] <= rango_profundidad[1])
    )
    df_sismos = df_sismos_raw[mask_filtro].copy()
    pct_cat = (len(df_sismos) / len(df_sismos_raw) * 100) if len(df_sismos_raw) > 0 else 0

    # CAJA 3: RESUMEN + DESCARGA
    with st.container(border=True):
        box_header("📊 Resumen operativo", f"{pct_cat:.1f}%", "#C6FF4D")
        st.markdown(
            f"""
<div style="font-size:0.8rem; line-height:1.8;">
<div style="display:flex; justify-content:space-between;"><span style="color:#8A9BB3;">Eventos activos</span><b style="color:#FFFFFF; font-family:'JetBrains Mono',monospace;">{len(df_sismos):,} / {len(df_sismos_raw):,}</b></div>
<div style="display:flex; justify-content:space-between;"><span style="color:#8A9BB3;">Periodo</span><b style="color:#C6FF4D;">{rango_años[0]} – {rango_años[1]}</b></div>
<div style="display:flex; justify-content:space-between;"><span style="color:#8A9BB3;">Magnitud</span><b style="color:#FF4D3D;">{rango_magnitud[0]:.1f} – {rango_magnitud[1]:.1f}</b></div>
</div>
""",
            unsafe_allow_html=True,
        )
        csv_filtrado = df_sismos.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Descargar catálogo CSV",
            data=csv_filtrado,
            file_name=f"sismos_colombia_{rango_años[0]}_{rango_años[1]}.csv",
            mime="text/csv",
            key="btn_descarga_csv",
        )


# ==============================================================================
# HERO CON ESCANEO Y TRAZO SISMOGRÁFICO
# ==============================================================================
st.markdown(
    """
<div class="hero-hud">
<div class="hero-badge"><span class="pulse-dot-green"></span>MONITOREO SÍSMICO NACIONAL ACTIVO</div>
<h1 class="hero-title">Riesgo Sísmico en <span class="col-red">Colom</span><span class="col-lime">bia</span></h1>
<p class="hero-subtitle">Plataforma analítica e interactiva para la vigilancia de sismicidad histórica, geofísica de hipocentros y evaluación predictiva mensual basada en <b>Random Forest (1°x1°)</b>.</p>
<div class="seismograph-container">
<svg viewBox="0 0 800 40" preserveAspectRatio="none" style="width:100%; height:32px;">
<defs>
<linearGradient id="seisGrad" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#C6FF4D" stop-opacity="0.3"/>
<stop offset="50%" stop-color="#FF4D3D" stop-opacity="1"/>
<stop offset="100%" stop-color="#C6FF4D" stop-opacity="0.3"/>
</linearGradient>
</defs>
<path class="seismic-trace" d="M0,20 L120,20 L130,8 L140,32 L150,2 L160,38 L170,14 L180,26 L190,20 L360,20 L370,5 L380,35 L390,0 L400,40 L410,10 L420,30 L430,20 L620,20 L630,9 L640,31 L650,20 L800,20" fill="none" stroke="url(#seisGrad)" stroke-width="2.2"/>
</svg>
</div>
</div>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# AGREGACIÓN ESPACIAL DE CELDAS PREDICTIVAS
# ==============================================================================
if not df_pred_raw.empty:
    df_celdas_agg = (
        df_pred_raw.groupby(["id_celda", "latitud", "longitud"])
        .agg(
            prob_RF_mean=("prob_RF", "mean"),
            prob_RF_max=("prob_RF", "max"),
            eventos_reales=("y_prox_mes", "sum"),
            meses_evaluados=("fecha_mes", "count"),
        )
        .reset_index()
    )
    if not df_celdas_agg.empty:
        celda_max_row = df_celdas_agg.sort_values(by="prob_RF_mean", ascending=False).iloc[0]
        top_celda_nombre = celda_max_row["id_celda"]
        top_celda_prob = celda_max_row["prob_RF_mean"] * 100
    else:
        top_celda_nombre, top_celda_prob = "N/D", 0.0
else:
    df_celdas_agg = pd.DataFrame()
    top_celda_nombre, top_celda_prob = "N/D", 0.0


# ==============================================================================
# 4 TARJETAS KPI
# ==============================================================================
kpi_c1, kpi_c2, kpi_c3, kpi_c4 = st.columns(4)

with kpi_c1:
    st.markdown(
        f"""
<div class="kpi-card lime-border">
<div class="kpi-top"><span class="kpi-tag">Total de sismos</span><div class="kpi-icon">🌋</div></div>
<div class="kpi-main-number">{len(df_sismos):,}</div>
<div class="kpi-foot"><span>Catálogo filtrado:</span> <b>{pct_cat:.1f}%</b></div>
</div>
""",
        unsafe_allow_html=True,
    )

max_m_val = df_sismos["magnitud"].max() if len(df_sismos) > 0 else 0.0
en_tj_val = df_sismos["energia_tj"].sum() if len(df_sismos) > 0 else 0.0
with kpi_c2:
    st.markdown(
        f"""
<div class="kpi-card red-border">
<div class="kpi-top"><span class="kpi-tag">Magnitud máxima</span><div class="kpi-icon">⚡</div></div>
<div class="kpi-main-number">{max_m_val:.1f} <span style="font-size:1.15rem; font-weight:600;">Mw</span></div>
<div class="kpi-foot"><span>Energía liberada:</span> <b>{en_tj_val:,.0f} TJ</b></div>
</div>
""",
        unsafe_allow_html=True,
    )

n_rojas = len(df_alertas[df_alertas["nivel"] == "ROJA"]) if not df_alertas.empty else 0
n_tot_alertas = len(df_alertas) if not df_alertas.empty else 1
with kpi_c3:
    st.markdown(
        f"""
<div class="kpi-card red-border">
<div class="kpi-top"><span class="kpi-tag">Alertas rojas</span><div class="kpi-icon">🚨</div></div>
<div class="kpi-main-number">{n_rojas}</div>
<div class="kpi-foot"><span>{n_rojas}/{n_tot_alertas} alertas</span> <b>({(n_rojas / n_tot_alertas) * 100:.0f}% críticas)</b></div>
</div>
""",
        unsafe_allow_html=True,
    )

with kpi_c4:
    st.markdown(
        f"""
<div class="kpi-card lime-border">
<div class="kpi-top"><span class="kpi-tag">Celda de mayor riesgo</span><div class="kpi-icon">🎯</div></div>
<div class="kpi-main-number" style="font-size:1.85rem;">{top_celda_nombre}</div>
<div class="kpi-foot"><span>Probabilidad media:</span> <b style="color:#C6FF4D;">{top_celda_prob:.1f}%</b></div>
</div>
""",
        unsafe_allow_html=True,
    )

st.markdown("<div style='margin-bottom:22px;'></div>", unsafe_allow_html=True)


# ==============================================================================
# WRAPPERS PARA MAPAS PLOTLY (compatibles con 5.x y 6.x/7.x)
# ==============================================================================
PALETA_COLOR_RIESGO = [
    [0.0, "#22c55e"],
    [0.25, "#C6FF4D"],
    [0.6, "#FFA53D"],
    [1.0, "#FF4D3D"],
]


def render_scatter_map(df, **kwargs):
    if hasattr(px, "scatter_map"):
        style = kwargs.pop("mapbox_style", kwargs.pop("map_style", "carto-darkmatter"))
        kwargs["map_style"] = style
        return px.scatter_map(df, **kwargs)
    elif hasattr(px, "scatter_mapbox"):
        style = kwargs.pop("map_style", kwargs.pop("mapbox_style", "carto-darkmatter"))
        kwargs["mapbox_style"] = style
        return px.scatter_mapbox(df, **kwargs)
    return px.scatter(df, x="longitud", y="latitud", size="magnitud", color="magnitud")


def render_density_map(df, **kwargs):
    if hasattr(px, "density_map"):
        style = kwargs.pop("mapbox_style", kwargs.pop("map_style", "carto-darkmatter"))
        kwargs["map_style"] = style
        return px.density_map(df, **kwargs)
    elif hasattr(px, "density_mapbox"):
        style = kwargs.pop("map_style", kwargs.pop("mapbox_style", "carto-darkmatter"))
        kwargs["mapbox_style"] = style
        return px.density_mapbox(df, **kwargs)
    return px.scatter(df, x="longitud", y="latitud", color="prob_RF_mean")


def build_burbujas_fig(df, max_dot_size=18):
    if df.empty:
        fig = go.Figure()
        fig.update_layout(template="plotly_dark", title="Sin eventos en el rango filtrado")
        return fig

    fig = render_scatter_map(
        df,
        lat="latitud",
        lon="longitud",
        size="magnitud",
        color="magnitud",
        color_continuous_scale=PALETA_COLOR_RIESGO,
        hover_name="ubicacion_reportada",
        hover_data={
            "latitud": ":.2f",
            "longitud": ":.2f",
            "magnitud": ":.1f",
            "profundidad_km": ":.1f km",
            "fecha_str": True,
            "regimen_profundidad": True,
        },
        zoom=4.85,
        center={"lat": 4.57, "lon": -74.29},
        size_max=max_dot_size,
        labels={
            "magnitud": "Magnitud",
            "profundidad_km": "Profundidad",
            "fecha_str": "Fecha UTC",
            "regimen_profundidad": "Régimen",
        },
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=550,
        coloraxis_colorbar=dict(
            title=dict(text="Magnitud", font=dict(color="#FFFFFF", size=12)),
            tickfont=dict(color="#94A3B8"),
            bgcolor="rgba(16, 23, 36, 0.85)",
            bordercolor="rgba(255, 255, 255, 0.1)",
            borderwidth=1,
            len=0.72,
            x=0.98,
            xanchor="right",
        ),
    )
    return fig


def build_calor_fig(df_celdas):
    if df_celdas.empty:
        fig = go.Figure()
        fig.update_layout(template="plotly_dark", title="Sin celdas predictivas disponibles")
        return fig

    df_plot = df_celdas.copy()
    df_plot["prob_pct"] = (df_plot["prob_RF_mean"] * 100).round(1).astype(str) + "%"
    df_plot["prob_max_pct"] = (df_plot["prob_RF_max"] * 100).round(1).astype(str) + "%"

    fig = render_density_map(
        df_plot,
        lat="latitud",
        lon="longitud",
        z="prob_RF_mean",
        radius=45,
        color_continuous_scale=PALETA_COLOR_RIESGO,
        range_color=[0, 1.0],
        hover_name="id_celda",
        hover_data={
            "latitud": ":.2f",
            "longitud": ":.2f",
            "prob_pct": True,
            "prob_max_pct": True,
            "eventos_reales": True,
            "prob_RF_mean": False,
        },
        labels={
            "prob_pct": "Prob. media RF",
            "prob_max_pct": "Prob. máxima RF",
            "eventos_reales": "Eventos históricos",
            "latitud": "Latitud",
            "longitud": "Longitud",
        },
        zoom=4.85,
        center={"lat": 4.57, "lon": -74.29},
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=550,
        coloraxis_colorbar=dict(
            title=dict(text="Probabilidad RF", font=dict(color="#FFFFFF", size=12)),
            tickformat=".0%",
            tickfont=dict(color="#94A3B8"),
            bgcolor="rgba(16, 23, 36, 0.85)",
            bordercolor="rgba(255, 255, 255, 0.1)",
            borderwidth=1,
            len=0.72,
            x=0.98,
            xanchor="right",
        ),
    )
    return fig


# ==============================================================================
# PESTAÑAS
# ==============================================================================
tab_mapas, tab_geofisica, tab_ia, tab_alertas, tab_limitaciones = st.tabs(
    [
        "🗺️ Centro geoespacial",
        "📈 Dinámica geofísica y energía",
        "🤖 Inteligencia artificial y celdas",
        "🚨 Monitor de alertas y eventos",
        "⚠️ Metodología y limitaciones",
    ]
)

# ------------------------------------------------------------------------------
# PESTAÑA 1: CENTRO GEOESPACIAL
# ------------------------------------------------------------------------------
with tab_mapas:
    col_map_h1, col_map_h2 = st.columns([3, 1])
    with col_map_h1:
        st.markdown("#### 🌐 Explorador cartográfico de sismicidad y riesgo")
    with col_map_h2:
        modo_capa = st.segmented_control(
            "Capa activa",
            ["Burbujas", "Calor (RF)", "Lado a lado"],
            default="Burbujas",
            label_visibility="collapsed",
        )
        if not modo_capa:
            modo_capa = "Burbujas"

    if modo_capa == "Burbujas":
        st.caption("📍 Puntos sísmicos escalados y coloreados por magnitud. Pasa el cursor para ver los detalles.")
        st.plotly_chart(build_burbujas_fig(df_sismos, max_dot_size=tam_burbuja), use_container_width=True)

    elif modo_capa == "Calor (RF)":
        st.caption("🔥 Superficie de densidad probabilística estimada por Random Forest para cuadrículas de 1°x1°.")
        st.plotly_chart(build_calor_fig(df_celdas_agg), use_container_width=True)

    else:
        col_la, col_lb = st.columns(2)
        with col_la:
            st.markdown("##### 📍 Sismicidad observada")
            st.plotly_chart(build_burbujas_fig(df_sismos, max_dot_size=tam_burbuja), use_container_width=True)
        with col_lb:
            st.markdown("##### 🔥 Riesgo predictivo (Random Forest)")
            st.plotly_chart(build_calor_fig(df_celdas_agg), use_container_width=True)


# ------------------------------------------------------------------------------
# PESTAÑA 2: DINÁMICA GEOFÍSICA Y ENERGÍA
# ------------------------------------------------------------------------------
with tab_geofisica:
    st.markdown("#### 📊 Análisis geofísico de hipocentros, frecuencia y energía")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        if len(df_sismos) > 0:
            df_anual = df_sismos.groupby("año").agg(
                total_sismos=("id_evento", "count"),
                mag_prom=("magnitud", "mean"),
            ).reset_index()

            fig_anual = go.Figure()
            fig_anual.add_trace(go.Scatter(
                x=df_anual["año"],
                y=df_anual["total_sismos"],
                mode="lines+markers",
                name="Sismos / año",
                line=dict(color="#FF4D3D", width=2.8, shape="spline"),
                marker=dict(size=7, color="#C6FF4D", line=dict(width=1.5, color="#101724")),
                fill="tozeroy",
                fillcolor="rgba(255, 77, 61, 0.12)",
                hovertemplate="<b>Año %{x}</b><br>Sismos: %{y:,}<br>Mag. media: %{customdata:.2f} Mw<extra></extra>",
                customdata=df_anual["mag_prom"],
            ))
            fig_anual.update_layout(
                title=dict(text="<b>Frecuencia anual de eventos sísmicos</b>", font=dict(color="#FFFFFF", size=14)),
                template="plotly_dark",
                paper_bgcolor="#0E1521",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=45, r=20, t=45, b=40),
                height=350,
                xaxis=dict(title=dict(text="Año", font=dict(color="#94A3B8")), gridcolor="#1E293B"),
                yaxis=dict(title=dict(text="Número de eventos", font=dict(color="#94A3B8")), gridcolor="#1E293B"),
            )
            st.plotly_chart(fig_anual, use_container_width=True)
        else:
            st.info("Sin registros en el rango seleccionado.")

    with col_g2:
        if len(df_sismos) > 0:
            fig_hist = px.histogram(
                df_sismos,
                x="profundidad_km",
                color="regimen_profundidad",
                color_discrete_map={
                    "Superficial (<30 km)": "#FF4D3D",
                    "Intermedio (30-120 km)": "#FFA53D",
                    "Profundo (>120 km)": "#C6FF4D",
                },
                nbins=35,
                title="<b>Distribución hipocentral por régimen geológico</b>",
                labels={"profundidad_km": "Profundidad hipocentral (km)", "count": "Frecuencia"},
            )
            fig_hist.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0E1521",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=45, r=20, t=45, b=40),
                height=350,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                            font=dict(size=10, color="#94A3B8")),
                xaxis=dict(title=dict(text="Profundidad (km)", font=dict(color="#94A3B8")), gridcolor="#1E293B"),
                yaxis=dict(title=dict(text="Frecuencia", font=dict(color="#94A3B8")), gridcolor="#1E293B"),
            )
            st.plotly_chart(fig_hist, use_container_width=True)

    col_g3, col_g4 = st.columns(2)

    with col_g3:
        if len(df_sismos) >= 20:
            m_bins = np.round(np.arange(2.5, 7.2, 0.2), 1)
            gr_rows = []
            for mb in m_bins:
                cnt = (df_sismos["magnitud"] >= mb).sum()
                if cnt > 0:
                    gr_rows.append({"magnitud": mb, "log_n": np.log10(cnt), "conteo": cnt})
            df_gr = pd.DataFrame(gr_rows)

            if len(df_gr) >= 2:
                sub_fit = df_gr[(df_gr["magnitud"] >= 3.4) & (df_gr["magnitud"] <= 5.8)]
                if len(sub_fit) >= 2:
                    slope, intercept = np.polyfit(sub_fit["magnitud"], sub_fit["log_n"], 1)
                    b_param = -slope
                    fit_vals = intercept + slope * df_gr["magnitud"]
                else:
                    b_param = 1.0
                    fit_vals = df_gr["log_n"]

                fig_gr = go.Figure()
                fig_gr.add_trace(go.Scatter(
                    x=df_gr["magnitud"], y=df_gr["log_n"], mode="markers",
                    name="log10 N(M ≥ m)", marker=dict(size=8, color="#C6FF4D", symbol="circle"),
                ))
                fig_gr.add_trace(go.Scatter(
                    x=df_gr["magnitud"], y=fit_vals, mode="lines",
                    name=f"Ajuste G-R (b = {b_param:.2f})", line=dict(color="#FF4D3D", width=2, dash="dash"),
                ))
                fig_gr.update_layout(
                    title=dict(text=f"<b>Frecuencia-magnitud (Gutenberg-Richter, b={b_param:.2f})</b>",
                               font=dict(color="#FFFFFF", size=14)),
                    template="plotly_dark",
                    paper_bgcolor="#0E1521",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=45, r=20, t=45, b=40),
                    height=340,
                    xaxis=dict(title=dict(text="Magnitud de corte (m)", font=dict(color="#94A3B8")), gridcolor="#1E293B"),
                    yaxis=dict(title=dict(text="log10 N acumulado", font=dict(color="#94A3B8")), gridcolor="#1E293B"),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                )
                st.plotly_chart(fig_gr, use_container_width=True)
            else:
                st.info("Insuficientes datos para la relación Gutenberg-Richter.")
        else:
            st.info("Insuficientes datos para la relación Gutenberg-Richter.")

    with col_g4:
        if len(df_sismos) > 0:
            df_en = df_sismos.groupby("año")["energia_tj"].sum().reset_index()
            fig_en = px.bar(
                df_en, x="año", y="energia_tj",
                title="<b>Energía sísmica liberada anual (terajoules, TJ)</b>",
                color_discrete_sequence=["#FF4D3D"],
            )
            fig_en.update_traces(
                marker=dict(line=dict(width=1, color="#0E1521")),
                hovertemplate="Año %{x}<br>Energía: %{y:,.1f} TJ<extra></extra>",
            )
            fig_en.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0E1521",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=45, r=20, t=45, b=40),
                height=340,
                xaxis=dict(title=dict(text="Año", font=dict(color="#94A3B8")), gridcolor="#1E293B"),
                yaxis=dict(title=dict(text="Energía (TJ)", font=dict(color="#94A3B8")), gridcolor="#1E293B"),
            )
            st.plotly_chart(fig_en, use_container_width=True)


# ------------------------------------------------------------------------------
# PESTAÑA 3: INTELIGENCIA ARTIFICIAL Y CELDAS
# ------------------------------------------------------------------------------
with tab_ia:
    st.markdown("#### 🤖 Evaluación predictiva: Random Forest y modelos comparativos")

    col_ia_a, col_ia_b = st.columns(2)

    with col_ia_a:
        st.markdown("##### 🎯 Top 10 celdas de mayor probabilidad media")
        if not df_celdas_agg.empty:
            top10_df = df_celdas_agg.sort_values(by="prob_RF_mean", ascending=False).head(10).copy()
            top10_df["Rank"] = range(1, len(top10_df) + 1)
            top10_df["prob_bar"] = top10_df["prob_RF_mean"]

            st.dataframe(
                top10_df[["Rank", "id_celda", "latitud", "longitud", "prob_bar", "eventos_reales"]],
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Rank": st.column_config.NumberColumn("#", width="small"),
                    "id_celda": st.column_config.TextColumn("Celda", width="small"),
                    "latitud": st.column_config.NumberColumn("Lat", format="%.1f°"),
                    "longitud": st.column_config.NumberColumn("Lon", format="%.1f°"),
                    "prob_bar": st.column_config.ProgressColumn(
                        "Prob. RF media",
                        help="Probabilidad calculada por Random Forest en test",
                        format="percent",
                        min_value=0.0,
                        max_value=1.0,
                    ),
                    "eventos_reales": st.column_config.NumberColumn("Sismos reales", width="small"),
                },
            )
        else:
            st.info("No hay predicciones disponibles en data/predicciones_test_RF.csv.")

    with col_ia_b:
        st.markdown("##### 🔬 Comparativa multi-métrica en test")
        if not df_comparacion.empty:
            fig_comp = go.Figure()
            fig_comp.add_trace(go.Bar(
                x=df_comparacion["modelo"], y=df_comparacion["PR-AUC test"],
                name="PR-AUC test", marker_color="#C6FF4D",
            ))
            fig_comp.add_trace(go.Bar(
                x=df_comparacion["modelo"], y=df_comparacion["Recall top10%"],
                name="Recall top 10%", marker_color="#FF4D3D",
            ))
            fig_comp.update_layout(
                barmode="group",
                template="plotly_dark",
                paper_bgcolor="#0E1521",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=45, r=20, t=35, b=60),
                height=300,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10)),
                xaxis=dict(tickangle=-25, tickfont=dict(size=10, color="#94A3B8")),
                yaxis=dict(title=dict(text="Score", font=dict(color="#94A3B8")), gridcolor="#1E293B"),
            )
            st.plotly_chart(fig_comp, use_container_width=True)
        else:
            st.info("No hay matriz de comparación en data/comparacion_final_test.csv.")

    st.markdown("---")
    st.markdown("##### 🔍 Auditor temporal por celda: probabilidad RF vs. ocurrencia real")

    if not df_pred_raw.empty:
        celdas_disponibles = df_celdas_agg.sort_values(by="prob_RF_mean", ascending=False)["id_celda"].tolist()
        celda_elegida = st.selectbox("Selecciona una celda para auditar:", celdas_disponibles, index=0)

        df_time_c = df_pred_raw[df_pred_raw["id_celda"] == celda_elegida].sort_values("fecha_mes")

        met1, met2, met3 = st.columns(3)
        with met1:
            st.metric("Probabilidad promedio", f"{df_time_c['prob_RF'].mean() * 100:.1f}%")
        with met2:
            st.metric("Probabilidad máxima", f"{df_time_c['prob_RF'].max() * 100:.1f}%")
        with met3:
            st.metric("Meses con evento real (y=1)", f"{int(df_time_c['y_prox_mes'].sum())} / {len(df_time_c)}")

        fig_audit = go.Figure()
        fig_audit.add_trace(go.Scatter(
            x=df_time_c["fecha_mes"], y=df_time_c["prob_RF"],
            mode="lines+markers", name="Probabilidad RF",
            line=dict(color="#C6FF4D", width=2.5), marker=dict(size=5, color="#C6FF4D"),
            hovertemplate="Mes: %{x|%Y-%m}<br>Probabilidad: %{y:.1%}<extra></extra>",
        ))
        df_real_pts = df_time_c[df_time_c["y_prox_mes"] == 1]
        fig_audit.add_trace(go.Scatter(
            x=df_real_pts["fecha_mes"], y=df_real_pts["prob_RF"],
            mode="markers", name="Evento real ocurrido (y=1)",
            marker=dict(size=12, color="#FF4D3D", symbol="diamond", line=dict(width=1.5, color="#FFFFFF")),
            hovertemplate="<b>¡Sismo real registrado!</b><br>Mes: %{x|%Y-%m}<br>Prob. asignada: %{y:.1%}<extra></extra>",
        ))
        fig_audit.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0E1521",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=45, r=20, t=30, b=40),
            height=320,
            yaxis=dict(title=dict(text="Probabilidad RF", font=dict(color="#94A3B8")),
                       tickformat=".0%", gridcolor="#1E293B"),
            xaxis=dict(title=dict(text="Mes", font=dict(color="#94A3B8")), gridcolor="#1E293B"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        st.plotly_chart(fig_audit, use_container_width=True)


# ------------------------------------------------------------------------------
# PESTAÑA 4: MONITOR DE ALERTAS Y EVENTOS
# ------------------------------------------------------------------------------
with tab_alertas:
    st.markdown("#### 🚨 Centro de alertas tempranas y catálogo detallado")

    col_alt1, col_alt2 = st.columns([1, 2])

    with col_alt1:
        st.markdown("##### 📌 Desglose de alertas")
        if not df_alertas.empty:
            conteo_al = df_alertas["nivel"].value_counts().reset_index()
            conteo_al.columns = ["nivel", "conteo"]

            fig_pie_al = px.pie(
                conteo_al, names="nivel", values="conteo", hole=0.55, color="nivel",
                color_discrete_map={"ROJA": "#FF4D3D", "NARANJA": "#FFA53D", "AMARILLA": "#FFD166"},
            )
            fig_pie_al.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=10, r=10, t=10, b=10),
                height=260,
                legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
            )
            st.plotly_chart(fig_pie_al, use_container_width=True)
        else:
            st.info("No hay alertas en data/alertas.csv.")

    with col_alt2:
        st.markdown("##### 📋 Registro reciente de alertas")
        if not df_alertas.empty:
            orden = "magnitud" if "magnitud" in df_alertas.columns else df_alertas.columns[0]
            st.dataframe(
                df_alertas.sort_values(by=orden, ascending=False),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "nivel": st.column_config.TextColumn("Nivel alerta", width="small"),
                    "magnitud": st.column_config.NumberColumn("Magnitud", format="%.1f Mw"),
                    "ubicacion": st.column_config.TextColumn("Ubicación", width="large"),
                    "fecha_hora_utc": st.column_config.TextColumn("Fecha UTC"),
                    "id_evento": st.column_config.TextColumn("ID evento", width="small"),
                },
            )

    st.markdown("---")
    st.markdown("##### 🔍 Búsqueda en el catálogo filtrado")
    termino_busc = st.text_input(
        "Filtrar por municipio, departamento o ID (ej. 'Bucaramanga', 'Chocó', 'Calvario'):",
        "", key="txt_buscar",
    )

    if len(df_sismos) > 0:
        if termino_busc.strip():
            df_tabla_ev = df_sismos[
                df_sismos["ubicacion_reportada"].str.contains(termino_busc, case=False, na=False, regex=False)
                | df_sismos["id_evento"].astype(str).str.contains(termino_busc, case=False, na=False, regex=False)
            ]
        else:
            df_tabla_ev = df_sismos.head(150)

        st.caption(f"Mostrando {len(df_tabla_ev):,} eventos ordenados cronológicamente:")
        st.dataframe(
            df_tabla_ev[["id_evento", "fecha_str", "magnitud", "profundidad_km", "ubicacion_reportada", "fuente"]]
            .sort_values("fecha_str", ascending=False),
            use_container_width=True,
            hide_index=True,
            column_config={
                "id_evento": st.column_config.TextColumn("ID", width="small"),
                "fecha_str": st.column_config.TextColumn("Fecha / hora UTC", width="medium"),
                "magnitud": st.column_config.NumberColumn("Magnitud", format="%.1f"),
                "profundidad_km": st.column_config.NumberColumn("Profundidad", format="%.1f km"),
                "ubicacion_reportada": st.column_config.TextColumn("Ubicación reportada", width="large"),
                "fuente": st.column_config.TextColumn("Fuente", width="small"),
            },
        )
    else:
        st.warning("No hay sismos para mostrar con los filtros actuales.")


# ------------------------------------------------------------------------------
# PESTAÑA 5: METODOLOGÍA Y LIMITACIONES
# ------------------------------------------------------------------------------
with tab_limitaciones:
    st.markdown(
        """
<div class="box-limitaciones">
<h3 style="color:#FF4D3D; margin-top:0;">⚠️ Evaluación rigurosa y limitaciones del modelo</h3>
<p style="color:#E6ECF5; font-size:0.95rem; line-height:1.65;">
<b>Desempeño demostrado y ganancia predictiva:</b><br>
El clasificador <b>Random Forest</b> (junto con la familia de modelos evaluados en test) muestra un <b>Lift de ~3.15x a 3.77x</b> sobre la tasa aleatoria base y sobre el baseline histórico de sismicidad. Además, captura más del <b>41% de los eventos significativos</b> concentrándose solo en el 10% de celdas con mayor alerta priorizada (<b>Recall top 10% = 0.411</b>).
</p>
<hr style="border:0; border-top:1px solid rgba(255,77,61,0.2); margin:18px 0;">
<p style="color:#E6ECF5; font-size:0.95rem; line-height:1.65;">
<b>Imposibilidad de predicción determinista puntual:</b><br>
El modelo <b>NO predice ni puede predecir sismos exactos</b>: ni el día, ni la hora, ni la falla individual que se romperá. La nucleación de fallas y la acumulación de esfuerzos en la corteza tienen un comportamiento caótico y no lineal.
</p>
<hr style="border:0; border-top:1px solid rgba(255,77,61,0.2); margin:18px 0;">
<p style="color:#8A9BB3; font-size:0.88rem; line-height:1.6; margin-bottom:0;">
<b style="color:#C6FF4D;">Propósito operativo institucional:</b><br>
Esta plataforma es una herramienta de <b>priorización probabilística mensual sobre una cuadrícula de 1° x 1°</b>. Su valor está en orientar decisiones preventivas: asignación de recursos para organismos de socorro, densificación de instrumentación sismológica, reforzamiento estructural en zonas de alta probabilidad y simulacros focalizados.
</p>
</div>
""",
        unsafe_allow_html=True,
    )


# ==============================================================================
# PIE DE PÁGINA
# ==============================================================================
st.markdown(
    """
<div style="text-align:center; color:#64748B; font-size:0.8rem; padding:32px 0 16px 0; border-top:1px solid rgba(255,255,255,0.05); margin-top:30px;">
<b>Portal de Inteligencia y Riesgo Sísmico en Colombia</b> | Desarrollado con <b>Streamlit y Plotly</b> | Paleta Cyber-Geology (#FF4D3D / #C6FF4D)
</div>
""",
    unsafe_allow_html=True,
)