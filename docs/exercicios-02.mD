### Constantes e Fórmulas de Apoio

Para todos os cálculos, utilizaremos as seguintes constantes físicas e fórmulas extraídas do material:

- **Permissividade do vácuo ($\epsilon_0$):** $\approx 8,854 \times 10^{-12} \text{ F/m}$
- **Permeabilidade do vácuo ($\mu_0$):** $4\pi \times 10^{-7} \text{ H/m}$

---

#### Fórmulas de Propagação

- **Fator de Atenuação ($\alpha$):**
  $$\alpha = \omega\sqrt{\frac{\mu\epsilon}{2} \left[ \sqrt{1 + \left( \frac{\sigma}{\omega\epsilon} \right)^2} - 1 \right]}$$

- **Fator de Fase ($\beta$):**
  $$\beta = \omega\sqrt{\frac{\mu\epsilon}{2} \left[ \sqrt{1 + \left( \frac{\sigma}{\omega\epsilon} \right)^2} + 1 \right]}$$

- **Impedância Intrínseca ($\eta$):**
  $$\eta = \sqrt{\frac{i\omega\mu}{\sigma + i\omega\epsilon}}$$

- **Velocidade de Fase ($v_p$):**
  $$v_p = \frac{\omega}{\beta}$$

- **Velocidade de Grupo ($v_g$):**
  $$v_g = \left\{ \text{Im} \left[ \frac{-2\omega\mu\epsilon + i\mu\sigma}{2\gamma} \right] \right\}^{-1}$$

---

### Resolução dos Exercícios

#### EXERCÍCIO 01

**Dados:**
- $f = 12\text{ MHz}$
- $\sigma = 0,002\text{ S/m}$
- $\epsilon = 3\epsilon_0$
- $\mu = \mu_0$

**Resolução:**

1.  **Frequência angular ($\omega$):**
    $\omega = 2\pi \cdot 12 \times 10^6 \approx 7,54 \times 10^7\text{ rad/s}$

2.  **Tangente de perdas ($\frac{\sigma}{\omega\epsilon}$):**
    $\tan\delta = \frac{0,002}{7,54 \times 10^7 \cdot 3 \cdot 8,854 \times 10^{-12}} \approx 0,9985$

3.  **Cálculo de $\alpha$:**
    - $\text{Termo interno} = \sqrt{1 + 0,9985^2} - 1 \approx 0,413$
    - $\alpha = 7,54 \times 10^7 \sqrt{\frac{\mu_0 \cdot 3\epsilon_0}{2} \cdot 0,413} \approx \mathbf{0,198\text{ Np/m}}$

4.  **Cálculo de $\beta$:**
    - $\text{Termo interno} = \sqrt{1 + 0,9985^2} + 1 \approx 2,413$
    - $\beta = 7,54 \times 10^7 \sqrt{\frac{\mu_0 \cdot 3\epsilon_0}{2} \cdot 2,413} \approx \mathbf{0,478\text{ rad/m}}$

---

#### EXERCÍCIO 02

**Dados:**
- $f = 5\text{ MHz}$
- $\sigma = 2 \times 10^{-3}\text{ S/m}$
- $\epsilon = 2\epsilon_0$
- $\mu = \mu_0$
- $E_{z=0} = 200\text{ mV}$

**Resolução:**

1.  **Frequência angular ($\omega$):**
    $\omega \approx 3,14 \times 10^7\text{ rad/s}$

2.  **Tangente de perdas ($\frac{\sigma}{\omega\epsilon}$):**
    $\tan\delta \approx 3,595$

3.  **Cálculo de $\alpha$ e $\beta$:**
    - $\alpha = 3,14 \times 10^7 \sqrt{1,11 \times 10^{-17} \cdot (\sqrt{1+3,595^2}-1)} \approx \mathbf{0,173\text{ Np/m}}$
    - $\beta = 3,14 \times 10^7 \sqrt{1,11 \times 10^{-17} \cdot (\sqrt{1+3,595^2}+1)} \approx \mathbf{0,228\text{ rad/m}}$

4.  **Campo Instantâneo:**
    $e(z,t) = 200 e^{-0,173z} \cos(3,14 \times 10^7 t - 0,228z) \text{ [mV/m]}$

5.  **Distância para metade da amplitude:**
    $e^{-\alpha z} = 0,5 \rightarrow z = \frac{\ln(2)}{0,173} \approx \mathbf{4,01\text{ m}}$

---

#### EXERCÍCIO 03

**Enunciado:** $\omega = 5 \cdot 10^7\text{ rad/s}$, $\mu = \mu_0$, $\epsilon = 20\epsilon_0$ e $\sigma = 12\text{ mS/m}$. Determine o fator de propagação ($\gamma$), impedância ($\eta$), velocidade de fase ($v_p$) e velocidade de grupo ($v_g$).

**Resolução:**

**Passo 1: Fator de Propagação ($\gamma = \alpha + i\beta$)**
- **Tangente de perdas:** $\frac{\sigma}{\omega\epsilon} = \frac{0,012}{5 \cdot 10^7 \cdot 20 \cdot 8,854 \cdot 10^{-12}} \approx 1,3553$
- **Cálculo de $\alpha$:** $\alpha = 5 \cdot 10^7 \sqrt{\frac{\mu_0 \cdot 20\epsilon_0}{2} (\sqrt{1+1,3553^2}-1)} \approx \mathbf{0,4363\text{ Np/m}}$
- **Cálculo de $\beta$:** $\beta = 5 \cdot 10^7 \sqrt{\frac{\mu_0 \cdot 20\epsilon_0}{2} (\sqrt{1+1,3553^2}+1)} \approx \mathbf{0,8641\text{ rad/m}}$
- **Resultado:** $\gamma = \mathbf{0,4363 + i0,8641\text{ m}^{-1}}$

**Passo 2: Velocidade de Fase ($v_p$)**
- $v_p = \frac{\omega}{\beta} = \frac{5 \cdot 10^7}{0,8641} \approx \mathbf{5,786 \times 10^7\text{ m/s}}$

**Passo 3: Impedância Intrínseca ($\eta$)**
- $\eta = \sqrt{\frac{i\omega\mu}{\sigma + i\omega\epsilon}} = \sqrt{\frac{i(5 \cdot 10^7)(4\pi \cdot 10^{-7})}{0,012 + i(5 \cdot 10^7)(20 \cdot 8,854 \cdot 10^{-12})}}$
- $\eta \approx \mathbf{64,91 \angle 26,79^\circ\ \Omega}$

**Passo 4: Velocidade de Grupo ($v_g$)**
- **Numerador ($N$):** $-2\omega\mu\epsilon + i\mu\sigma$
  - $\text{Parte Real} = -2(5 \cdot 10^7)(20 \cdot \mu_0 \cdot \epsilon_0) \approx -2,2253 \times 10^{-8}$
  - $\text{Parte Imag} = i(\mu_0)(0,012) \approx i1,508 \times 10^{-8}$
- **Denominador ($D$):** $2\gamma = 0,8726 + i1,7282$
- **Cálculo da parte imaginária de $N/D$:**
  $\text{Im} \left[ \frac{N}{D} \right] = \frac{\text{Im}(N) \cdot \text{Re}(D) - \text{Re}(N) \cdot \text{Im}(D)}{|D|^2} \approx 1,377 \times 10^{-8}$
- **Resultado:** $v_g = (1,377 \times 10^{-8})^{-1} \approx \mathbf{7,26 \times 10^7\text{ m/s}}$

---

#### EXERCÍCIO 04

**Dados:**
- $\omega = 10^8\text{ rad/s}$
- $\sigma = 2 \times 10^{-3}\text{ S/m}$
- $\epsilon = 3\epsilon_0$
- $\vec{E} = (10\hat{x} + i20\hat{y})e^{-\gamma z}$

**Resolução:**

1.  **Cálculo de $\alpha$ e $\beta$:**
    - $\frac{\sigma}{\omega\epsilon} \approx 0,753$
    - $\alpha = 10^8 \sqrt{1,67 \times 10^{-17} \cdot 0,252} \approx \mathbf{0,205\text{ Np/m}}$
    - $\beta = 10^8 \sqrt{1,67 \times 10^{-17} \cdot 2,252} \approx \mathbf{0,613\text{ rad/m}}$

2.  **Impedância Intrínseca ($\eta$):**
    $\eta = \sqrt{\frac{i\omega\mu}{\sigma + i\omega\epsilon}} \approx \mathbf{194,4 \angle 18,5^\circ\ \Omega}$

3.  **Fasor $\vec{H}$:**
    $\vec{H} = \frac{1}{\eta} \hat{a}_z \times \vec{E} = \mathbf{(0,103 \angle -108,5^\circ \hat{x} + 0,051 \angle -18,5^\circ \hat{y}) e^{-\gamma z}\ [A/m]}$

---

#### EXERCÍCIO 05

**Enunciado:** $f = 18\text{ MHz}$, $\sigma = 4 \cdot 10^{-3}\text{ S/m}$ e $\epsilon = 4\epsilon_0$ em meio não ferromagnético ($\mu = \mu_0$). Determine $v_p$, $v_g$ e velocidade de deslocamento de energia.

**Resolução:**

**Passo 1: Parâmetros iniciais**
- **Frequência angular:** $\omega = 2\pi \cdot 18 \cdot 10^6 \approx 1,131 \times 10^8\text{ rad/s}$
- **Tangente de perdas:** $\frac{\sigma}{\omega\epsilon} = \frac{0,004}{1,131 \cdot 10^8 \cdot 4 \cdot 8,854 \cdot 10^{-12}} \approx 0,9985$

**Passo 2: Velocidade de Fase ($v_p$)**
- **$\beta$:** $1,131 \times 10^8 \sqrt{\frac{\mu_0 \cdot 4\epsilon_0}{2} (\sqrt{1+0,9985^2}+1)} \approx \mathbf{0,8286\text{ rad/m}}$
- $v_p = \frac{\omega}{\beta} = \frac{1,131 \cdot 10^8}{0,8286} \approx \mathbf{1,365 \times 10^8\text{ m/s}}$

**Passo 3: Velocidade de Grupo ($v_g$)**
- **Numerador ($N$):** $-2\omega\mu\epsilon + i\mu\sigma$
  - $\text{Parte Real} \approx -1,0067 \times 10^{-8}$
  - $\text{Parte Imag} \approx i5,0265 \times 10^{-9}$
- **Denominador ($D$):** $2\gamma$ (onde $\alpha \approx 0,3432$) $\rightarrow D = 0,6864 + i1,6572$
- **Cálculo da parte imaginária de $N/D$:**
  $\text{Im} \left[ \frac{N}{D} \right] \approx 6,258 \times 10^{-9}$
- **Resultado:** $v_g \approx \mathbf{1,598 \times 10^8\text{ m/s}}$

> **Nota:** Em meios isotrópicos e lineares, a **velocidade de deslocamento de energia** é numericamente igual à **velocidade de grupo** ($v_g \approx 1,598 \times 10^8\text{ m/s}$).
