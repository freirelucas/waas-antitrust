/* ============================================================================
 * Simulador in-browser do modelo LCMC (ABM)
 *
 * Mini-versão fiel das fases P1..P3 do `WaaSModel` (Mesa 3.x) — escrita em
 * JavaScript puro para rodar no navegador sem nenhuma dependência. Não é
 * substituto do modelo Python; é uma "lupa didática" que permite ajustar
 * sliders e ver o efeito no bem-estar agregado em <1s.
 *
 * Implementa:
 * - Três populações: trabalhadores (3 arquétipos: ético/imitativo/racional),
 *   empresas (violadora/não-violadora), autoridade (escrow + janela adesão).
 * - P1 sinalização (decisão por arquétipo, com phi de vizinhança simplificada)
 * - P2 massa crítica intra-firma
 * - P2.5b abertura simultânea do escrow (R27)
 * - P2.5c janela de adesão pós-abertura com desconto progressivo (R29 — NOVO)
 * - P3 decisão de pagamento da firma (IC-F*)
 * - P4 dano social ponderado pela fatia de mercado
 *
 * Não implementa (deliberadamente): jogo global Morris-Shin, Hirschman,
 * choques R19, distribuição Pareto/Lognormal de fatia de mercado, erosão
 * Coleman R26, bootstrap multi-seed. Quem quer o modelo cheio roda o
 * Python local — `pip install -e .[dev]` e `python scripts/...`.
 * ========================================================================== */

(() => {
  "use strict";

  // ----------------------------------------------------------------------
  // Mini-RNG seedável (mulberry32) para reproducibilidade entre rodadas
  // ----------------------------------------------------------------------
  function mulberry32(seed) {
    let s = seed >>> 0;
    return function () {
      s = (s + 0x6d2b79f5) >>> 0;
      let t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // ----------------------------------------------------------------------
  // Mini-WaaSModel
  // ----------------------------------------------------------------------
  class WaaSSimMini {
    constructor(params) {
      this.p = Object.assign(
        {
          n_empresas: 10,
          tam_medio_empresa: 80,
          n_tiques: 24,
          seed: 11,
          regime: "B", // "A" | "B" | "C"
          fracao_violadoras: 0.5,
          taxa_observacao: 0.45,
          W_mult: 1.5, // recompensa em múltiplos do "salário anual"
          k_rel: 0.05, // massa crítica clássica (Regime A)
          q_min_cooperacao_interna: 0.1, // massa crítica do canal LCMC
          r_represalia: 0.5, // custo de represália individual
          usar_escrow_explicito: true,
          janela_escrow_tiques: 0,
          janela_adesao_pos_abertura: 10,
          descontos_faixas_adesao: [1.0, 0.7, 0.5, 0.3, 0.1],
          alpha_erosao: 0.0,
        },
        params || {}
      );
      this.rng = mulberry32(this.p.seed);
      this._init();
    }

    _init() {
      const p = this.p;
      this.tique = 0;
      this.empresas = [];
      this.trabalhadores = []; // flat list, com {id_empresa, arquetipo, w_a, sinalizou, depositou, aderiu_em_bloco}
      this.fatias = [];
      // Fatia uniforme normalizada (R13a "uniforme").
      const fatia = 1 / p.n_empresas;
      for (let i = 0; i < p.n_empresas; i++) {
        this.empresas.push({
          id: i,
          eh_violadora: this.rng() < p.fracao_violadoras,
          notificada_acum: 0,
          tcc_assinado: false,
          escrow: [],
          bloco_em_adesao: null, // {tique_abertura, depositantes_orig, aderentes}
        });
        this.fatias.push(fatia);
        for (let j = 0; j < p.tam_medio_empresa; j++) {
          // 50% éticos, 30% imitativos, 20% racionais (mistura didática)
          let arq = "racional";
          const r = this.rng();
          if (r < 0.5) arq = "ético";
          else if (r < 0.8) arq = "imitativo";
          this.trabalhadores.push({
            id_empresa: i,
            arquetipo: arq,
            w_a: 0.6 + this.rng() * 0.4, // severidade percebida ~ U(0.6, 1.0)
            sinalizou: false,
            depositou: false,
            aderiu_em_bloco: null,
            tique_cooperou: null,
          });
        }
      }
      // Reporters cumulativos
      this.n_sinais_acum = 0;
      this.n_depositos_acum = 0;
      this.n_aberturas_acum = 0;
      this.n_aderentes_acum = 0;
      this.n_blocos_em_adesao_acum = 0;
      this.n_tccs_acum = 0;
      this.dano_acum = 0;
      this.capital_social_residual = 1.0;
      this.serie = []; // {tique, violadoras_ativas, dano, bem_estar, n_depositos_em_escrow, n_aderentes_acum}
    }

    _W_esperado(prob_pagamento = 0.4) {
      // Recompensa esperada = W_mult * prob_pagamento (didático)
      return this.p.W_mult * prob_pagamento;
    }

    _trabalhadores_da(id_empresa) {
      return this.trabalhadores.filter((t) => t.id_empresa === id_empresa);
    }

    _phi_vizinhos(t, ws_firma_anterior) {
      // Phi: fração de "vizinhos" (mesma firma, neste caso simplificado)
      // que sinalizaram no tique anterior.
      if (!ws_firma_anterior || ws_firma_anterior.length === 0) return 0;
      const n_sig = ws_firma_anterior.filter((tt) => tt.sinalizou).length;
      return n_sig / ws_firma_anterior.length;
    }

    step() {
      const p = this.p;
      const W_ativo = p.regime !== "A";
      // P0 — observação (probabilidade fixa por tique, sem memória)
      for (const t of this.trabalhadores) {
        t.observou = this.rng() < p.taxa_observacao;
      }
      // P1 — sinalização (por arquétipo)
      // Snapshot do tique anterior para phi.
      const phi_por_firma = new Map();
      for (let i = 0; i < p.n_empresas; i++) {
        phi_por_firma.set(i, this._phi_vizinhos(null, this._trabalhadores_da(i)));
      }
      const W_esp = this._W_esperado();
      for (const t of this.trabalhadores) {
        if (!t.observou && t.arquetipo !== "oportunista") {
          t.sinaliza_agora = false;
          continue;
        }
        if (t.arquetipo === "ético") {
          t.sinaliza_agora = this.rng() < 0.6; // ético tem propensão alta
        } else if (t.arquetipo === "imitativo") {
          const phi = phi_por_firma.get(t.id_empresa) || 0;
          t.sinaliza_agora = phi >= 0.3;
        } else {
          // racional: IR-W simplificada
          const ganho = W_esp;
          const custo = p.r_represalia * t.w_a;
          t.sinaliza_agora = W_ativo && ganho > custo;
        }
      }
      // P2 — massa crítica clássica + depósito condicional
      for (const e of this.empresas) {
        const ws = this._trabalhadores_da(e.id);
        const n_sig = ws.filter((t) => t.sinaliza_agora).length;
        const k_req = Math.max(1, Math.floor(p.k_rel * ws.length));
        // R27: depósita cada sinal no escrow se usar_escrow_explicito.
        if (W_ativo && p.usar_escrow_explicito) {
          for (const t of ws) {
            if (t.sinaliza_agora && !t.depositou) {
              e.escrow.push({
                id_trabalhador: this.trabalhadores.indexOf(t),
                qualidade_prova: 0.5,
                tique_deposito: this.tique,
              });
              t.depositou = true;
              this.n_depositos_acum++;
            }
          }
        }
        e.notificada_no_periodo = W_ativo && n_sig >= k_req;
        if (e.notificada_no_periodo) e.notificada_acum++;
        for (const t of ws) {
          if (t.sinaliza_agora) this.n_sinais_acum++;
        }
      }
      // P2.5a — expiração R27-ii
      if (p.usar_escrow_explicito && p.janela_escrow_tiques > 0) {
        for (const e of this.empresas) {
          e.escrow = e.escrow.filter(
            (d) => this.tique - d.tique_deposito < p.janela_escrow_tiques
          );
        }
      }
      // P2.5b — abertura simultânea quando massa crítica intra-firma é atingida
      if (p.usar_escrow_explicito) {
        for (const e of this.empresas) {
          const n_emp = this._trabalhadores_da(e.id).length;
          if (n_emp <= 0) continue;
          const fracao = e.escrow.length / n_emp;
          if (fracao >= p.q_min_cooperacao_interna && e.escrow.length > 0) {
            const depositantes_orig = e.escrow.slice();
            e.escrow = [];
            e.notificada_no_periodo = true;
            this.n_aberturas_acum++;
            // P2.5c hook: registra bloco em janela de adesão (R29)
            if (p.janela_adesao_pos_abertura > 0 && !e.bloco_em_adesao) {
              e.bloco_em_adesao = {
                tique_abertura: this.tique,
                depositantes_originais: depositantes_orig,
                aderentes: [],
              };
              this.n_blocos_em_adesao_acum++;
            }
          }
        }
      }
      // P2.5c — janela de adesão pós-abertura (R29)
      if (p.usar_escrow_explicito && p.janela_adesao_pos_abertura > 0) {
        for (const e of this.empresas) {
          const reg = e.bloco_em_adesao;
          if (!reg) continue;
          const idade = this.tique - reg.tique_abertura;
          if (idade >= p.janela_adesao_pos_abertura) {
            e.bloco_em_adesao = null;
            continue;
          }
          const ws = this._trabalhadores_da(e.id);
          const ja_dentro = new Set(
            reg.depositantes_originais.map((d) => d.id_trabalhador).concat(
              reg.aderentes.map((a) => a.id_trabalhador)
            )
          );
          for (const t of ws) {
            const tid = this.trabalhadores.indexOf(t);
            if (ja_dentro.has(tid)) continue;
            const pos = reg.aderentes.length;
            const faixa = Math.min(p.descontos_faixas_adesao.length - 1, pos);
            const fator = p.descontos_faixas_adesao[faixa];
            if (fator <= 0) continue;
            // IR-W projetada: aderir só se fator * W_max > custo represália
            if (fator * this._W_esperado(1.0) <= p.r_represalia * t.w_a) continue;
            reg.aderentes.push({
              id_trabalhador: tid,
              faixa,
              fator_desconto: fator,
              tique_adesao: this.tique,
            });
            t.aderiu_em_bloco = e.id;
            t.tique_cooperou = this.tique;
            this.n_aderentes_acum++;
            ja_dentro.add(tid);
          }
        }
      }
      // P3 — decisão de pagamento da firma (IC-F* simplificada)
      for (const e of this.empresas) {
        if (!e.notificada_no_periodo || e.tcc_assinado) continue;
        // Firma assina TCC se IC-F* fechar: D > W
        // D = desconto base ≈ 0.45; W = W_mult * (n_aderentes + n_disparados)
        const ws = this._trabalhadores_da(e.id);
        const n_disparados = ws.filter((t) => t.sinaliza_agora || t.depositou).length;
        const n_aderentes = (e.bloco_em_adesao?.aderentes?.length || 0);
        const W_total = p.W_mult * (n_disparados + 0.5 * n_aderentes);
        const D = 0.45 * (W_total + 1); // proxy didático
        if (W_ativo && D > W_total) {
          e.tcc_assinado = true;
          this.n_tccs_acum++;
        }
      }
      // P4 — atualização do estado e dano
      let violadoras_ativas = 0;
      for (const e of this.empresas) {
        // Firma sob TCC ou que foi notificada várias vezes deixa de violar
        if (e.tcc_assinado) e.eh_violadora = false;
        if (e.notificada_acum >= 3 && W_ativo) e.eh_violadora = false;
        if (e.eh_violadora) violadoras_ativas++;
      }
      // Dano social no tique = soma de fatias das violadoras × overcharge (proxy 1)
      let dano_tique = 0;
      for (let i = 0; i < this.empresas.length; i++) {
        if (this.empresas[i].eh_violadora) dano_tique += this.fatias[i];
      }
      this.dano_acum += dano_tique;
      // Bem-estar agregado: medida normalizada (1 - dano relativo)
      const bem_estar = 1 - this.dano_acum / Math.max(1, this.tique + 1);
      // Erosão Coleman R26 (opcional)
      const n_notificadas_neste = this.empresas.filter(
        (e) => e.notificada_no_periodo
      ).length;
      if (p.alpha_erosao > 0 && n_notificadas_neste > 0) {
        this.capital_social_residual *= Math.pow(
          1 - p.alpha_erosao * 0.3,
          n_notificadas_neste
        );
      }
      // Conta depósitos ainda em escrow
      const n_em_escrow = this.empresas.reduce((acc, e) => acc + e.escrow.length, 0);
      this.serie.push({
        tique: this.tique,
        violadoras_ativas,
        dano_acum: this.dano_acum,
        bem_estar,
        n_sinais_acum: this.n_sinais_acum,
        n_em_escrow,
        n_depositos_acum: this.n_depositos_acum,
        n_aderentes_acum: this.n_aderentes_acum,
        n_blocos_em_adesao_acum: this.n_blocos_em_adesao_acum,
        n_tccs_acum: this.n_tccs_acum,
        capital_social_residual: this.capital_social_residual,
      });
      this.tique++;
    }

    executar() {
      while (this.tique < this.p.n_tiques) this.step();
      return this.serie;
    }
  }

  // ----------------------------------------------------------------------
  // Plotagem em Canvas (sem D3, sem Chart.js)
  // ----------------------------------------------------------------------
  function plotarSerie(canvas, series, opts) {
    const ctx = canvas.getContext("2d");
    const W = canvas.width;
    const H = canvas.height;
    ctx.clearRect(0, 0, W, H);
    // fundo
    ctx.fillStyle = opts.bg || "#fafafa";
    ctx.fillRect(0, 0, W, H);
    const pad = { top: 18, right: 14, bottom: 28, left: 44 };
    const plotW = W - pad.left - pad.right;
    const plotH = H - pad.top - pad.bottom;
    // Encontra extremos
    let maxY = 0;
    let minY = 0;
    const cores = opts.cores || ["#27AE60", "#5D6D7E", "#8E44AD", "#C0392B"];
    for (const s of series) {
      for (const v of s.data) {
        if (v > maxY) maxY = v;
        if (v < minY) minY = v;
      }
    }
    if (maxY === minY) maxY = minY + 1;
    const padY = (maxY - minY) * 0.1;
    maxY += padY;
    minY = Math.max(0, minY - padY);
    const xs = series[0]?.x || [];
    if (xs.length === 0) return;
    const maxX = Math.max(...xs);
    function sx(x) {
      return pad.left + (x / Math.max(1, maxX)) * plotW;
    }
    function sy(y) {
      return pad.top + plotH - ((y - minY) / (maxY - minY)) * plotH;
    }
    // Eixos
    ctx.strokeStyle = "#2C3E50";
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(pad.left, pad.top);
    ctx.lineTo(pad.left, pad.top + plotH);
    ctx.lineTo(pad.left + plotW, pad.top + plotH);
    ctx.stroke();
    // Ticks Y
    ctx.fillStyle = "#2C3E50";
    ctx.font = "10px sans-serif";
    ctx.textAlign = "right";
    for (let i = 0; i <= 4; i++) {
      const y = minY + ((maxY - minY) * i) / 4;
      const py = sy(y);
      ctx.strokeStyle = "rgba(0,0,0,0.07)";
      ctx.beginPath();
      ctx.moveTo(pad.left, py);
      ctx.lineTo(pad.left + plotW, py);
      ctx.stroke();
      ctx.fillText(y.toFixed(maxY > 10 ? 0 : 2), pad.left - 4, py + 3);
    }
    // Ticks X (a cada ~5)
    ctx.textAlign = "center";
    const passo = Math.max(1, Math.floor(maxX / 6));
    for (let x = 0; x <= maxX; x += passo) {
      const px = sx(x);
      ctx.strokeStyle = "rgba(0,0,0,0.07)";
      ctx.beginPath();
      ctx.moveTo(px, pad.top);
      ctx.lineTo(px, pad.top + plotH);
      ctx.stroke();
      ctx.fillStyle = "#2C3E50";
      ctx.fillText(String(x), px, pad.top + plotH + 14);
    }
    // Título
    ctx.textAlign = "left";
    ctx.fillStyle = "#2C3E50";
    ctx.font = "bold 11px sans-serif";
    ctx.fillText(opts.titulo || "", pad.left, pad.top - 4);
    // Séries
    series.forEach((s, idx) => {
      ctx.strokeStyle = s.cor || cores[idx % cores.length];
      ctx.lineWidth = 2;
      ctx.beginPath();
      for (let i = 0; i < s.x.length; i++) {
        const px = sx(s.x[i]);
        const py = sy(s.data[i]);
        if (i === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.stroke();
    });
    // Legenda
    let lx = pad.left + 6;
    const ly = pad.top + 6;
    ctx.font = "10px sans-serif";
    series.forEach((s, idx) => {
      const cor = s.cor || cores[idx % cores.length];
      ctx.fillStyle = cor;
      ctx.fillRect(lx, ly, 10, 10);
      ctx.fillStyle = "#2C3E50";
      ctx.fillText(s.label, lx + 14, ly + 9);
      lx += 14 + ctx.measureText(s.label).width + 14;
    });
  }

  // ----------------------------------------------------------------------
  // UI: cria controles, escuta mudanças, roda comparação A vs Regime escolhido
  // ----------------------------------------------------------------------
  function rodarComparativo(params) {
    // Sempre roda Regime A como baseline + Regime escolhido na mesma seed.
    const baseA = new WaaSSimMini(Object.assign({}, params, { regime: "A" }));
    baseA.executar();
    const tratamento = new WaaSSimMini(params);
    tratamento.executar();
    return { baseA, tratamento };
  }

  function atualizarGraficos(out) {
    const xs = out.baseA.serie.map((s) => s.tique);
    const cores = { A: "#5D6D7E", B: "#27AE60", C: "#8E44AD", EUA: "#D68910", UE: "#16A085" };
    const corRegime = cores[out.tratamento.p.regime] || "#27AE60";
    const cv = document.getElementById("sim-canvas-dano");
    if (cv) {
      plotarSerie(
        cv,
        [
          { label: "Regime A", x: xs, data: out.baseA.serie.map((s) => s.dano_acum), cor: cores.A },
          {
            label: `Regime ${out.tratamento.p.regime}`,
            x: xs,
            data: out.tratamento.serie.map((s) => s.dano_acum),
            cor: corRegime,
          },
        ],
        { titulo: "(A) Dano social acumulado (proxy)" }
      );
    }
    const cv2 = document.getElementById("sim-canvas-violadoras");
    if (cv2) {
      plotarSerie(
        cv2,
        [
          {
            label: "Regime A",
            x: xs,
            data: out.baseA.serie.map((s) => s.violadoras_ativas),
            cor: cores.A,
          },
          {
            label: `Regime ${out.tratamento.p.regime}`,
            x: xs,
            data: out.tratamento.serie.map((s) => s.violadoras_ativas),
            cor: corRegime,
          },
        ],
        { titulo: "(B) Violadoras ativas por tique" }
      );
    }
    const cv3 = document.getElementById("sim-canvas-canal");
    if (cv3) {
      plotarSerie(
        cv3,
        [
          {
            label: "Em escrow",
            x: xs,
            data: out.tratamento.serie.map((s) => s.n_em_escrow),
            cor: "#16A085",
          },
          {
            label: "Aderentes pós-abertura",
            x: xs,
            data: out.tratamento.serie.map((s) => s.n_aderentes_acum),
            cor: "#27AE60",
          },
          {
            label: "TCCs assinados (acum)",
            x: xs,
            data: out.tratamento.serie.map((s) => s.n_tccs_acum),
            cor: "#8E44AD",
          },
        ],
        { titulo: "(C) Canal LCMC — escrow, adesões, TCCs" }
      );
    }
    const cv4 = document.getElementById("sim-canvas-capital");
    if (cv4) {
      plotarSerie(
        cv4,
        [
          {
            label: "Capital social residual",
            x: xs,
            data: out.tratamento.serie.map((s) => s.capital_social_residual),
            cor: "#C0392B",
          },
        ],
        { titulo: "(D) Capital social (R26 Coleman)" }
      );
    }
    // KPIs no rodapé
    const ult = out.tratamento.serie[out.tratamento.serie.length - 1] || {};
    const ultA = out.baseA.serie[out.baseA.serie.length - 1] || {};
    const set = (id, val) => {
      const el = document.getElementById(id);
      if (el) el.textContent = val;
    };
    set("sim-kpi-dano-A", (ultA.dano_acum || 0).toFixed(2));
    set("sim-kpi-dano-T", (ult.dano_acum || 0).toFixed(2));
    set("sim-kpi-aderentes", ult.n_aderentes_acum || 0);
    set("sim-kpi-blocos", ult.n_blocos_em_adesao_acum || 0);
    set("sim-kpi-tccs", ult.n_tccs_acum || 0);
    const delta =
      (ultA.dano_acum || 0) > 0
        ? (100 * (1 - (ult.dano_acum || 0) / ultA.dano_acum)).toFixed(1) + "%"
        : "—";
    set("sim-kpi-delta", delta);
  }

  function lerParams() {
    const $ = (id) => document.getElementById(id);
    const val = (id, def) => {
      const el = $(id);
      if (!el) return def;
      if (el.type === "checkbox") return el.checked;
      const n = parseFloat(el.value);
      return Number.isFinite(n) ? n : def;
    };
    const reg = ($("sim-regime")?.value) || "B";
    return {
      n_empresas: val("sim-n-empresas", 10),
      tam_medio_empresa: val("sim-tam-empresa", 80),
      n_tiques: val("sim-n-tiques", 24),
      seed: val("sim-seed", 11),
      regime: reg,
      fracao_violadoras: val("sim-fracao-violadoras", 0.5),
      taxa_observacao: val("sim-taxa-observacao", 0.45),
      W_mult: val("sim-w-mult", 1.5),
      k_rel: val("sim-k-rel", 0.05),
      q_min_cooperacao_interna: val("sim-q-min", 0.1),
      r_represalia: val("sim-r-represalia", 0.5),
      usar_escrow_explicito: val("sim-escrow", true),
      janela_escrow_tiques: val("sim-janela-escrow", 0),
      janela_adesao_pos_abertura: val("sim-janela-adesao", 10),
      alpha_erosao: val("sim-alpha-erosao", 0.0),
    };
  }

  function montarUI() {
    if (!document.getElementById("sim-controles")) return;
    const sliders = [
      ["sim-n-empresas", "Número de firmas", "n_empresas"],
      ["sim-tam-empresa", "Trabalhadores por firma", "tam_medio_empresa"],
      ["sim-n-tiques", "Horizonte (tiques)", "n_tiques"],
      ["sim-fracao-violadoras", "Fração violadoras (0–1)", "fracao_violadoras"],
      ["sim-taxa-observacao", "Taxa de observação (0–1)", "taxa_observacao"],
      ["sim-w-mult", "Recompensa W_mult (0–4)", "W_mult"],
      ["sim-k-rel", "Massa crítica clássica k_rel (0–0,25)", "k_rel"],
      ["sim-q-min", "Massa crítica do canal q_min (0–0,3)", "q_min_cooperacao_interna"],
      ["sim-r-represalia", "Custo de represália r (0–1)", "r_represalia"],
      ["sim-janela-escrow", "Janela de expiração escrow (0–12)", "janela_escrow_tiques"],
      ["sim-janela-adesao", "Janela de adesão R29 (0–20)", "janela_adesao_pos_abertura"],
      ["sim-alpha-erosao", "Erosão Coleman alpha (0–0,9)", "alpha_erosao"],
      ["sim-seed", "Semente RNG", "seed"],
    ];
    for (const [id] of sliders) {
      const el = document.getElementById(id);
      if (el) {
        el.addEventListener("input", agendarRodada);
        el.addEventListener("change", agendarRodada);
      }
    }
    const escrow = document.getElementById("sim-escrow");
    if (escrow) escrow.addEventListener("change", agendarRodada);
    const reg = document.getElementById("sim-regime");
    if (reg) reg.addEventListener("change", agendarRodada);
    const btn = document.getElementById("sim-rodar");
    if (btn) btn.addEventListener("click", rodar);
    // Atualiza display dos valores
    for (const [id] of sliders) {
      const el = document.getElementById(id);
      const out = document.getElementById(id + "-val");
      if (el && out) {
        const sync = () => {
          out.textContent = el.value;
        };
        sync();
        el.addEventListener("input", sync);
      }
    }
  }

  let rodadaPendente = null;
  function agendarRodada() {
    if (rodadaPendente) clearTimeout(rodadaPendente);
    rodadaPendente = setTimeout(rodar, 200);
  }

  function rodar() {
    const params = lerParams();
    const t0 = performance.now();
    const out = rodarComparativo(params);
    const dt = performance.now() - t0;
    const tempo = document.getElementById("sim-tempo");
    if (tempo) tempo.textContent = `rodada em ${dt.toFixed(0)} ms · seed ${params.seed}`;
    atualizarGraficos(out);
  }

  // Boot
  function init() {
    montarUI();
    if (document.getElementById("sim-controles")) rodar();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
  // MkDocs Material faz navegação SPA — re-inicia quando o DOM muda.
  document.addEventListener("DOMContentSwitch", init);
})();
