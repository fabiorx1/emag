## Exercício 1

Provar os argumentos abaixo, utilizando a técnica da redução ao absurdo:

- **(a)** $a \rightarrow b,\ c \vee \sim b,\ \sim(a \wedge c)\ \therefore \sim a$
- **(b)** $a \rightarrow \sim b,\ e \rightarrow \sim a,\ b \vee e\ \therefore \sim a$
- **(c)** $b \rightarrow c \leftrightarrow \sim d,\ \sim d \rightarrow b,\ \sim c \rightarrow \sim d\ \therefore c$
- **(d)** $a \rightarrow e \vee f,\ e \rightarrow \sim a,\ c \rightarrow \sim f\ \therefore \sim(a \wedge c)$

### **(a) Prova do Argumento**

**Premissas:**

1. $a \rightarrow b$
2. $c \vee \sim b$
3. $\sim(a \wedge c)$

**Conclusão:** $\sim a$

**Demonstração por absurdo:**

1. **Suposição:** Assumimos a negação da conclusão. Portanto, assumimos que **$a$ é verdadeiro**.
2. De (1) e da Premissa 1 ($a \rightarrow b$), aplicando _Modus Ponens_, deduzimos que **$b$ é verdadeiro**.
3. Da Premissa 2 temos $c \vee \sim b$. Como sabemos pelo passo (2) que $b$ é verdadeiro, $\sim b$ obrigatoriamente é falso. Aplicando o _Silogismo Disjuntivo_, a única opção restante é que **$c$ seja verdadeiro**.
4. Juntando os passos (1) e (3), concluímos que a conjunção **$a \wedge c$** é verdadeira.
5. **O Absurdo:** O passo (4) contradiz diretamente a Premissa 3 ($\sim(a \wedge c)$). Chegamos a uma contradição.
6. **Conclusão:** Como a suposição de $a$ levou a uma falha lógica, $a$ deve ser falso. Logo, o argumento **$\sim a$** é válido.

---

### **(b) Prova do Argumento**

**Premissas:**

1. $a \rightarrow \sim b$
2. $e \rightarrow \sim a$
3. $b \vee e$

**Conclusão:** $\sim a$

**Demonstração por absurdo:**

1. **Suposição:** Assumimos a negação da conclusão. Logo, assumimos que **$a$ é verdadeiro**.
2. De (1) e da Premissa 1 ($a \rightarrow \sim b$), por _Modus Ponens_, deduzimos **$\sim b$** (ou seja, $b$ é falso).
3. Da Premissa 3 temos $b \vee e$. Como vimos em (2) que $b$ é falso, pelo _Silogismo Disjuntivo_, deduzimos que **$e$ é verdadeiro**.
4. Do passo (3) e da Premissa 2 ($e \rightarrow \sim a$), por _Modus Ponens_, deduzimos **$\sim a$**.
5. **O Absurdo:** Chegamos a uma contradição direta. No passo (1) assumimos $a$, mas no passo (4) deduzimos logicamente $\sim a$. Uma proposição não pode ser verdadeira e falsa simultaneamente ($a \wedge \sim a$).
6. **Conclusão:** A suposição de que $a$ é verdadeiro é impossível. Logo, o argumento **$\sim a$** é válido.

---

### **(c) Prova do Argumento**

**Premissas:**

1. $b \rightarrow c \leftrightarrow \sim d$ _(Em lógica, geralmente interpretado pelas regras de precedência como $(b \rightarrow c) \leftrightarrow \sim d$)_
2. $\sim d \rightarrow b$
3. $\sim c \rightarrow \sim d$

**Conclusão:** $c$

**Demonstração por absurdo:**

1. **Suposição:** Assumimos a negação da conclusão. Logo, assumimos que **$\sim c$ é verdadeiro**.
2. Do passo (1) e da Premissa 3 ($\sim c \rightarrow \sim d$), por _Modus Ponens_, deduzimos que **$\sim d$ é verdadeiro**.
3. Do passo (2) e da Premissa 2 ($\sim d \rightarrow b$), por _Modus Ponens_, deduzimos que **$b$ é verdadeiro**.
4. Agora analisamos a Premissa 1 ($(b \rightarrow c) \leftrightarrow \sim d$):
   - Como deduzimos no passo (2) que $\sim d$ é verdadeiro, a implicação do outro lado da equivalência, $(b \rightarrow c)$, também precisa ser verdadeira.
   - Sabemos pelo passo (3) que $b$ é verdadeiro. Para que a implicação $(b \rightarrow c)$ resulte em verdade, obrigatoriamente **$c$ precisa ser verdadeiro**.
5. **O Absurdo:** No passo (4) fomos forçados a deduzir $c$, o que contradiz frontalmente nossa suposição inicial no passo (1) de que $\sim c$ era verdadeiro.
6. **Conclusão:** A suposição de $\sim c$ derruba o sistema. Logo, o argumento **$c$** é válido.

---

### **(d) Prova do Argumento**

**Premissas:**

1. $a \rightarrow e \vee f$
2. $e \rightarrow \sim a$
3. $c \rightarrow \sim f$

**Conclusão:** $\sim(a \wedge c)$

**Demonstração por absurdo:**

1. **Suposição:** Assumimos a negação da conclusão. Ou seja, tiramos a negação externa e assumimos que a conjunção **$a \wedge c$ é verdadeira**.
2. Pela regra da _Simplificação_ sobre (1), podemos separar as verdades: tanto **$a$** quanto **$c$** são individualmente verdadeiros.
3. Usando $a$ e a Premissa 1 ($a \rightarrow e \vee f$), por _Modus Ponens_, deduzimos que a disjunção **$e \vee f$ é verdadeira**.
4. Usando $c$ e a Premissa 3 ($c \rightarrow \sim f$), por _Modus Ponens_, deduzimos **$\sim f$** (ou seja, $f$ é falso).
5. Juntando os passos (3) e (4): temos $e \vee f$, mas sabemos que $f$ falhou. Pelo _Silogismo Disjuntivo_, a única forma de a disjunção ser verdadeira é se **$e$ for verdadeiro**.
6. Usando $e$ e a Premissa 2 ($e \rightarrow \sim a$), por _Modus Ponens_, deduzimos **$\sim a$**.
7. **O Absurdo:** Mais uma vez, o colapso. No passo (2) garantimos que $a$ é verdadeiro, mas no passo (6) o próprio sistema nos fez deduzir $\sim a$. Temos a contradição fatal ($a \wedge \sim a$).
8. **Conclusão:** A suposição inicial de que $a \wedge c$ pudesse ser verdadeira gera uma inconsistência. Portanto, a negação disso, **$\sim(a \wedge c)$**, é a conclusão logicamente válida.
