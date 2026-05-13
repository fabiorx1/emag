# ELETROMAGNETISMO

**Professor:** Danilo H. Spadoti 
**Data:** 04/2026 

---

## CAPÍTULO 2: ONDAS ELETROMAGNÉTICAS 

### 2.1) EQUAÇÃO DE ONDA 

### 2.2) SOLUÇÃO DA EQUAÇÃO DE ONDA 

### 2.3) INTERPRETAÇÃO DA SOLUÇÃO 

### 2.4) ESTUDO DO FATOR DE PROPAGAÇÃO ($\gamma$) 

### 2.5) ONDA ELETROMAGNÉTICA TRANSVERSAL (TEM) 

### 2.6) FRENTE DE ONDA 

---

### 2.7) IMPEDÂNCIA DE ONDAS 

Considerando as relações anteriormente estabelecidas:

- $\vec{\gamma} \times \vec{E} = i\omega\mu\vec{H}$ 
- $\vec{\gamma} = \gamma \hat{\gamma}$ , onde $\hat{\gamma}$ é o vetor unitário na direção de $\vec{\gamma}$.

Podemos expressar o campo magnético como:
$$\vec{H} = \frac{\gamma \hat{\gamma} \times \vec{E}}{i\omega\mu} = \frac{\hat{\gamma} \times \vec{E}}{(\frac{i\omega\mu}{\gamma})}$$

A grandeza $(\frac{i\omega\mu}{\gamma})$, representada por $Z_\omega$ ou $\eta$ ("heta"), possui dimensão de impedância e é denominada **impedância de onda**.

$$\eta = \frac{i\omega\mu}{\gamma} \, [\Omega]$$ 

Sendo o fator de propagação definido por:
$$\gamma = \sqrt{i\omega\mu(\sigma + i\omega\epsilon)} = \alpha + i\beta$$

Substituindo $\gamma$, obtém-se a impedância para um meio ilimitado:
$$\eta = \sqrt{\frac{i\omega\mu}{\sigma + i\omega\epsilon}} \, [\Omega]$$

No meio ilimitado, $\eta$ depende das características eletromagnéticas do meio e da frequência, sendo por isso chamado de **impedância intrínseca da onda**.

Portanto:
$$\vec{H} = \frac{\hat{\gamma} \times \vec{E}}{\eta}$$ 

Se considerarmos a propagação no eixo $z$ ($r_p = z \rightarrow \hat{\gamma} = \hat{z}$)  e os campos definidos como:

- $\vec{E} = (\vec{E}_x \hat{x} + \vec{E}_y \hat{y})e^{-\gamma z}$
- $\vec{H} = (\vec{H}_x \hat{x} + \vec{H}_y \hat{y})e^{-\gamma z}$

Temos:
$$\vec{H} = \frac{\hat{z} \times (\vec{E}_x \hat{x} + \vec{E}_y \hat{y})}{\eta} = \frac{\vec{E}_x \hat{y} - \vec{E}_y \hat{x}}{\eta}$$

Comparando os membros, resultam as relações:

- $H_y = \frac{E_x}{\eta} \rightarrow \eta = \frac{E_x}{H_y}$
- $H_x = \frac{-E_y}{\eta} \rightarrow \eta = \frac{-E_y}{H_x}$

> No caso geral, $\eta$ é uma grandeza complexa: $\eta = |\eta|e^{i\phi_n} = |\eta| \angle \phi_n$. O argumento $\phi_n$ indica que os campos elétrico e magnético estão defasados entre si.

---

#### CASOS PARTICULARES 

**1. Dielétrico Perfeito:** 

- $\eta = \sqrt{\frac{\mu}{\epsilon}}$ (Grandeza real).
- Os campos elétrico e magnético estão rigorosamente em fase em meios sem perdas.
- No **vácuo**: $\eta = \sqrt{\frac{\mu_0}{\epsilon_0}} \approx 377 \, \Omega$ ou $120\pi \, \Omega$.
- Para um dielétrico perfeito não-magnetizável: $\eta = \frac{120\pi}{\sqrt{\epsilon_r}} \, \Omega$.

**2. Dielétrico Real ($\sigma \ll \omega\epsilon$):** 
Usando a aproximação $\sqrt{1+u} \approx 1 + \frac{u}{2}$ para $u \ll 1$:
$$\eta \approx \sqrt{\frac{\mu}{\epsilon}} [1 + i(\frac{\sigma}{2\omega\epsilon})] \, [\Omega]$$ 

**3. Condutor Real ($\sigma \gg \omega\epsilon$):** 
$$\eta = \sqrt{\frac{i\omega\mu}{\sigma}} = \sqrt{\frac{\omega\mu}{\sigma}}\sqrt{i} = \sqrt{\frac{\omega\mu}{2\sigma}} + i\sqrt{\frac{\omega\mu}{2\sigma}} \, [\Omega]$$ 

- O campo elétrico está adiantado em relação ao campo magnético em quase $45^\circ$.
- Em metais, a impedância é muito pequena (milésimos de ohms).
- A parte real é a **resistência superficial** e a imaginária a **reatância superficial**.

| Tipo de Meio        | Ângulo de Defasagem ($\phi_n$)                                            |
| :------------------ | :------------------------------------------------------------------------ |
| Dielétrico Perfeito | $\phi_n = 0^\circ$                                  |
| Dielétrico Real     | $\phi_n = \arctan(\frac{\sigma}{2\omega\epsilon})$  |
| Condutor Real       | $\phi_n = 45^\circ$                                 |

---

### 2.8) VELOCIDADES ENVOLVIDAS NA PROPAGAÇÃO 

#### A) VELOCIDADE DE FASE ($V_p$) 

A frente de onda é definida por $\omega t - \beta r_p = \text{cte}$. A velocidade de fase é a rapidez de deslocamento dessa frente:
$$V_p = \frac{\partial r_p}{\partial t} = \frac{\omega}{\beta} \, [m/s]$$ 

**Casos Particulares:**

1.  **Dielétrico Perfeito:** $V_p = \frac{1}{\sqrt{\mu\epsilon}}$. No vácuo, $V_p = 3 \cdot 10^8 \, m/s$.
2.  **Dielétrico Real:** $V_p \approx \frac{1}{\sqrt{\mu\epsilon}} \{1 - \frac{1}{8}(\frac{\sigma}{\omega\epsilon})^2\}$.
3.  **Condutor Real:** $V_p = \sqrt{\frac{2\omega}{\mu\sigma}}$.

---

#### B) VELOCIDADE DE GRUPO ($V_g$) 

Considere um sinal composto por duas frequências próximas, $\omega$ e $(\omega + \Delta\omega)$. A soma resulta em uma onda cuja amplitude varia no tempo (batimento):
$$\vec{e} = 2E_1 \cos(\frac{\Delta\omega t - \Delta\beta r_p}{2}) \cos(\omega t - \beta r_p)$$ 

A rapidez com que o envelope (amplitude constante) se desloca é a **velocidade de grupo**:
$$V_g = \frac{\Delta\omega}{\Delta\beta}$$ 

No limite $\Delta\omega \rightarrow 0$:
$$V_g = \left\{ \frac{\partial \beta}{\partial \omega} \right\}^{-1} \, [m/s]$$ 

**Casos Particulares:**

1.  **Dielétrico Perfeito:** $V_g = V_p = \frac{1}{\sqrt{\mu\epsilon}}$ (Meio não-dispersivo).
2.  **Dielétrico Real:** $V_g \cdot V_p = \frac{1}{\mu\epsilon}$.
3.  **Condutor Real:** $V_g = 2\sqrt{\frac{2\omega}{\mu\sigma}} = 2V_p$.

---

#### RELAÇÃO DE DISPERSÃO 

A relação geral entre as velocidades é:
$$V_g = \frac{V_p}{1 - (\frac{\omega}{V_p})(\frac{\partial V_p}{\partial \omega})} \, [m/s]$$

- **Meio Não-Dispersivo:** $V_p$ independente de $\omega$, logo $V_g = V_p$.
- **Meio Dispersivo Normal:** $\frac{\partial V_p}{\partial \omega} < 0 \rightarrow V_g < V_p$.
- **Meio Dispersivo Anômalo:** $\frac{\partial V_p}{\partial \omega} > 0 \rightarrow V_g > V_p$.

**Exemplo:** Fibra ótica (onde $\eta_{\text{core}} > \eta_{\text{casca}}$).

---

#### C) VELOCIDADE DE ENERGIA 
