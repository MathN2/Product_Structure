(() => {
  const state = { items: [], formulas: [], formulaId: null, explosion: null, productionQuantity: 1, toastTimer: null };
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => [...root.querySelectorAll(selector)];
  const currency = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' });

  async function api(path, options = {}) {
    const response = await fetch(path, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    });
    const body = await response.json().catch(() => null);
    if (!response.ok) {
      const detail = body?.detail || body?.mensagem || `Falha na API (${response.status})`;
      throw new Error(typeof detail === 'string' ? detail : JSON.stringify(detail));
    }
    return body;
  }

  function escapeHtml(value) {
    return String(value ?? '').replace(/[&<>"']/g, (char) => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
    })[char]);
  }

  function showToast(message, isError = false) {
    const toast = $('#toast');
    toast.textContent = message;
    toast.classList.toggle('error', isError);
    toast.classList.add('show');
    clearTimeout(state.toastTimer);
    state.toastTimer = setTimeout(() => toast.classList.remove('show'), 3600);
  }

  function setView(name) {
    $$('.view').forEach((view) => view.classList.toggle('active', view.id === `view-${name}`));
    $$('.nav-link').forEach((link) => link.classList.toggle('active', link.dataset.view === name));
    const labels = { inicio: 'Visão geral', itens: 'Itens', formulas: 'Fórmulas' };
    $('#breadcrumbCurrent').textContent = labels[name] || 'Visão geral';
  }

  function updateCounts() {
    $('#statItems').textContent = state.items.length;
    $('#statFormulas').textContent = state.formulas.length;
    $('#navItemCount').textContent = state.items.length;
    $('#navFormulaCount').textContent = state.formulas.length;
    $('#itemsHeadingCount').textContent = state.items.length;
    $('#itemsCountPill').textContent = `${state.items.length} ${state.items.length === 1 ? 'item' : 'itens'}`;
    $('#formulasHeadingCount').textContent = state.formulas.length;
    $('#formulaCountPill').textContent = state.formulas.length;
  }

  function renderItems() {
    updateCounts();
    const container = $('#itemsTable');
    if (!state.items.length) {
      container.innerHTML = '<div class="empty-state">Seu catálogo está vazio. Cadastre o primeiro item ao lado.</div>';
    } else {
      const rows = state.items.map((item) => `<tr>
        <td><span class="item-initial">${escapeHtml((item.nome || '?').slice(0, 1).toUpperCase())}</span><strong>${escapeHtml(item.nome)}</strong></td>
        <td>${escapeHtml(item.descricao || '—')}</td>
        <td><form class="item-price-form" data-item-id="${escapeHtml(item.id)}"><span>R$</span><input aria-label="Preço de ${escapeHtml(item.nome)}" type="number" min="0" step="0.01" value="${Number(item.preco || 0).toFixed(2)}" required><button class="mini-save" type="submit">Salvar</button></form></td>
        <td><button class="mini-delete" type="button" data-delete-item="${escapeHtml(item.id)}">Excluir</button></td>
      </tr>`).join('');
      container.innerHTML = `<table class="data-table"><thead><tr><th>ITEM</th><th>DESCRIÇÃO</th><th>PREÇO UNITÁRIO</th><th>AÇÕES</th></tr></thead><tbody>${rows}</tbody></table>`;
    }
    const usedNames = new Set(state.formulas.map((formula) => formula.nome));
    const available = state.items.filter((item) => !usedNames.has(item.nome));
    const select = $('#formulaItem');
    const current = select.value;
    select.innerHTML = '<option value="">Selecione um produto</option>' + available.map((item) =>
      `<option value="${escapeHtml(item.id)}">${escapeHtml(item.nome)}</option>`).join('');
    if (available.some((item) => String(item.id) === current)) select.value = current;
    $('#formulaForm button[type="submit"]').disabled = !available.length;
    if (available.length === 0) {
      $('#formulaItem').innerHTML = `<option value="">${state.items.length ? 'Todos os itens já têm fórmula' : 'Cadastre um item primeiro'}</option>`;
    }
  }

  function renderFormulaLists() {
    updateCounts();
    const formulaList = $('#formulaList');
    const recent = $('#recentFormulas');
    if (!state.formulas.length) {
      formulaList.innerHTML = '<div class="empty-state">Nenhuma fórmula cadastrada.</div>';
      recent.innerHTML = '<div class="empty-state">As fórmulas cadastradas aparecerão aqui.</div>';
    } else {
      formulaList.innerHTML = state.formulas.map((formula) => `<button class="formula-list-row ${String(formula.id) === String(state.formulaId) ? 'selected' : ''}" data-formula-id="${escapeHtml(formula.id)}">
        <span class="formula-symbol">⌘</span><span><strong>${escapeHtml(formula.nome)}</strong><small>Fórmula #${escapeHtml(formula.id)}</small></span><span class="row-arrow">→</span>
      </button>`).join('');
      recent.innerHTML = state.formulas.slice(0, 4).map((formula) => `<div class="recent-row" role="button" tabindex="0" data-recent-id="${escapeHtml(formula.id)}">
        <span class="formula-symbol">⌘</span><div><strong>${escapeHtml(formula.nome)}</strong><small>Fórmula de produto · #${escapeHtml(formula.id)}</small></div><b>→</b>
      </div>`).join('');
    }
    renderItems();
  }

  function flattenNodes(node, rows = [], depth = 0) {
    if (!node) return rows;
    rows.push({ id: node.node_id, nome: node.nome, depth });
    (node.componentes || []).forEach((child) => flattenNodes(child, rows, depth + 1));
    return rows;
  }

  function renderTreeNode(node, depth = 0) {
    const isRoot = depth === 0;
    const icon = isRoot ? '◆' : '•';
    const name = escapeHtml(node.nome);
    const qty = Number(node.quantidade || 1);
    const price = Number(node.preco || 0);
    const subline = isRoot ? 'Produto final' : `${currency.format(price)} por unidade`;
    const actions = isRoot ? '' : `<span class="tree-qty">× ${Number.isFinite(qty) ? qty : 1} necessários</span><form class="tree-qty-form" data-node-id="${escapeHtml(node.node_id)}" aria-label="Atualizar quantidade por produto de ${name}"><small>por produto</small><input aria-label="Quantidade de ${name} por produto" type="number" min="1" step="1" value="${Number(node.quantidade_por_unidade ?? qty) || 1}" required><button title="Salvar quantidade" type="submit">✓</button><button class="tree-remove" type="button" title="Remover componente" aria-label="Remover ${name}" data-remove-node="${escapeHtml(node.node_id)}">×</button></form>`;
    const children = (node.componentes || []).length
      ? `<div class="tree-children">${node.componentes.map((child) => `<div class="tree-child">${renderTreeNode(child, depth + 1)}</div>`).join('')}</div>`
      : '';
    return `<div class="${isRoot ? 'tree-root' : 'tree-row'}">
      <span class="tree-node-icon">${icon}</span><span class="tree-node-main"><strong>${name}</strong><small>${subline}</small></span>
      ${actions}
    </div>${children}`;
  }

  function renderDetail() {
    const panel = $('#formulaDetail');
    const formula = state.formulas.find((item) => String(item.id) === String(state.formulaId));
    if (!formula || !state.explosion) {
      panel.innerHTML = '<div class="empty-detail"><span class="empty-art">⌘</span><h2>Escolha uma fórmula</h2><p>Selecione uma fórmula da lista para visualizar sua explosão e gerenciar componentes.</p></div>';
      return;
    }
    const root = { ...state.explosion, quantidade: state.explosion.quantidade_producao || 1 };
    const flat = flattenNodes(state.explosion);
    const totalNodes = Math.max(flat.length - 1, 0);
    const totalUnits = flat.slice(1).reduce((sum, node) => sum + Number(node.quantidade || 0), 0);
    const totalPrice = state.explosion.custo_aquisicao ?? state.explosion.preco?.total ?? state.explosion.preco;
    const itemOptions = state.items.filter((item) => item.nome !== state.explosion.nome);
    const parentOptions = flat.filter((node) => node.id != null).map((node) =>
      `<option value="${escapeHtml(node.id)}">${'　'.repeat(node.depth)}${escapeHtml(node.nome)}</option>`).join('');
    const componentOptions = itemOptions.map((item) => `<option value="${escapeHtml(item.id)}">${escapeHtml(item.nome)}</option>`).join('');
    panel.innerHTML = `<div class="detail-header"><div><div class="detail-kicker">EXPLOSÃO DA FÓRMULA</div><h2 class="detail-title">${escapeHtml(formula.nome)}</h2><div class="detail-subtitle">Fórmula #${escapeHtml(formula.id)} · Produto final e seus componentes</div></div><div class="detail-actions"><button class="button button-danger" id="deleteFormula">Excluir</button></div></div>
      <div class="detail-metrics"><div class="metric-chip production-chip"><small>QUANTIDADE A PRODUZIR</small><div class="production-control"><input id="productionQuantity" type="number" min="1" step="1" value="${escapeHtml(state.productionQuantity)}" aria-label="Quantidade de produtos a produzir"><button id="calculateProduction" type="button">Calcular</button></div></div><div class="metric-chip"><small>UNIDADES NECESSÁRIAS</small><strong>${totalUnits} <span class="metric-muted">· ${totalNodes} componentes</span></strong></div><div class="metric-chip"><small>VALOR DE AQUISIÇÃO</small><strong>${totalPrice == null ? '—' : currency.format(Number(totalPrice))}</strong></div></div>
      <div class="tree-heading"><h3>Estrutura do produto</h3><small>${flat.length} ${flat.length === 1 ? 'nível' : 'nós'}</small></div>
      ${renderTreeNode(root)}
      <form id="componentForm" class="component-form"><h3>＋ Adicionar componente</h3><div class="component-fields">
        <div><label class="field-label" for="componentItem">Item</label><select id="componentItem" class="field" required><option value="">Selecione</option>${componentOptions}</select></div>
        <div><label class="field-label" for="componentParent">Adicionar dentro de</label><select id="componentParent" class="field" required>${parentOptions}</select></div>
        <div><label class="field-label" for="componentQuantity">Quantidade</label><input id="componentQuantity" class="field" type="number" min="1" step="1" value="1" required></div>
        <button class="button button-primary" type="submit" ${!itemOptions.length || !flat.some((node) => node.id != null) ? 'disabled' : ''}>Adicionar</button>
      </div>${!itemOptions.length ? '<div class="helper-text">Cadastre outro item para adicionar à estrutura.</div>' : ''}</form>`;
  }

  async function loadItems() {
    state.items = await api('/itens/');
    renderItems();
    if (state.explosion) renderDetail();
  }

  async function loadFormulas(preferredId = state.formulaId) {
    state.formulas = await api('/formulas/');
    renderFormulaLists();
    if (preferredId && state.formulas.some((item) => String(item.id) === String(preferredId))) {
      await selectFormula(preferredId, false);
    } else if (state.formulas.length) {
      await selectFormula(state.formulas[0].id, false);
    } else {
      state.formulaId = null;
      state.explosion = null;
      renderDetail();
    }
  }

  async function selectFormula(id, redraw = true, productionQuantity = state.productionQuantity) {
    state.formulaId = id;
    state.productionQuantity = Number(productionQuantity);
    state.explosion = await api(`/formulas/${encodeURIComponent(id)}?quantidade_producao=${encodeURIComponent(state.productionQuantity)}`);
    if (redraw) renderFormulaLists();
    renderDetail();
  }

  async function refreshAll() {
    const [itemsResult, formulasResult] = await Promise.allSettled([loadItems(), loadFormulas()]);
    const failed = [itemsResult, formulasResult].find((result) => result.status === 'rejected');
    const isOnline = !failed;
    $('#connectionLabel').textContent = isOnline ? 'API conectada' : 'API indisponível';
    $('.status-dot').classList.toggle('online', isOnline);
    $('.api-indicator').classList.toggle('online', isOnline);
    if (!failed) renderDetail();
    if (failed) showToast(`Não foi possível carregar os dados: ${failed.reason.message}`, true);
  }

  document.addEventListener('click', async (event) => {
    const nav = event.target.closest('[data-view]');
    if (nav) setView(nav.dataset.view);
    const go = event.target.closest('[data-go]');
    if (go) setView(go.dataset.go);
    const formulaButton = event.target.closest('[data-formula-id]');
    const recentButton = event.target.closest('[data-recent-id]');
    if (formulaButton || recentButton) {
      const id = formulaButton?.dataset.formulaId || recentButton?.dataset.recentId;
      setView('formulas');
      try { await selectFormula(id); } catch (error) { showToast(error.message, true); }
    }
    if (event.target.closest('#calculateProduction')) {
      const quantity = Number($('#productionQuantity').value);
      if (!Number.isInteger(quantity) || quantity < 1) {
        showToast('Informe uma quantidade inteira maior que zero.', true);
      } else {
        try { await selectFormula(state.formulaId, false, quantity); }
        catch (error) { showToast(error.message, true); }
      }
    }
    const deleteItem = event.target.closest('[data-delete-item]');
    if (deleteItem) {
      const item = state.items.find((candidate) => String(candidate.id) === deleteItem.dataset.deleteItem);
      if (!window.confirm(`Excluir o item “${item?.nome || 'selecionado'}”?`)) return;
      try {
        await api(`/itens/${encodeURIComponent(deleteItem.dataset.deleteItem)}`, { method: 'DELETE' });
        await loadItems();
        renderDetail();
        showToast('Item removido do catálogo.');
      } catch (error) { showToast(error.message, true); }
    }
    const remove = event.target.closest('[data-remove-node]');
    if (remove) {
      if (!window.confirm('Remover este componente e todos os seus subcomponentes?')) return;
      try {
        await api(`/formulas/${encodeURIComponent(state.formulaId)}/nodes/${encodeURIComponent(remove.dataset.removeNode)}`, { method: 'DELETE' });
        await selectFormula(state.formulaId);
        showToast('Componente removido da fórmula.');
      } catch (error) { showToast(error.message, true); }
    }
    if (event.target.closest('#deleteFormula')) {
      if (!window.confirm('Excluir esta fórmula e todos os seus componentes?')) return;
      const deletedId = state.formulaId;
      try {
        await api(`/formulas/${encodeURIComponent(deletedId)}`, { method: 'DELETE' });
        state.formulaId = null;
        await loadFormulas();
        showToast('Fórmula excluída.');
      } catch (error) { showToast(error.message, true); }
    }
  });

  document.addEventListener('keydown', (event) => {
    const recent = event.target.closest('[data-recent-id]');
    if (recent && (event.key === 'Enter' || event.key === ' ')) recent.click();
  });

  $('#itemForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const button = event.currentTarget.querySelector('button[type="submit"]');
    button.disabled = true;
    try {
      await api('/itens/', { method: 'POST', body: JSON.stringify({
        nome: String(form.get('nome')).trim(), descricao: String(form.get('descricao') || '').trim(), preco: Number(form.get('preco')),
      }) });
      event.currentTarget.reset();
      await loadItems();
      showToast('Item cadastrado no catálogo.');
    } catch (error) { showToast(error.message, true); }
    finally { button.disabled = false; }
  });

  $('#formulaForm').addEventListener('submit', async (event) => {
    event.preventDefault();
    const item = state.items.find((candidate) => String(candidate.id) === $('#formulaItem').value);
    if (!item) return;
    const button = event.currentTarget.querySelector('button[type="submit"]');
    button.disabled = true;
    try {
      const created = await api('/formulas/', { method: 'POST', body: JSON.stringify({ nome: item.nome }) });
      await loadFormulas(created.id);
      showToast('Fórmula criada. A raiz já está pronta para receber componentes.');
    } catch (error) { showToast(error.message, true); }
    finally { button.disabled = false; }
  });

  document.addEventListener('submit', async (event) => {
    const form = event.target;
    if (!form.matches('#componentForm, .item-price-form, .tree-qty-form')) return;
    event.preventDefault();
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    try {
      if (form.matches('.item-price-form')) {
        const id = form.dataset.itemId;
        const item = state.items.find((candidate) => String(candidate.id) === id);
        await api(`/itens/${encodeURIComponent(id)}`, { method: 'PATCH', body: JSON.stringify({
          nome: item.nome, descricao: item.descricao || '', preco: Number(form.querySelector('input').value),
        }) });
        await loadItems();
        if (state.formulaId) await selectFormula(state.formulaId);
        showToast('Preço atualizado. O custo da fórmula foi recalculado.');
      } else if (form.matches('.tree-qty-form')) {
        const quantidade = Number(form.querySelector('input').value);
        await api(`/formulas/${encodeURIComponent(state.formulaId)}/nodes/${encodeURIComponent(form.dataset.nodeId)}`, {
          method: 'PATCH', body: JSON.stringify({ quantidade }),
        });
        await selectFormula(state.formulaId);
        showToast('Quantidade do componente atualizada.');
      } else {
        await api(`/formulas/${encodeURIComponent(state.formulaId)}/nodes`, { method: 'POST', body: JSON.stringify({
          item_id: Number($('#componentItem').value), parent_id: Number($('#componentParent').value), quantidade: Number($('#componentQuantity').value),
        }) });
        await selectFormula(state.formulaId);
        showToast('Componente adicionado à estrutura.');
      }
    } catch (error) { showToast(error.message, true); button.disabled = false; }
  });

  refreshAll();
})();
