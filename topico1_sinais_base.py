"""
=============================================================================
ATIVIDADE DE SIMULACAO - MODULACAO ANGULAR (FM e PM)
Topico 1 - Observacao dos sinais base: portadora c(t) e mensagem m(t)
=============================================================================

Objetivo:
    Gerar os sinais fundamentais que serao usados nos proximos topicos
    (portadora e mensagem), analisar seus parametros e visualizar seu
    comportamento no dominio do tempo em escalas apropriadas.

Sinais gerados:
    c(t) = Ac * cos(2*pi*fc*t)   -> portadora nao modulada
    m(t) = Am * cos(2*pi*fm*t)   -> sinal mensagem (mensagem de teste,
                                     um tom puro para simplificar a analise)
"""

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------
# 1. PARAMETROS DA SIMULACAO
# -----------------------------------------------------------------------

# --- Parametros da portadora ---
Ac = 1.0        # Amplitude da portadora [V]
fc = 10e3       # Frequencia da portadora [Hz] (10 kHz)

# --- Parametros da mensagem ---
Am = 1.0        # Amplitude da mensagem [V]
fm = 500.0      # Frequencia da mensagem [Hz] (500 Hz)

# --- Frequencia de amostragem ---
# Escolhida em 200 kHz. Justificativa (ver texto completo ao final do
# script, impresso no console):
#   - O sinal de maior frequencia presente neste topico e a propria
#     portadora, fc = 10 kHz.
#   - Pelo Teorema de Nyquist, fs deve ser >= 2*fc = 20 kHz para que o
#     sinal possa, em tese, ser reconstruido sem aliasing.
#   - fs = 200 kHz fornece um fator de sobre-amostragem de 10x o minimo
#     de Nyquist (200 kHz / 20 kHz), o que equivale a 20 amostras por
#     ciclo de portadora (200 kHz / 10 kHz). Isso da uma folga
#     confortavel: garante curvas suaves nos graficos
#     (sem efeito de "serrilhado"/aliasing visual) e deixa margem para,
#     nos proximos topicos, gerar sinais FM/PM cuja banda ocupada (pela
#     Regra de Carson) e maior que a da portadora pura sem modulacao.
fs = 200e3      # Frequencia de amostragem [Hz]
Ts = 1 / fs     # Periodo de amostragem [s]

# --- Vetor de tempo ---
# Duracao minima exigida: pelo menos 10 periodos completos de fm.
n_periodos_fm = 10
Tm = 1 / fm                     # periodo da mensagem [s]
T_total = n_periodos_fm * Tm    # duracao total do vetor de tempo [s]

# np.arange gera as amostras discretas t = 0, Ts, 2*Ts, ..., ate T_total
t = np.arange(0, T_total, Ts)   # vetor de tempo [s]
N = len(t)                      # numero total de amostras

# -----------------------------------------------------------------------
# 2. GERACAO DOS SINAIS
# -----------------------------------------------------------------------

c_t = Ac * np.cos(2 * np.pi * fc * t)   # portadora nao modulada
m_t = Am * np.cos(2 * np.pi * fm * t)   # sinal mensagem

# -----------------------------------------------------------------------
# 3. ANALISE DOS PARAMETROS (impressa no console)
# -----------------------------------------------------------------------

Tc = 1 / fc                          # periodo da portadora [s]
amostras_por_ciclo_portadora = fs / fc
fator_sobreamostragem = fs / (2 * fc)  # em relacao ao minimo de Nyquist

print("=" * 65)
print("ANALISE DOS PARAMETROS DA SIMULACAO")
print("=" * 65)
print(f"Portadora  c(t): Ac = {Ac} V | fc = {fc/1e3:.1f} kHz | "
      f"Tc = {Tc*1e6:.2f} us")
print(f"Mensagem   m(t): Am = {Am} V | fm = {fm:.1f} Hz  | "
      f"Tm = {Tm*1e3:.2f} ms")
print(f"Frequencia de amostragem fs = {fs/1e3:.0f} kHz "
      f"(Ts = {Ts*1e6:.3f} us)")
print(f"Duracao total do vetor de tempo: {T_total*1e3:.1f} ms "
      f"({n_periodos_fm} periodos de fm)")
print(f"Numero total de amostras: N = {N}")
print("-" * 65)
print("CRITERIO DE NYQUIST (para o sinal de maior frequencia = fc):")
print(f"  fs_minimo (Nyquist) = 2 * fc = {2*fc/1e3:.0f} kHz")
print(f"  fs escolhida        = {fs/1e3:.0f} kHz")
print(f"  Fator de sobre-amostragem em relacao ao minimo de Nyquist: "
      f"{fator_sobreamostragem:.1f}x")
print(f"  Amostras por ciclo da portadora: {amostras_por_ciclo_portadora:.0f}")
print("  --> fs = 200 kHz respeita Nyquist com folga confortavel.")
print("=" * 65)

# -----------------------------------------------------------------------
# 4. VISUALIZACAO
# -----------------------------------------------------------------------
# Como fc (10 kHz) e fm (500 Hz) tem escalas de tempo muito diferentes
# (a portadora oscila 20x mais rapido que a mensagem), usamos DUAS
# janelas de tempo distintas:
#   - Janela CURTA: para enxergar os ciclos da portadora com clareza.
#   - Janela LONGA (o vetor de tempo completo): para enxergar os 10
#     periodos completos da mensagem.

# Janela curta: mostrar ~6 ciclos da portadora (6 * Tc)
t_curta_max = 6 * Tc
mask_curta = t <= t_curta_max

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))

# --- Subplot 1: janela curta (foco na portadora) ---
ax1.plot(t[mask_curta] * 1e6, c_t[mask_curta],
         color="#378ADD", linewidth=1.6, label="c(t) = Ac·cos(2π·fc·t)")
ax1.plot(t[mask_curta] * 1e6, m_t[mask_curta],
         color="#D85A30", linewidth=1.6, linestyle="--",
         label="m(t) = Am·cos(2π·fm·t)")
ax1.set_title("Janela curta (foco nos ciclos da portadora)")
ax1.set_xlabel("Tempo [µs]")
ax1.set_ylabel("Amplitude [V]")
ax1.legend(loc="upper right")
ax1.grid(True, alpha=0.3)

# --- Subplot 2: janela longa (foco na mensagem, vetor de tempo completo) ---
ax2.plot(t * 1e3, m_t, color="#D85A30", linewidth=1.8,
         label="m(t) = Am·cos(2π·fm·t)")
ax2.plot(t * 1e3, c_t, color="#378ADD", linewidth=0.4, alpha=0.5,
         label="c(t) (mostrada apenas para contraste de escala)")
ax2.set_title(f"Janela longa ({n_periodos_fm} periodos completos de fm)")
ax2.set_xlabel("Tempo [ms]")
ax2.set_ylabel("Amplitude [V]")
ax2.legend(loc="upper right")
ax2.grid(True, alpha=0.3)

fig.suptitle("Topico 1 - Sinais base: portadora c(t) e mensagem m(t)",
             fontsize=13)
fig.tight_layout()
fig.savefig("topico1_sinais_base.png", dpi=150)
print("\nGrafico salvo em: topico1_sinais_base.png")

# -----------------------------------------------------------------------
# 5. "ALTERAR E OBSERVAR" - exemplo de variacao de parametros
# -----------------------------------------------------------------------
# Para cumprir o pedido de "alterar e observar as mudancas", geramos uma
# segunda versao com fm dobrada (1 kHz em vez de 500 Hz) e fc reduzida
# pela metade (5 kHz em vez de 10 kHz), mantendo fs = 200 kHz.
# Isso reduz a razao fc/fm de 20 para apenas 5, aproximando as duas
# escalas de tempo -- util para observar como a relacao fc/fm afeta a
# "separacao" visual entre portadora e mensagem.

fc2, fm2 = 5e3, 1e3
Tc2, Tm2 = 1 / fc2, 1 / fm2
T_total2 = n_periodos_fm * Tm2
t2 = np.arange(0, T_total2, Ts)
c2_t = Ac * np.cos(2 * np.pi * fc2 * t2)
m2_t = Am * np.cos(2 * np.pi * fm2 * t2)

fig2, ax3 = plt.subplots(figsize=(10, 3.5))
mask_curta2 = t2 <= 6 * Tc2
ax3.plot(t2[mask_curta2] * 1e6, c2_t[mask_curta2],
         color="#378ADD", linewidth=1.6, label="c(t): fc = 5 kHz")
ax3.plot(t2[mask_curta2] * 1e6, m2_t[mask_curta2],
         color="#D85A30", linewidth=1.6, linestyle="--",
         label="m(t): fm = 1 kHz")
ax3.set_title("Variacao dos parametros: fc/fm cai de 20 para 5 "
              "(sinais ficam menos 'separados' em escala de tempo)")
ax3.set_xlabel("Tempo [µs]")
ax3.set_ylabel("Amplitude [V]")
ax3.legend(loc="upper right")
ax3.grid(True, alpha=0.3)
fig2.tight_layout()
fig2.savefig("topico1_variacao_parametros.png", dpi=150)
print("Grafico da variacao salvo em: topico1_variacao_parametros.png")

# plt.show()  # descomente para abrir os graficos interativamente
