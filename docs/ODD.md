# Protocolo ODD do modelo WaaS

Documentação seguindo Grimm, Railsback, Vincenot et al. (*JASSS* 23(2):7, 2020).

## 1. Visão geral

### 1.1 Propósito e padrões

Quantificar a taxa de denúncia, taxa de verdadeiros positivos, taxa de falsos positivos e bem-estar social gerado pelo mecanismo WaaS sob três regimes institucionais brasileiros.

Padrões-alvo para calibração:

- CADE: 109 acordos de leniência cumulativos em 20 anos.
- CADE: 349 TCCs em 7,5 anos (média 47/ano), conforme Saito 2021.
- Dyck-Morse-Zingales (2010): aproximadamente 19% das fraudes corporativas grandes nos EUA são descobertas por funcionários.

### 1.2 Entidades, variáveis de estado, escalas

Três populações:

1. **Trabalhadores** — arquétipos heterogêneos (Hokamp & Pickhardt 2010): ético (15%), imitativo (35%), racional (40%), aleatório (10%). Estado: arquétipo, w_a, k_pessoal, observou, sinaliza_agora.
2. **Empresas** — parametrizadas por (σ, fatia_mercado, R_receita, eh_violadora).
3. **Autoridade** — capacidade κ e acurácia ρ.

Escalas: 1 tique = 1 trimestre; horizonte = 40 tiques (10 anos). Dimensão "espacial" = rede intra-firma (Watts-Strogatz pequeno-mundo).

### 1.3 Visão geral do processo

Por tique:

- **P1** — cada trabalhador observador amostra `s_i = σ + ε_i` e decide `a_i ∈ {0, 1}`.
- **P2** — agregador conta `Σ_i a_i` na rede intra-firma; dispara se `≥ k`.
- **P3** — empresa decide pagar (β=1) ou não (β=0).
- **P4** — autoridade recebe caso (com restrição de capacidade κ).
- **P5** — coleta de estado.

## 2. Conceitos de desenho

- **Princípios básicos**: PBE; seleção **inspirada em** jogo global (Morris-Shin 1998) e difusão **aproximando** contágio complexo (Centola-Macy 2007). *Nota: o código usa limiares heurísticos (sinal privado ruidoso; imitação por fração de vizinhos no tique anterior), não o equilíbrio do jogo global nem um modelo formal de contágio — ver §3.3 e os submódulos.*
- **Emergência**: taxa macro de denúncia a partir de limiares micro e topologia de rede.
- **Sensoriamento**: trabalhadores observam σ com ruído; plataforma observa Σa exatamente mas só publica gatilho binário.
- **Estocasticidade**: ε_i, arquétipo, detecção, represália.
- **Acoplamento por conhecimento comum**: P(massa crítica) cresce com σ por (i) `q(σ)` crescente e (ii) atualização de crenças de ordem superior.

## 3. Detalhes

### 3.1 Inicialização

- Número de empresas, tamanho médio (calibrado contra 30–50 mil empregados em subsidiárias de big tech no Brasil).
- Fração violadoras: 30%.
- Salário base: R$ 180.000 (Brasscom 2024).
- Rede: Watts-Strogatz com `k = 2% de n_firm`.

### 3.2 Entrada

Não há entrada externa em tempo real. Calibração ex post.

### 3.3 Submodelos

Ver `src/waas_antitrust/agents.py` e `src/waas_antitrust/model.py`.

## Proposições com esboços de prova

### Proposição 1 — Viabilidade IC do caminho "empresa paga"

Sob Regime B, existem parâmetros no interior do espaço factível em que IC-F* (D > W) e IR-W são satisfeitas estritamente.

*Esboço*: a jurisprudência da Res. 21/2018 permite D até 50% da multa esperada; para uma grande empresa de tecnologia com receita R no setor afetado e multa típica em [1%, 20%]·R, D ∈ [0,5%·R, 10%·R]. Pagamentos por trabalhador da ordem de 3·w_a com n ≤ 20 trabalhadores disparados ainda mantêm D > W. IR-W requer W ≥ r·(L_carreira + T·w_a/12); com r = 0,15, T = 8 meses, L = 2·w_a, o limiar é ≈ 0,4·w_a, bem abaixo da recompensa proposta. IC-T satisfeita pelo Art. 340 CP. □

> **Status (v0.1.0):** a desigualdade D > W no ponto-alvo é verificada por teste de regressão (`tests/test_model.py`); as faixas jurídicas do esboço (multa, D ≤ 50%) são ilustrativas, não calibradas.

### Proposição 2 — Unicidade do equilíbrio de coordenação

No limite τ → 0 do subjogo de jogo global, há equilíbrio único de switching `s*` para cada (k, W, r) na região relevante.

*Esboço*: aplicação direta do Teorema 1 de Morris-Shin (1998) ao jogo binário com complementaridades estratégicas. □

> **Status (v0.1.0):** conjectura. O modelo computacional **não** resolve o jogo global nem varre τ → 0 (τ é fixo); a unicidade não é verificada no código.

### Proposição 3 — Dominância de bem-estar do Regime B sobre o Regime A

Para um conjunto de medida positiva de (W, D, σ), o bem-estar social esperado é estritamente maior sob Regime B do que sob Regime A.

*Esboço*: a diferença se decompõe em três canais — dissuasão (Regime B eleva p_detecção), substituição (alguns trabalhadores que silenciariam passam a denunciar) e custo (recompensa privadamente financiada). □

> **Status (v0.1.0):** conjectura. O canal de **dissuasão** (p_detecção endógena) não existe no modelo atual — o tipo da firma é fixo na inicialização (DECISIONS D05). Além disso, "bem-estar" é hoje operacionalizado como VP − FP (contagem), sem excedente/custo. Reenunciar quando esses elementos forem implementados.
