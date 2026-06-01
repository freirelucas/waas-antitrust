# Crítica x10 — síntese do recrutamento especialista

Recrutei 8 especialistas em paralelo (2 matemáticos, 2 economistas, 2 advogados,
1 designer, 1 product manager) para revisão crítica do projeto. Esta página
consolida as convergências e divergências, e remete ao [Plano de
melhorias](plano_melhorias.md) para execução.

Cada especialista entregou: diagnóstico de ~400 palavras + 3–5 melhorias
concretas com arquivo-alvo e estimativa S/M/L. As críticas integrais estão
arquivadas no histórico da sessão; aqui ficam os achados sintéticos.

---

## Convergências principais

Pontos em que **dois ou mais especialistas** chegaram à mesma conclusão
independentemente. Esses são os achados mais robustos.

### A. `fatia_mercado` é variável fantasma (Eco A, Eco B, PM)
A `EmpresaAgent.fatia_mercado` é atribuída como `1/n_empresas` (homogênea) e
nunca lida em parte alguma do pacote (`grep` confirma zero leitores).
`sancao_esperada` usa só `0,05·R·(1+σ)`; `bem_estar` é `−(dano + β·FP + γ·custo)`.
**Uma violação de firma de 40% conta igual a uma de 2%.** Para um projeto que
invoca abuso de posição dominante, é vício estrutural.

### B. Headline-metrics de uma seed não sustentam comparação (Mat A, Mat B)
O teste `test_dissuasao_endogena_reduz_violadoras_no_regime_b` usa **uma seed
única** com comparação pontual de médias. A variância do estimador
`vp/n_violadoras` é alta; com bootstrap multi-seed, o ranking dano(A) > dano(B)
pode cruzar zero em algumas seeds. **Nada do que está em `Resultados` é
robusto a re-amostragem.**

### C. Risco jurídico do Art. 12 vira seção, não TODO (Adv A, Adv B)
Os dois advogados convergem em três frentes:
1. **Quem é "vítima" no Art. 12?** Vítima na práxis CADE é categoria coletiva
   (consumidor/concorrente/erário). O denunciante interno pode ser **partícipe**
   da conduta (eng, comercial, growth), o que colide com Art. 86.
2. **Descompasso de competência (Adv B, fundacional)**: Resolução do CADE é
   infralegal — não pode criar cláusula contratual padrão de vesting nem
   proteção trabalhista (reserva de lei Art. 22 CF). **O Regime B não tem
   instrumento jurídico para impor a cláusula que `hirschman.py` modela.**
3. **F6/D01 subtratado no paper**: `main.tex` tem TODO de rodapé; merecia
   seção própria de 3–5 páginas.

### D. Sinalização visual de status faltando (Designer, Adv A)
Duas críticas independentes pedem **chips/marcadores visuais** distinguindo:
- **Figuras**: conceitual (Fig 1 inversão, Fig 2 fase) vs. saída real (Fig 3).
- **Texto**: alerta jurídico em afirmações fortes (e.g., "é, assim,
  re-caracterizada" em `main.tex:100`).

O risco é simétrico: jornalista cita figura conceitual como resultado simulado;
jurista cita tese como pacífica quando é controvertida.

### E. `custo_exodo_acum` exposto mas órfão (Eco B + meu próprio gap)
R07 adicionou o reporter mas ele NÃO entra em `calcular_bem_estar`. R05 foi
fechado prematuramente — há um termo de bem-estar pendente, com peso provisional.

---

## Críticas únicas (não-convergentes, mas relevantes)

### Mat A — dinâmica de p_percebida
- Mapa `p ← (1−λ)p + λ·(vp/n_viol)` é descontínuo no laço de realimentação;
  **suspeita de histerese** (não verificada numericamente).
- Estimador `vp/n_viol` é razão com denominador pequeno: variância explosiva
  e singularidade em `n_viol=0`. Hoje o guard congela `p_perc` — produz ponto
  fixo neutro artificial. **Beta-Binomial MAP** (prior `Beta(α, β)` com
  pseudo-contagens) é drop-in trivial que resolve.
- `peso_hirschman` em `g_i_efetivo` é **feedback gain**, não atrito linear
  — pode atravessar bifurcação Hopf/saddle-node. Vale traçar diagrama de
  bifurcação em `(λ, peso_hirschman)`.

### Mat B — jogo global × ABM
- **Dois modelos de coordenação coexistem sem conversar**: `jogo_global.py`
  deriva `x*` analiticamente; `agents.py::decidir_sinal` usa heurísticas
  com `0.30` hardcoded. Solução: substituir o arquétipo "racional" por
  `s_i ≥ x*` derivado do `limiar_switching`.
- **Contraste multiplicidade × unicidade está ausente**: a Prop. 2 perde o pé
  teórico de Morris-Shin (1998) sem demonstrar a multiplicidade sob
  informação completa.
- Heterogeneidade de arquétipos pode quebrar a unicidade do equilíbrio — não
  há resultado fechado conhecido para o mix do ABM.

### Eco A — endogeneizar incentivo
- `g_i` é **sorteio uniforme estático** em `_criar_empresas`. Becker exige
  `g(t) = π·R / (p·S)` — função do estado, não constante.
- **Falta o termo Becker `p·(S−D)` na IC-F\***: a `satisfaz_ic_f_estrela` é
  literalmente `D > W`. O branch "não paga" é dominado por suposição
  estrutural — vicia qualquer alegação sobre economizar contribuição
  pecuniária.
- **Hirschman como subtração linear de `g_i` é ad hoc**: economicamente,
  cláusula de vesting acelerado é equivalente a *pagamento condicional*
  — deveria entrar como **elevação de `W_esperado`**, não como redução
  de `ganho/sanção`.
- Falta NPV do crime (taxa de desconto temporal `r` e horizonte `T`).

### Eco B — bem-estar substantivo
- **Sem proxy de excedente do consumidor**. WaaS é política de mercado
  digital, mas o bem-estar não modela perda do consumidor (sobrepreço ×
  quantidade afetada). Mínimo: `Σ (σ · share · R)`.
- **Sem `multa_arrecadada`**: VP via P4 não gera receita do Estado no caixa
  do bem-estar. Há ganho líquido para o erário simplesmente descartado.
- **Pesos β, γ frágeis**: literatura Connor-Lande (overcharge mediano
  15–25%), Polinsky-Shavell (custo FP ≈ 1–2× sanção) dariam âncora.
- **Fatia uniforme é "non sequitur"** para projeto que invoca posição
  dominante. Lognormal/Pareto seria realista.

### Adv A — Art. 12 / "vítima"
- **Empregado-denunciante NÃO é "vítima"** no sentido coletivo do Art. 45,
  V/VI da Lei 12.529. É testemunha qualificada — ou partícipe (R08).
- **Conflito com leniência clássica (Art. 86)**: WaaS pode tornar leniência
  redundante para empresas que prefiram pagar diretamente os empregados,
  criando arbitragem regulatória.
- **`p_anulacao_tcc` como parâmetro de simulação**: transforma F6 de rótulo
  em falsificador de fato — Regime B com `p_anulacao > 0` colapsa em A.
- E04 (verbatim do Art. 12) segue aberto — a charneira do Regime B é citada
  de memória.

### Adv B — CLT / vesting / sigilo
- **Vesting acelerado por gatilho de ação coletiva NÃO EXISTE em templates
  YC/NVCA padrão** — eles cobrem só *change of control*. O docstring de
  `hirschman.py` invocando "padrões YC" é overclaim. (Vício que eu próprio
  introduzi; corrijo na execução.)
- **Lei 13.608/2018 não cobre antitruste no eixo recompensa** — Art. 4º-C,
  §3º restringe a "crimes contra administração pública". Extensão
  analógica anti-represália é hipótese, não jurisprudência consolidada.
- **Tributação (IRPF + INSS) derrete 40–50% do `valor_vesting_acelerado`**.
  O modelo opera em bruto, superestimando o exit-threat.
- **Forum selection americano inoponível ao trabalhador brasileiro** (Art.
  651 CLT, OJ 287 SDI-1).

### Designer — UX visual + acessibilidade
- **`cmap="RdYlGn"`** em `inversao.py` e `fase.py` é pior caso para
  daltonismo vermelho-verde — e o significado semântico depende exatamente
  desse eixo. Trocar por `cividis`/`viridis` + isoclinas rotuladas.
- **Figura 3 subaproveitada**: linhas finas, painel B esmagado pela escala
  de A, sem rótulos "A"/"B" nos cantos, sem anotações numéricas (e.g.,
  "20→0 em 2 tiques", "ΔW = +98%").
- **Hierarquia tipográfica**: H1 = `waas-antitrust` desperdiça a dobra com
  nome de pacote. Deveria ser pergunta-tese; pacote vira subtítulo.
- **Personas hoje são admonition de texto corrido**: vira `grid cards` do
  Material.

### PM — catálogo BR + atores
- **Lacunas materialmente brasileiras**: faltam (a) exclusividade/retaliação
  em marketplace de duas pontas (iFood TCC 2023 + indícios de
  descumprimento 2025); (b) anti-steering/IAP (Apple Brasil, dez/2025); (c)
  abuso exploratório por extração de dado (Google × conteúdo jornalístico
  para IA, 2026). O catálogo é exclusionista; o CADE pós-2023 está virando
  para exploratório.
- **Atores primários subdimensionam growth/comercial**: `self_preferencing`
  passa por marketing pago e gestão de seller, não só eng+produto.
- **`PAPEIS_PADRAO` falta `operacoes` e `financeiro`**: marketplaces BR
  (iFood, Mercado Livre) são operations-heavy; predatory_pricing tem como
  ator primário FP&A.
- **Distribuição BR ≠ big tech madura**: precisaria de presets
  `BIGTECH_MADURA` (atual) vs. `MARKETPLACE_BR`.
- **Observabilidade binária (1.0 / 0.2) deveria ser gradiente 3 níveis**
  (primário=1.0, adjacente=0.5, distal=0.1) — referência Near & Miceli
  sobre whistleblowing organizacional.

---

## Sinal mais forte da sessão

O **descompasso de competência** apontado por Adv B (§3) é o ponto que mais
muda a leitura do projeto: o Regime B não pode entregar o que promete, e o
modelo silencia sobre essa restrição. Combinado com a observação de Adv A
sobre "vítima" no Art. 12, **o paper precisa de uma seção própria de risco
jurídico que recoloca o Regime C como caminho institucionalmente sólido e o
Regime B como conjectura otimista**.

Ver o [Plano de melhorias](plano_melhorias.md) para a ordem de execução.
